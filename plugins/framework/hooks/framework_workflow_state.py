"""Per-conversation scratch state for Cursor workflow hooks.

Cursor does not list every edited file in its end-of-turn payload, so the
recorders accumulate what the gate needs into a small JSON file keyed by
conversation id. State lives under ``.cursor/.workflow-state``.

The recorded list is a *lower bound* on what changed: it misses Tab edits,
shell/``sed``-driven edits, subagent edits, and human edits. The stop gate
reconciles it against ``git`` before treating it as the changed set.

``git`` alone is a poor *upper* bound, though: a repository can carry unrelated
in-flight work (a half-finished refactor, another branch's staging), and
attributing that to this conversation makes the gate permanently red. So the
first recorder invocation snapshots the already-dirty file set as ``baseline``,
and the gate attributes only ``recorded | (dirty - baseline)``.

State layout::

    {
      "files": ["addons/example_addon/api/components/record.py", ...],
      "unverified": ["addons/example_addon/api/components/record.py"],
      "baseline": ["some/preexisting/dirty.py", ...],       # dirty before this conversation
      "deslop_announced": false,
      "updated": 1735689600.0
    }
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

STATE_DIR = ".cursor/.workflow-state"
DESLOP_SENTINEL = "deslop suite:"
MAX_AGE_SECONDS = 24 * 60 * 60
GIT_TIMEOUT_SECONDS = 15
UNSAFE_ID = re.compile(r"[^A-Za-z0-9_-]")

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
try:
    from scripts.worktree.checkout_identity import linked_worktree_root
    from scripts.workspace.project_env import worktree_dir as configured_worktree_dir
except ImportError:  # pragma: no cover - hooks always ship with scripts/

    def configured_worktree_dir(root: Path | None = None) -> Path | None:
        """Return no configured worktree parent when project env cannot load."""
        return None

    def linked_worktree_root(live_root: Path, candidate: Path) -> Path | None:
        """Return no linked worktree when checkout identity cannot load."""
        return None


def project_root() -> Path:
    """Return the repository root exported by Cursor, or this checkout."""
    env_root = os.environ.get("CURSOR_PROJECT_DIR")
    if env_root:
        candidate = Path(env_root)
        if candidate.is_dir():
            return candidate.resolve()
    return Path(__file__).resolve().parents[2]


def state_path(root: Path, conversation_id: str) -> Path:
    """Return the Cursor state path for one conversation.

    Args:
        root: Repository root.
        conversation_id: Active conversation identifier.

    Returns:
        Absolute path to the conversation JSON state file.
    """
    safe = UNSAFE_ID.sub("_", conversation_id or "")[:120] or "unknown"
    return root / STATE_DIR / f"{safe}.json"


def record_exists(root: Path, conversation_id: str) -> bool:
    """True when this conversation has recorded at least one edit."""
    return state_path(root, conversation_id).is_file()


def load(root: Path, conversation_id: str) -> dict[str, Any]:
    """Read one conversation's state, returning an empty record when absent."""
    path = state_path(root, conversation_id)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return _empty()
    if not isinstance(data, dict):
        return _empty()
    record = _empty()
    for key in ("files", "unverified", "baseline"):
        value = data.get(key)
        if isinstance(value, list):
            record[key] = [item for item in value if isinstance(item, str)]
    record["deslop_announced"] = bool(data.get("deslop_announced", False))
    worktrees = data.get("worktrees")
    if isinstance(worktrees, dict):
        cleaned: dict[str, Any] = {}
        for key, payload in worktrees.items():
            if not isinstance(key, str) or not isinstance(payload, dict):
                continue
            entry = _empty_worktree(str(payload.get("root") or ""))
            for field in ("files", "unverified", "baseline"):
                value = payload.get(field)
                if isinstance(value, list):
                    entry[field] = [item for item in value if isinstance(item, str)]
            if entry["root"]:
                cleaned[key] = entry
        record["worktrees"] = cleaned
    return record


