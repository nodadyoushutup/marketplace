#!/usr/bin/env python3
"""stop gate: refuse to end a turn on red, and require the deslop suite.

Runs the repo's verification commands itself rather than trusting a claim that
they passed. The changed set is ``recorded | (git dirty - baseline)``: the
recorded edits alone miss Tab, shell, subagent, and human edits, while raw git
dirt would wrongly attribute unrelated in-flight work in the repository to this
conversation and keep the gate permanently red.

Supports linked git worktrees and ``WORKTREE_DIR`` clones: edits recorded
there are verified with that checkout as the root (pytest and vitest cwd,
plus optional ``node_modules`` symlink from the live GUI runtime).

Fails open: any internal problem emits an empty result so the turn ends
normally. These are observational hooks; they never exit ``2`` (deny).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import framework_workflow_state as ws  # noqa: E402

MAX_FOLLOWUPS = 2
VERIFY_TIMEOUT_SECONDS = 150
QUALITY_FILE_THRESHOLD = 12
OUTPUT_TAIL_CHARS = 2500
LISTED_FILES = 15

GUI_DIR = "framework/runtimes/gui"
PYTHON_ROOTS = ("framework/", "addons/", "scripts/")
RUNTIME_DIRS = ("api", "beat", "gui", "mcp", "worker")
SOURCE_SUFFIXES = (".py", ".js", ".jsx", ".mjs", ".cjs")
GUI_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs")
GENERATED_MARKERS = (
    "addonGui.generated.js",
    ".framework-addons/",
    "node_modules/",
    "docs/sphinx/source/code/",
    "/migrations/versions/",
)


def main() -> None:
    """Run framework verification and quality gates at editor turn completion."""
    event = ws.read_event()
    if not _turn_finished(event) or _already_looping(event):
        return emit()
    conversation_id = event.get("conversation_id")
    if not isinstance(conversation_id, str):
        return emit()

    root = ws.project_root()
    if not ws.record_exists(root, conversation_id):
        return emit()
    text = event.get("text")
    if isinstance(text, str) and ws.DESLOP_SENTINEL in text.lower():
        ws.update(root, conversation_id, _mark_deslop_announced)
    record = ws.load(root, conversation_id)

    changed = _changed_set(root, record)
    failure = run_verification(root, changed, live_root=root)
    if failure is not None:
        return emit(failure)

    for worktree in (record.get("worktrees") or {}).values():
        if not isinstance(worktree, dict):
            continue
        wt_root_raw = worktree.get("root")
        if not isinstance(wt_root_raw, str) or not wt_root_raw:
            continue
        wt_root = Path(wt_root_raw)
        if not wt_root.is_dir():
            continue
        wt_changed = _changed_set(wt_root, worktree)
        failure = run_verification(wt_root, wt_changed, live_root=root)
        if failure is not None:
            return emit(failure)

    if record["unverified"] or any(
        isinstance(wt, dict) and wt.get("unverified")
        for wt in (record.get("worktrees") or {}).values()
    ):
        ws.update(root, conversation_id, _clear_unverified)

    all_changed = list(changed)
    for worktree in (record.get("worktrees") or {}).values():
        if isinstance(worktree, dict):
            all_changed.extend(
                _changed_set(Path(str(worktree.get("root") or root)), worktree)
            )
    reminder = quality_reminder(record, sorted(set(all_changed)))
    # Mark on emit so the nudge fires once. Waiting for the agent to echo
    # ``deslop suite:`` re-spammed every stop when the pass was interrupted
    # or dismissed.
    if reminder:
        ws.update(root, conversation_id, _mark_deslop_announced)
    return emit(reminder)


def _changed_set(root: Path, record: dict) -> list[str]:
    """Files this conversation changed: recorded edits plus new git dirt.

    Anything already dirty when the conversation started is excluded; the gate
    verifies what this conversation did, not the repository's in-flight work.
    """
    attributable = ws.git_dirty(root) - set(record.get("baseline") or [])
    combined = (
        set(record.get("files") or [])
        | set(record.get("unverified") or [])
        | attributable
    )
    return sorted(p for p in combined if p and not p.startswith(ws.STATE_DIR))


def run_verification(
    root: Path,
    changed: list[str],
    *,
    live_root: Path,
) -> str | None:
    """Run the checks the touched paths call for; return a follow-up on failure."""
    for label, command, cwd, env in plan_checks(root, changed, live_root=live_root):
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=VERIFY_TIMEOUT_SECONDS,
                env=env,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.returncode != 0:
            return verification_followup(label, result)
    return None


def plan_checks(
    root: Path,
    changed: list[str],
    *,
    live_root: Path | None = None,
) -> list[tuple[str, list[str], Path, dict[str, str]]]:
    """Select verification commands for the files changed this conversation."""
    live = (live_root or root).resolve()
    checks: list[tuple[str, list[str], Path, dict[str, str]]] = []
    base_env = os.environ.copy()

    isolation_check = root / "scripts" / "addon" / "check_addon_isolation.py"
    if changed and isolation_check.is_file():
        checks.append(
            (
                "custom addon isolation",
                [_python_bin(root, live_root=live), str(isolation_check)],
                root,
                base_env,
            )
        )

    python_targets = _python_targets(root, changed)
    if python_targets:
        label = "pytest " + " ".join(python_targets)
        command = [
            _python_bin(root, live_root=live),
            "-m",
            "pytest",
            *python_targets,
            "-q",
            "-p",
            "no:cacheprovider",
        ]
        env = dict(base_env)
        if root.resolve() != live:
            env["PYTHONPATH"] = str(root) + (
                f":{env['PYTHONPATH']}" if env.get("PYTHONPATH") else ""
            )
            env["FRAMEWORK_INFRASTRUCTURE__CUSTOM_ADDONS_DIR"] = str(root / "addons")
            command.extend(["--import-mode=importlib"])
        checks.append((label, command, root, env))

    if _gui_touched(changed):
        gui_root = root / GUI_DIR
        npm = shutil.which("npm")
        if npm and _ensure_gui_node_modules(root, live):
            gui_targets = _gui_targets(root, changed)
            if gui_targets is None:
                checks.append(
                    (
                        "npm test (vitest run)",
                        [npm, "test", "--silent"],
                        gui_root,
                        base_env,
                    )
                )
            elif gui_targets:
                # Vitest runs with cwd=gui_root; repo-relative filters like
                # ``framework/addons/…/gui/tests`` do not match its include
                # globs. Absolute paths do (see vite.config.js include).
                vitest_filters = [
                    str((root / target).resolve()) for target in gui_targets
                ]
                label = "npm test (vitest run) " + " ".join(gui_targets)
                checks.append(
                    (
                        label,
                        [npm, "test", "--silent", "--", *vitest_filters],
                        gui_root,
                        base_env,
                    )
                )

    return checks


def _ensure_gui_node_modules(checkout: Path, live_root: Path) -> bool:
    """Ensure the GUI runtime can resolve deps, symlinking from live when needed."""
    target = checkout / GUI_DIR / "node_modules"
    if target.is_dir():
        return True
    source = live_root / GUI_DIR / "node_modules"
    if not source.is_dir():
        return False
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink() or target.exists():
            target.unlink()
        target.symlink_to(source)
    except OSError:
        return False
    return target.is_dir()


def _python_targets(root: Path, changed: list[str]) -> list[str]:
    """Map changed Python files to the smallest existing pytest targets."""
    targets: set[str] = set()
    for path in changed:
        if not path.endswith(".py") or _is_generated(path):
            continue
        if not path.startswith(PYTHON_ROOTS):
            continue
        if "/tests/" in path or path.startswith("tests/"):
            if (root / path).is_file():
                targets.add(path)
            continue
        runtime_owner = _runtime_test_dir(path)
        if runtime_owner and (root / runtime_owner).is_dir():
            targets.add(runtime_owner)
            continue
        owner = _owner_test_dir(path)
        if owner and (root / owner).is_dir():
            targets.add(owner)
    return sorted(targets)


def _custom_addon_runtime_prefix(path: str) -> tuple[str, str] | None:
    """Return ``(addon_prefix, runtime)`` for a custom-addon runtime path.

    Supports flat ``addons/<leaf>/<runtime>/…`` and one-level operator buckets
    ``addons/<bucket>/<leaf>/<runtime>/…``.
    """
    parts = path.split("/")
    if parts[0] != "addons":
        return None
    if len(parts) >= 3 and parts[2] in RUNTIME_DIRS:
        return f"addons/{parts[1]}", parts[2]
    if len(parts) >= 4 and parts[3] in RUNTIME_DIRS:
        return f"addons/{parts[1]}/{parts[2]}", parts[3]
    return None


def _runtime_test_dir(path: str) -> str | None:
    """Map an addon's runtime subtree to that runtime's own test directory."""
    parts = path.split("/")
    custom = _custom_addon_runtime_prefix(path)
    if custom is not None:
        prefix, runtime = custom
        return f"{prefix}/{runtime}/tests"
    if (
        parts[:2] == ["framework", "addons"]
        and len(parts) >= 5
        and parts[3] in RUNTIME_DIRS
    ):
        return f"framework/addons/{parts[2]}/{parts[3]}/tests"
    return None


def _owner_test_dir(path: str) -> str | None:
    parts = path.split("/")
    if parts[0] == "scripts":
        return "scripts/tests"
    custom = _custom_addon_runtime_prefix(path)
    if custom is not None:
        prefix, _runtime = custom
        return f"{prefix}/api/tests"
    if parts[0] == "addons" and len(parts) >= 2:
        # Non-runtime paths under a leaf or bucket/leaf (for example manifest).
        if len(parts) >= 3 and parts[2] not in RUNTIME_DIRS:
            return f"addons/{parts[1]}/{parts[2]}/api/tests"
        return f"addons/{parts[1]}/api/tests"
    if parts[:2] == ["framework", "runtimes"] and len(parts) >= 3:
        return f"framework/runtimes/{parts[2]}/tests"
    if parts[:2] == ["framework", "addons"] and len(parts) >= 3:
        return f"framework/addons/{parts[2]}/api/tests"
    if parts[0] == "framework" and len(parts) >= 2:
        return f"framework/{parts[1]}/tests"
    return None


def _gui_touched(changed: list[str]) -> bool:
    for path in changed:
        if not path.endswith(GUI_SUFFIXES) or _is_generated(path):
            continue
        if path.startswith(f"{GUI_DIR}/") or "/gui/" in path:
            return True
    return False


def _gui_targets(root: Path, changed: list[str]) -> list[str] | None:
    """Map changed GUI files to the smallest vitest path filters.

    Returns:
        ``None`` when framework GUI runtime source changed (full suite).
        A sorted list of addon ``gui/tests`` paths (or concrete test files)
        when only addon GUI was touched. An empty list when nothing has an
        owner test directory.
    """
    filters: set[str] = set()
    framework_gui_changed = False
    for path in changed:
        if not path.endswith(GUI_SUFFIXES) or _is_generated(path):
            continue
        if path.startswith(f"{GUI_DIR}/"):
            framework_gui_changed = True
            continue
        if "/gui/" not in path:
            continue
        if "/gui/tests/" in path and (root / path).is_file():
            filters.add(path)
            continue
        runtime_owner = _runtime_test_dir(path)
        if runtime_owner and (root / runtime_owner).is_dir():
            filters.add(runtime_owner)
    if framework_gui_changed:
        return None
    return sorted(filters)


def verification_followup(label: str, result: subprocess.CompletedProcess) -> str:
    output = f"{result.stdout}\n{result.stderr}".strip()
    if len(output) > OUTPUT_TAIL_CHARS:
        output = "...\n" + output[-OUTPUT_TAIL_CHARS:]
    return (
        f"Verification gate: `{label}` failed after the files changed this turn.\n\n"
        f"```\n{output}\n```\n\n"
        "Phase 8 of the code-workflow skill: classify this as a local failure "
        "or a structural one, fix it, then re-run the command. If the same "
        "failure repeats, stop and report blocked rather than working around it."
    )


def quality_reminder(record: dict, changed: list[str]) -> str | None:
    """Ask for the deslop suite once a conversation crosses the file threshold.

    Callers must mark ``deslop_announced`` when this returns a message so the
    nudge cannot re-fire every subsequent stop.
    """
    if record["deslop_announced"]:
        return None
    source = sorted({path for path in changed if _is_source(path)})
    if len(source) < QUALITY_FILE_THRESHOLD:
        return None
    listed = "\n".join(f"- {path}" for path in source[:LISTED_FILES])
    if len(source) > LISTED_FILES:
        listed += f"\n- ... and {len(source) - LISTED_FILES} more"
    return (
        f"Quality gate: this conversation has changed {len(source)} source files "
        "without running the deslop suite.\n\n"
        f"{listed}\n\n"
        "Phase 9 of the code-workflow skill: run "
        "the deslop suite per `code-deslop` on that scope, "
        "then any quality gates selected in the technical plan. Re-verify "
        "anything the cleanup changes. If the suite genuinely does not apply "
        "here, say why in one line and stop."
    )


def emit(followup: str | None = None) -> None:
    """Emit Cursor's stop-hook response shape.

    Args:
        followup: Optional follow-up message that blocks the turn when set.
    """
    if not followup:
        print("{}")
    else:
        print(json.dumps({"followup_message": followup}))


def _clear_unverified(record: dict) -> None:
    record["unverified"] = []
    for worktree in (record.get("worktrees") or {}).values():
        if isinstance(worktree, dict):
            worktree["unverified"] = []


def _turn_finished(event: dict[str, object]) -> bool:
    """Return whether the event represents a completed Cursor turn.

    Args:
        event: Normalized stop-hook payload.

    Returns:
        True when Cursor reports ``status == completed``.
    """
    return event.get("status") == "completed"


def _already_looping(event: dict[str, object]) -> bool:
    """Return whether Cursor is already handling a stop-hook follow-up.

    Args:
        event: Normalized stop-hook payload.

    Returns:
        True when ``loop_count`` has reached the configured maximum.
    """
    try:
        return int(event.get("loop_count") or 0) >= MAX_FOLLOWUPS
    except (TypeError, ValueError):
        return False


def _mark_deslop_announced(record: dict[str, object]) -> None:
    """Mark the quality suite as announced for this conversation."""
    record["deslop_announced"] = True


def _python_bin(root: Path, *, live_root: Path | None = None) -> str:
    for candidate in (root, live_root):
        if candidate is None:
            continue
        venv = candidate / ".venv" / "bin" / "python3"
        if venv.is_file():
            return str(venv)
    return shutil.which("python3") or sys.executable


def _is_generated(path: str) -> bool:
    return any(marker in path for marker in GENERATED_MARKERS)


def _is_source(path: str) -> bool:
    if _is_generated(path):
        return False
    return path.endswith(SOURCE_SUFFIXES)


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 - the gate must never wedge a conversation
        print("{}")
    raise SystemExit(0)
