#!/usr/bin/env python3
"""Sync canonical ``.cursor`` project policy to Claude, Copilot, and Codex.

Edit durable guidance under ``AGENTS.md`` and ``.cursor/`` only, then run this
script so host mirrors stay aligned. Scope is the open git repository root —
never user-home IDE trees.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import yaml

from policy_config import load_policy_config
from policy_hosts import (
    CANONICAL_HOST,
    HOST_CLAUDE,
    HOST_CODEX,
    HOST_COPILOT,
    SYNC_MARKER,
    SYNC_MARKER_HTML,
    policy_present,
    resolve_repo_root,
)

FRONTMATTER_FENCE = "---"
COPILOT_STANDING = f"""{SYNC_MARKER_HTML}
# Repository instructions

Follow `AGENTS.md` at the repository root for standing agent guidance.
Path-specific instructions under `.github/instructions/` are synced from
`.cursor/rules/` by `global-policy-evolution`. Edit the canonical Cursor tree
(and `AGENTS.md`), then re-run sync — do not hand-edit generated mirrors.
"""

CLAUDE_STANDING = f"""{SYNC_MARKER_HTML}
@AGENTS.md
"""


@dataclass
class SyncResult:
    """Outcome of a policy sync run."""

    wrote: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def sync_repository(
    root: Path,
    *,
    dry_run: bool = False,
    check: bool = False,
) -> SyncResult:
    """Propagate canonical Cursor policy into enabled host mirrors.

    Args:
        root: Repository root (resolved to git root when present).
        dry_run: When True, report planned writes without mutating disk.
        check: When True, fail if mirrors would change (drift detection).

    Returns:
        Lists of wrote/removed/skipped paths and any errors.
    """
    result = SyncResult()
    root = resolve_repo_root(root)
    try:
        config = load_policy_config(root)
    except Exception as exc:  # noqa: BLE001
        result.errors.append(f"Invalid policy config: {exc}")
        return result

    if not config["syncEnabled"]:
        result.skipped.append("syncEnabled=false")
        return result

    hosts = set(config["enabledHosts"])
    if CANONICAL_HOST not in hosts:
        result.errors.append("enabledHosts must include cursor")
        return result

    if not (root / ".cursor").is_dir() and not (root / "AGENTS.md").is_file():
        if not policy_present(root):
            result.skipped.append("no project policy trees present")
            return result

    if HOST_CLAUDE in hosts:
        _sync_standing_doc(
            root,
            relative="CLAUDE.md",
            content=CLAUDE_STANDING,
            result=result,
            dry_run=dry_run,
            check=check,
            require_agents=True,
        )
    if HOST_COPILOT in hosts:
        _sync_standing_doc(
            root,
            relative=".github/copilot-instructions.md",
            content=COPILOT_STANDING,
            result=result,
            dry_run=dry_run,
            check=check,
            require_agents=True,
        )

    cursor_rules = root / ".cursor" / "rules"
    if cursor_rules.is_dir():
        if HOST_CLAUDE in hosts:
            _sync_rules_to_claude(root, cursor_rules, result, dry_run, check)
        if HOST_COPILOT in hosts:
            _sync_rules_to_copilot(root, cursor_rules, result, dry_run, check)

    cursor_skills = root / ".cursor" / "skills"
    if cursor_skills.is_dir():
        if HOST_CLAUDE in hosts:
            _sync_skill_tree(
                root,
                cursor_skills,
                root / ".claude" / "skills",
                result,
                dry_run,
                check,
            )
        if HOST_CODEX in hosts:
            _sync_skill_tree(
                root,
                cursor_skills,
                root / ".agents" / "skills",
                result,
                dry_run,
                check,
            )

    cursor_agents = root / ".cursor" / "agents"
    if cursor_agents.is_dir() and HOST_CLAUDE in hosts:
        _sync_agents_to_claude(root, cursor_agents, result, dry_run, check)

    if check and (result.wrote or result.removed):
        result.errors.append(
            "policy mirrors are out of date; run sync_policy.py without --check"
        )
    return result


def _sync_standing_doc(
    root: Path,
    *,
    relative: str,
    content: str,
    result: SyncResult,
    dry_run: bool,
    check: bool,
    require_agents: bool,
) -> None:
    if require_agents and not (root / "AGENTS.md").is_file():
        result.skipped.append(f"{relative} (AGENTS.md missing)")
        return
    path = root / relative
    if path.is_file() and not _is_managed(path):
        result.skipped.append(f"{relative} (unmanaged existing file)")
        return
    desired = content if content.endswith("\n") else content + "\n"
    _write_text(root, path, desired, result, dry_run, check)


def _sync_rules_to_claude(
    root: Path,
    cursor_rules: Path,
    result: SyncResult,
    dry_run: bool,
    check: bool,
) -> None:
    target_dir = root / ".claude" / "rules"
    expected: set[str] = set()
    for source in sorted(cursor_rules.glob("*.mdc")):
        if source.is_symlink():
            result.errors.append(f"skip symlink rule: {source.relative_to(root)}")
            continue
        stem = source.stem
        expected.add(stem)
        body = _cursor_rule_to_claude(source.read_text(encoding="utf-8"), stem)
        _write_text(
            root,
            target_dir / f"{stem}.md",
            body,
            result,
            dry_run,
            check,
        )
    _prune_generated(
        root,
        target_dir,
        keep_stems=expected,
        suffix=".md",
        result=result,
        dry_run=dry_run,
        check=check,
    )


def _sync_rules_to_copilot(
    root: Path,
    cursor_rules: Path,
    result: SyncResult,
    dry_run: bool,
    check: bool,
) -> None:
    target_dir = root / ".github" / "instructions"
    expected: set[str] = set()
    for source in sorted(cursor_rules.glob("*.mdc")):
        if source.is_symlink():
            result.errors.append(f"skip symlink rule: {source.relative_to(root)}")
            continue
        stem = source.stem
        expected.add(stem)
        body = _cursor_rule_to_copilot(source.read_text(encoding="utf-8"), stem)
        _write_text(
            root,
            target_dir / f"{stem}.instructions.md",
            body,
            result,
            dry_run,
            check,
        )
    _prune_generated(
        root,
        target_dir,
        keep_stems=expected,
        suffix=".instructions.md",
        result=result,
        dry_run=dry_run,
        check=check,
    )


def _sync_skill_tree(
    root: Path,
    source_skills: Path,
    target_skills: Path,
    result: SyncResult,
    dry_run: bool,
    check: bool,
) -> None:
    expected: set[str] = set()
    for skill_dir in sorted(p for p in source_skills.iterdir() if p.is_dir()):
        if skill_dir.is_symlink():
            result.errors.append(
                f"skip symlink skill: {skill_dir.relative_to(root).as_posix()}"
            )
            continue
        if not (skill_dir / "SKILL.md").is_file():
            continue
        expected.add(skill_dir.name)
        dest = target_skills / skill_dir.name
        _mirror_directory(root, skill_dir, dest, result, dry_run, check)

    if target_skills.is_dir():
        for existing in sorted(p for p in target_skills.iterdir() if p.is_dir()):
            if existing.name in expected:
                continue
            if not (existing / "SKILL.md").is_file():
                continue
            relative = existing.relative_to(root).as_posix()
            if check or dry_run:
                result.removed.append(relative)
            else:
                shutil.rmtree(existing)
                result.removed.append(relative)


def _sync_agents_to_claude(
    root: Path,
    cursor_agents: Path,
    result: SyncResult,
    dry_run: bool,
    check: bool,
) -> None:
    target_dir = root / ".claude" / "agents"
    expected: set[str] = set()
    for source in sorted(cursor_agents.glob("*.md")):
        if source.is_symlink():
            result.errors.append(f"skip symlink agent: {source.relative_to(root)}")
            continue
        stem = source.stem
        expected.add(stem)
        body = _cursor_agent_to_claude(source.read_text(encoding="utf-8"), stem)
        _write_text(
            root,
            target_dir / f"{stem}.md",
            body,
            result,
            dry_run,
            check,
        )
    _prune_generated(
        root,
        target_dir,
        keep_stems=expected,
        suffix=".md",
        result=result,
        dry_run=dry_run,
        check=check,
    )


def _cursor_rule_to_claude(text: str, stem: str) -> str:
    metadata, body = _split_frontmatter(text)
    description = metadata.get("description")
    always_apply = bool(metadata.get("alwaysApply", False))
    globs = metadata.get("globs")
    claude_meta: dict[str, object] = {}
    if isinstance(description, str) and description.strip():
        claude_meta["description"] = description.strip()
    if not always_apply:
        paths = _globs_to_list(globs)
        if paths:
            claude_meta["paths"] = paths
    rendered = _render_frontmatter(claude_meta)
    header = (
        f"{SYNC_MARKER_HTML}\n"
        f"<!-- canonical: .cursor/rules/{stem}.mdc -->\n"
    )
    return header + rendered + body.lstrip("\n")


def _cursor_rule_to_copilot(text: str, stem: str) -> str:
    metadata, body = _split_frontmatter(text)
    always_apply = bool(metadata.get("alwaysApply", False))
    globs = metadata.get("globs")
    if always_apply:
        apply_to = "**"
    else:
        paths = _globs_to_list(globs)
        apply_to = ", ".join(paths) if paths else "**"
    copilot_meta = {"applyTo": apply_to}
    description = metadata.get("description")
    if isinstance(description, str) and description.strip():
        # Copilot ignores unknown keys; keep description for humans/sync.
        copilot_meta["description"] = description.strip()
    rendered = _render_frontmatter(copilot_meta)
    header = (
        f"{SYNC_MARKER_HTML}\n"
        f"<!-- canonical: .cursor/rules/{stem}.mdc -->\n"
    )
    return header + rendered + body.lstrip("\n")


def _cursor_agent_to_claude(text: str, stem: str) -> str:
    metadata, body = _split_frontmatter(text)
    claude_meta: dict[str, object] = {}
    name = metadata.get("name")
    description = metadata.get("description")
    if isinstance(name, str) and name.strip():
        claude_meta["name"] = name.strip()
    elif stem:
        claude_meta["name"] = stem
    if isinstance(description, str) and description.strip():
        claude_meta["description"] = description.strip()
    rendered = _render_frontmatter(claude_meta)
    header = (
        f"{SYNC_MARKER_HTML}\n"
        f"<!-- canonical: .cursor/agents/{stem}.md -->\n"
    )
    return header + rendered + body.lstrip("\n")


def _globs_to_list(globs: object) -> list[str]:
    if globs is None or globs == "":
        return []
    if isinstance(globs, str):
        text = globs.strip()
        if text.startswith("{") and text.endswith("}"):
            inner = text[1:-1]
            return [part.strip() for part in inner.split(",") if part.strip()]
        if "," in text and not text.startswith("{"):
            return [part.strip() for part in text.split(",") if part.strip()]
        return [text]
    if isinstance(globs, list):
        return [str(item).strip() for item in globs if str(item).strip()]
    return [str(globs)]


def _split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        return {}, text
    closing = next(
        (
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == FRONTMATTER_FENCE
        ),
        None,
    )
    if closing is None:
        return {}, text
    block = "\n".join(lines[1:closing])
    try:
        loaded = yaml.safe_load(block) or {}
    except yaml.YAMLError:
        loaded = {}
    if not isinstance(loaded, dict):
        loaded = {}
    body = "\n".join(lines[closing + 1 :])
    if body and not body.startswith("\n"):
        body = "\n" + body
    if body and not body.endswith("\n"):
        body += "\n"
    return dict(loaded), body


def _render_frontmatter(metadata: dict[str, object]) -> str:
    if not metadata:
        return f"{FRONTMATTER_FENCE}\n{FRONTMATTER_FENCE}\n"
    dumped = yaml.safe_dump(
        metadata,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    ).rstrip()
    return f"{FRONTMATTER_FENCE}\n{dumped}\n{FRONTMATTER_FENCE}\n"


def _is_managed(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return SYNC_MARKER in text


def _write_text(
    root: Path,
    path: Path,
    content: str,
    result: SyncResult,
    dry_run: bool,
    check: bool,
) -> None:
    relative = path.relative_to(root).as_posix()
    if path.is_file():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return
    if check or dry_run:
        result.wrote.append(relative)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    result.wrote.append(relative)


def _mirror_directory(
    root: Path,
    source: Path,
    dest: Path,
    result: SyncResult,
    dry_run: bool,
    check: bool,
) -> None:
    relative = dest.relative_to(root).as_posix()
    if dest.exists() and _dirs_equal(source, dest):
        return
    if check or dry_run:
        result.wrote.append(relative)
        return
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest, symlinks=False)
    result.wrote.append(relative)


def _dirs_equal(left: Path, right: Path) -> bool:
    left_files = {
        p.relative_to(left).as_posix(): p.read_bytes()
        for p in left.rglob("*")
        if p.is_file() and not p.is_symlink()
    }
    right_files = {
        p.relative_to(right).as_posix(): p.read_bytes()
        for p in right.rglob("*")
        if p.is_file() and not p.is_symlink()
    }
    return left_files == right_files


def _prune_generated(
    root: Path,
    target_dir: Path,
    *,
    keep_stems: set[str],
    suffix: str,
    result: SyncResult,
    dry_run: bool,
    check: bool,
) -> None:
    if not target_dir.is_dir():
        return
    for path in sorted(target_dir.glob(f"*{suffix}")):
        if not path.is_file():
            continue
        stem = path.name[: -len(suffix)] if suffix else path.stem
        if stem in keep_stems:
            continue
        if not _is_managed(path):
            continue
        relative = path.relative_to(root).as_posix()
        if check or dry_run:
            result.removed.append(relative)
        else:
            path.unlink()
            result.removed.append(relative)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Sync canonical .cursor project policy to Claude, Copilot, and Codex"
        )
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report planned writes without changing files",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero when mirrors would change (drift)",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    result = sync_repository(root, dry_run=args.dry_run, check=args.check)
    for path in result.wrote:
        print(f"WRITE: {path}")
    for path in result.removed:
        print(f"REMOVE: {path}")
    for path in result.skipped:
        print(f"SKIP: {path}")
    for message in result.errors:
        print(f"ERROR: {message}")
    if result.ok:
        print(
            f"OK: {len(result.wrote)} write(s), {len(result.removed)} remove(s), "
            f"{len(result.skipped)} skip(s)"
        )
        return 0
    print(f"FAILED: {len(result.errors)} error(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
