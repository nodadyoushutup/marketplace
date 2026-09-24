#!/usr/bin/env python3
"""Produce a concise, deterministic map of a code repository."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

EXCLUDED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "vendor",
}

AGENT_SKILL_PREFIXES = (
    (".agents", "skills"),
    (".cursor", "skills"),
)

MANIFEST_NAMES = {
    "Cargo.toml",
    "Dockerfile",
    "Makefile",
    "Pipfile",
    "compose.code-yaml",
    "docker-compose.code-yaml",
    "package.json",
    "poetry.lock",
    "pyproject.toml",
    "requirements.txt",
    "setup.cfg",
    "setup.py",
    "uv.lock",
}

LANGUAGES = {
    ".c": "C",
    ".cpp": "C++",
    ".css": "CSS",
    ".go": "Go",
    ".code-html": "HTML",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript JSX",
    ".json": "JSON",
    ".kt": "Kotlin",
    ".md": "Markdown",
    ".php": "PHP",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".scss": "SCSS",
    ".sh": "Shell",
    ".sql": "SQL",
    ".tsx": "TypeScript JSX",
    ".ts": "TypeScript",
    ".code-yaml": "YAML",
    ".yml": "YAML",
}


def _run(command: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        return subprocess.CompletedProcess(command, 127, "", str(error))


def _git_files(root: Path) -> list[str] | None:
    result = _run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        root,
    )
    if result.returncode != 0:
        return None
    return sorted(path for path in result.stdout.split("\0") if path)


def _walk_files(root: Path) -> list[str]:
    files: list[str] = []
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            dirname for dirname in dirnames if dirname not in EXCLUDED_DIRS
        )
        current = Path(current_root)
        for filename in sorted(filenames):
            files.append((current / filename).relative_to(root).as_posix())
    return files


def _is_excluded(path: PurePosixPath) -> bool:
    return bool(set(path.parts) & EXCLUDED_DIRS) or (
        path.parts[:2] in AGENT_SKILL_PREFIXES
    )


def collect_inventory(root: Path) -> tuple[list[str], str]:
    """Return repository files and the collection method used."""
    git_files = _git_files(root)
    files = git_files if git_files is not None else _walk_files(root)
    mode = "git" if git_files is not None else "filesystem fallback"
    return [
        path
        for path in files
        if (root / path).is_file()
        and not _is_excluded(PurePosixPath(path))
    ], mode


def collect_files(root: Path) -> list[str]:
    """Return repository files while respecting Git ignores when available."""
    files, _ = collect_inventory(root)
    return files


def _is_test(path: PurePosixPath) -> bool:
    name = path.name.lower()
    return (
        "test" in path.parts
        or "tests" in path.parts
        or name.startswith("test_")
        or ".test." in name
        or ".spec." in name
    )


def _is_instruction(path: PurePosixPath) -> bool:
    return (
        path.name in {"AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md"}
        or path.parts[:2] in {(".cursor", "agents"), (".cursor", "rules")}
    )


def _is_manifest(path: PurePosixPath) -> bool:
    name = path.name
    return (
        name in MANIFEST_NAMES
        or name.startswith("requirements")
        or name.endswith(".lock")
        or name.startswith("Dockerfile")
    )


def _is_migration(path: PurePosixPath) -> bool:
    return bool({"migration", "migrations", "alembic", "versions"} & set(path.parts))


def _is_documentation(path: PurePosixPath) -> bool:
    return (
        "docs" in path.parts
        or path.name.startswith("README")
        or path.suffix.lower() in {".md", ".mdx", ".rst"}
    ) and path.parts[:1] != (".cursor",)


def _is_deployment(path: PurePosixPath) -> bool:
    return bool(
        {"deploy", "deployment", "docker", "infra", "k8s", "code-terraform"}
        & set(path.parts)
    ) or path.parts[:2] == (".github", "workflows")


def _sample(paths: Iterable[str], limit: int) -> list[str]:
    return sorted(paths)[:limit]


def _working_tree(root: Path, limit: int) -> dict[str, object]:
    result = _run(["git", "status", "--short"], root)
    if result.returncode != 0:
        return {
            "available": False,
            "entries": [],
            "error": result.stderr.strip() or "git status unavailable",
        }
    entries = result.stdout.splitlines()
    return {
        "available": True,
        "entries": entries[:limit],
        "truncated": len(entries) > limit,
    }


def build_snapshot(root: Path, limit: int = 12) -> dict[str, object]:
    """Build a compact repository snapshot suitable for agent context."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Repository root is not a directory: {root}")

    files, collection_mode = collect_inventory(root)
    paths = [PurePosixPath(path) for path in files]

    language_counts = Counter(
        LANGUAGES[path.suffix.lower()]
        for path in paths
        if path.suffix.lower() in LANGUAGES
    )
    top_level_counts = Counter(
        path.parts[0] if len(path.parts) > 1 else "(root)" for path in paths
    )

    categories = {
        "instructions": _sample(
            (str(path) for path in paths if _is_instruction(path)), limit
        ),
        "manifests": _sample(
            (str(path) for path in paths if _is_manifest(path)), limit
        ),
        "tests": _sample((str(path) for path in paths if _is_test(path)), limit),
        "migrations": _sample(
            (str(path) for path in paths if _is_migration(path)), limit
        ),
        "documentation": _sample(
            (str(path) for path in paths if _is_documentation(path)), limit
        ),
        "deployment": _sample(
            (str(path) for path in paths if _is_deployment(path)), limit
        ),
    }

    return {
        "root": str(root),
        "file_count": len(files),
        "collection_mode": collection_mode,
        "languages": dict(language_counts.most_common(limit)),
        "top_level": dict(top_level_counts.most_common(limit)),
        "categories": categories,
        "working_tree": _working_tree(root, limit),
    }


def _format_mapping(title: str, values: dict[str, int]) -> list[str]:
    lines = [f"## {title}"]
    lines.extend(f"- {name}: {count}" for name, count in values.items())
    return lines


def format_code-markdown(snapshot: dict[str, object]) -> str:
    """Format a repository snapshot as concise Markdown."""
    lines = [
        "# Repository map",
        f"- Root: `{snapshot['root']}`",
        f"- Files considered: {snapshot['file_count']}",
        f"- Collection: {snapshot['collection_mode']}",
        "",
    ]
    lines.extend(_format_mapping("Languages", snapshot["languages"]))
    lines.extend(["", *_format_mapping("Top-level areas", snapshot["top_level"])])

    categories = snapshot["categories"]
    for category, paths in categories.items():
        lines.extend(["", f"## {category.replace('_', ' ').title()}"])
        lines.extend(f"- `{path}`" for path in paths)
        if not paths:
            lines.append("- None found")

    lines.extend(["", "## Working tree"])
    working_tree = snapshot["working_tree"]
    if not working_tree["available"]:
        lines.append(f"- Unavailable: {working_tree['error']}")
    elif not working_tree["entries"]:
        lines.append("- Clean")
    else:
        lines.extend(f"- `{entry}`" for entry in working_tree["entries"])
        if working_tree.get("truncated"):
            lines.append("- Additional changes omitted")
    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a high-signal repository map for code investigation."
    )
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--limit",
        type=int,
        default=12,
        help="Maximum entries shown per section (default: 12)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    snapshot = build_snapshot(Path(args.root), args.limit)
    if args.json:
        print(json.dumps(snapshot, indent=2, sort_keys=True))
    else:
        print(format_code-markdown(snapshot))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