def git_dirty(root: Path) -> set[str]:
    """Repo-relative paths git currently reports as changed or untracked."""
    files: set[str] = set()
    commands = (
        ["git", "diff", "--name-only", "HEAD"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    )
    for command in commands:
        try:
            result = subprocess.run(
                command,
                cwd=root,
                capture_output=True,
                text=True,
                timeout=GIT_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            line = line.strip()
            if line:
                files.add(line)
    return files


def update(
    root: Path,
    conversation_id: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    """Apply ``mutate`` to the conversation record and write it back atomically.

    On the first write for a conversation, snapshot the already-dirty file set
    so the gate can subtract pre-existing work it did not cause. The file being
    recorded right now is normally already dirty and therefore lands in the
    baseline, but it is also in ``files``, and the gate unions the two.

    ``os.replace`` prevents a torn file, not a lost update: two concurrent hook
    processes for the same conversation can still clobber each other. The stop
    gate does not trust this list as ground truth, so a rare lost append only
    weakens the deslop nudge, never correctness.
    """
    is_new = not record_exists(root, conversation_id)
    record = load(root, conversation_id)
    if is_new:
        record["baseline"] = sorted(git_dirty(root))
    mutate(record)
    record["updated"] = time.time()
    path = state_path(root, conversation_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)
    prune(path.parent)


def prune(state_dir: Path) -> None:
    """Delete conversation records older than ``MAX_AGE_SECONDS``."""
    cutoff = time.time() - MAX_AGE_SECONDS
    for path in state_dir.glob("*.json"):
        try:
            if path.stat().st_mtime < cutoff:
                path.unlink()
        except OSError:
            continue


def relative_path(root: Path, raw: str) -> str | None:
    """Normalize an edited path to a repo-relative POSIX path, or None if outside.

    Prefer :func:`resolve_edit` when the path may live under an ephemeral
    ``~/worktrees/<ISSUE-KEY>`` clone; this helper only accepts ``root``.
    """
    resolved = resolve_edit(root, raw)
    if resolved is None:
        return None
    checkout, relative = resolved
    try:
        if checkout.resolve() != root.resolve():
            return None
    except OSError:
        return None
    return relative


def resolve_edit(project_root: Path, raw: str) -> tuple[Path, str] | None:
    """Map an edit path to ``(checkout_root, repo_relative)``.

    Accepts the live editor project root, a linked git worktree of that
    repository (including ``~/.cursor/worktrees/<repo>/<name>``), and, when
    ``project.env`` sets ``WORKTREE_DIR``, a child checkout under that
    directory.
    """
    if not raw:
        return None
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    try:
        resolved = candidate.resolve()
        live = project_root.resolve()
    except OSError:
        return None

    try:
        return live, resolved.relative_to(live).as_posix()
    except ValueError:
        pass

    linked = linked_worktree_root(live, resolved)
    if linked is not None:
        try:
            return linked, resolved.relative_to(linked).as_posix()
        except ValueError:
            return None

    worktree_parent = configured_worktree_dir(project_root)
    if worktree_parent is None or not worktree_parent.is_dir():
        return None

    try:
        relative_to_parent = resolved.relative_to(worktree_parent)
    except ValueError:
        return None

    parts = relative_to_parent.parts
    if not parts:
        return None
    checkout = (worktree_parent / parts[0]).resolve()
    if not checkout.is_dir():
        return None
    if not ((checkout / ".git").exists() or (checkout / "framework").is_dir()):
        return None
    try:
        return checkout, resolved.relative_to(checkout).as_posix()
    except ValueError:
        return None


def record_path(
    project_root: Path,
    conversation_id: str,
    raw_path: str,
) -> str | None:
    """Record one edited path under the live root or a known issue worktree.

    Returns the repo-relative path when recorded, otherwise ``None``.
    """
    resolved = resolve_edit(project_root, raw_path)
    if resolved is None:
        return None
    checkout, relative = resolved
    if relative.startswith(STATE_DIR):
        return None

    try:
        live = project_root.resolve()
        checkout_resolved = checkout.resolve()
    except OSError:
        return None

    if checkout_resolved == live:

        def add_live(record: dict[str, Any]) -> None:
            for key in ("files", "unverified"):
                if relative not in record[key]:
                    record[key].append(relative)

        update(project_root, conversation_id, add_live)
        return relative

    key = checkout_resolved.name

    def add_worktree(record: dict[str, Any]) -> None:
        worktrees = record.setdefault("worktrees", {})
        entry = worktrees.get(key)
        if not isinstance(entry, dict) or not entry.get("root"):
            entry = _empty_worktree(str(checkout_resolved))
            entry["baseline"] = sorted(git_dirty(checkout_resolved))
            worktrees[key] = entry
        else:
            entry["root"] = str(checkout_resolved)
            entry.setdefault("files", [])
            entry.setdefault("unverified", [])
            entry.setdefault("baseline", [])
        for field in ("files", "unverified"):
            values = entry.setdefault(field, [])
            if relative not in values:
                values.append(relative)

    update(project_root, conversation_id, add_worktree)
    return relative


def read_event() -> dict[str, Any]:
    """Parse and normalize a Cursor hook payload.

    Returns:
        A dict with Cursor fields when stdin held valid JSON; otherwise ``{}``.
    """
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def _empty_worktree(root: str = "") -> dict[str, Any]:
    """Return an empty per-worktree edit record."""
    return {
        "root": root,
        "files": [],
        "unverified": [],
        "baseline": [],
    }


def _empty() -> dict[str, Any]:
    return {
        "files": [],
        "unverified": [],
        "baseline": [],
        "deslop_announced": False,
        "worktrees": {},
    }
