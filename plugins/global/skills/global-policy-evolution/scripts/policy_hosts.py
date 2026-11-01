#!/usr/bin/env python3
"""Host layouts for repo-local multi-IDE project policy.

Policy is scoped to the open git repository root. User-home trees
(``~/.cursor``, ``~/.claude``, ``~/.codex``, ``~/.agents``) are never
project policy owners.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

HOST_CURSOR = "cursor"
HOST_CLAUDE = "claude"
HOST_COPILOT = "copilot"
HOST_CODEX = "codex"

ALL_HOSTS = (HOST_CURSOR, HOST_CLAUDE, HOST_COPILOT, HOST_CODEX)
CANONICAL_HOST = HOST_CURSOR

SYNC_MARKER = "policy-sync: managed"
SYNC_MARKER_HTML = f"<!-- {SYNC_MARKER} -->"


@dataclass(frozen=True)
class HostLayout:
    """Paths relative to a repository root for one coding host."""

    name: str
    rules_dir: str | None
    skills_dir: str | None
    agents_dir: str | None
    rule_suffix: str
    standing_docs: tuple[str, ...]


HOST_LAYOUTS: dict[str, HostLayout] = {
    HOST_CURSOR: HostLayout(
        name=HOST_CURSOR,
        rules_dir=".cursor/rules",
        skills_dir=".cursor/skills",
        agents_dir=".cursor/agents",
        rule_suffix=".mdc",
        standing_docs=("AGENTS.md",),
    ),
    HOST_CLAUDE: HostLayout(
        name=HOST_CLAUDE,
        rules_dir=".claude/rules",
        skills_dir=".claude/skills",
        agents_dir=".claude/agents",
        rule_suffix=".md",
        standing_docs=("CLAUDE.md", "AGENTS.md"),
    ),
    HOST_COPILOT: HostLayout(
        name=HOST_COPILOT,
        rules_dir=".github/instructions",
        skills_dir=None,
        agents_dir=None,
        rule_suffix=".instructions.md",
        standing_docs=("AGENTS.md", ".github/copilot-instructions.md"),
    ),
    HOST_CODEX: HostLayout(
        name=HOST_CODEX,
        rules_dir=None,
        skills_dir=".agents/skills",
        agents_dir=None,
        rule_suffix="",
        standing_docs=("AGENTS.md",),
    ),
}


def resolve_repo_root(path: Path) -> Path:
    """Resolve ``path`` to a git repository root when possible.

    Args:
        path: Candidate directory (usually the open workspace root).

    Returns:
        The nearest ancestor containing ``.git``, else ``path.resolve()``.
    """
    resolved = path.resolve()
    current = resolved if resolved.is_dir() else resolved.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return resolved


def policy_present(root: Path) -> bool:
    """Return True when the repo has any project-local policy surface."""
    root = root.resolve()
    if (root / "AGENTS.md").is_file() or (root / "CLAUDE.md").is_file():
        return True
    if (root / ".github" / "copilot-instructions.md").is_file():
        return True
    for layout in HOST_LAYOUTS.values():
        for relative in (layout.rules_dir, layout.skills_dir, layout.agents_dir):
            if relative and (root / relative).is_dir():
                return True
    return False


def cursor_hooks_dir(root: Path) -> Path:
    """Return the Cursor-only hooks directory (not synced)."""
    return root / ".cursor" / "hooks"


def policy_config_path(root: Path) -> Path:
    """Return the optional project policy overlay path."""
    return root / ".cursor" / "policy-config.json"
