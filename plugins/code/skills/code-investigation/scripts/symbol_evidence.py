#!/usr/bin/env python3
"""Collect bounded, categorized evidence for a symbol or distinctive literal."""

from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import IO, Sequence

CATEGORY_ORDER = ("definitions", "tests", "wiring", "documentation", "references")
CATEGORY_TITLES = {
    "definitions": "Likely definitions",
    "tests": "Test references",
    "wiring": "Likely runtime wiring",
    "documentation": "Documentation references",
    "references": "Other references",
}
DEFAULT_EXCLUDE_GLOBS = ("!.git/**",)
WIRING_TERMS = {
    "api",
    "blueprint",
    "config",
    "docker",
    "jobs",
    "manifest",
    "migration",
    "migrations",
    "registry",
    "routes",
    "settings",
    "tasks",
    "urls",
    "worker",
}
DEFINITION_PREFIXES = (
    "class",
    "const",
    "def",
    "enum",
    "function",
    "interface",
    "let",
    "struct",
    "trait",
    "type",
    "var",
)
MAX_SOURCE_COLUMNS = 500
MAX_DISPLAY_COLUMNS = 240


def _run(command: Sequence[str], root: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        return subprocess.CompletedProcess(command, 127, "", str(error))


def _require_rg() -> str:
    executable = shutil.which("rg")
    if not executable:
        raise RuntimeError("ripgrep (rg) is required but was not found on PATH")
    return executable


def _append_globs(command: list[str], globs: Sequence[str]) -> None:
    for glob in (*DEFAULT_EXCLUDE_GLOBS, *globs):
        command.extend(["--glob", glob])


def _rg_command(
    executable: str,
    query: str,
    regex: bool,
    word: bool,
    globs: Sequence[str],
) -> list[str]:
    command = [
        executable,
        "--json",
        "--line-number",
        "--color",
        "never",
        "--smart-case",
        "--hidden",
        "--max-columns",
        str(MAX_SOURCE_COLUMNS),
        "--max-columns-preview",
    ]
    if not regex:
        command.append("--fixed-strings")
    if word:
        command.append("--word-regexp")
    _append_globs(command, globs)
    command.extend(["--", query, "."])
    return command


def _decode_rg_value(value: dict[str, str]) -> str:
    if "text" in value:
        return value["text"]
    encoded = value.get("bytes")
    if not encoded:
        return ""
    return base64.b64decode(encoded).decode("utf-8", errors="replace")


def _safe_excerpt(text: str) -> str:
    printable = "".join(
        character if character.isprintable() or character == "\t" else " "
        for character in text
    ).strip()
    if len(printable) > MAX_DISPLAY_COLUMNS:
        printable = f"{printable[: MAX_DISPLAY_COLUMNS - 1]}…"
    return (
        printable.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _parse_match(raw_line: str) -> dict[str, object] | None:
    event = json.loads(raw_line)
    if event.get("type") != "match":
        return None
    data = event["data"]
    path = _decode_rg_value(data["path"]).removeprefix("./")
    text = _decode_rg_value(data["lines"]).rstrip("\r\n")
    return {
        "path": path,
        "line": data["line_number"],
        "text": _safe_excerpt(text),
    }


def _terminate(process: subprocess.Popen[str]) -> None:
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def _collect_stream(
    process: subprocess.Popen[str],
    stdout: IO[str],
    max_matches: int,
) -> tuple[list[dict[str, object]], bool]:
    matches: list[dict[str, object]] = []
    for raw_line in stdout:
        match = _parse_match(raw_line)
        if match is None:
            continue
        matches.append(match)
        if len(matches) > max_matches:
            _terminate(process)
            return matches[:max_matches], True
    return matches, False


def search_matches(
    root: Path,
    query: str,
    *,
    regex: bool = False,
    word: bool = False,
    globs: Sequence[str] = (),
    max_matches: int = 500,
) -> tuple[list[dict[str, object]], bool]:
    """Search content with a global match bound.

    Returns:
        A pair containing collected matches and whether collection was truncated.

    Raises:
        RuntimeError: If ripgrep is unavailable or the search fails.
    """
    executable = _require_rg()
    command = _rg_command(executable, query, regex, word, globs)
    try:
        with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as error_stream:
            with subprocess.Popen(
                command,
                cwd=root,
                stdout=subprocess.PIPE,
                stderr=error_stream,
                text=True,
            ) as process:
                if process.stdout is None:
                    _terminate(process)
                    raise RuntimeError("Unable to capture ripgrep output")

                matches, truncated = _collect_stream(
                    process,
                    process.stdout,
                    max_matches,
                )
                if truncated:
                    return matches, True

                return_code = process.wait()
                error_stream.seek(0)
                stderr = error_stream.read().strip()
    except OSError as error:
        raise RuntimeError(f"Unable to start ripgrep: {error}") from error

    if return_code not in {0, 1}:
        raise RuntimeError(stderr or f"ripgrep exited with status {return_code}")
    return matches, False


def _looks_like_definition(text: str, query: str, regex: bool) -> bool:
    if regex:
        return False
    escaped = re.escape(query)
    prefixes = "|".join(DEFINITION_PREFIXES)
    patterns = (
        rf"\b(?:{prefixes})\s+{escaped}\b",
        rf"\b{escaped}\s*(?::[^=]+)?=",
        rf"\b{escaped}\s*:\s*(?:class|interface|type)\b",
    )
    return any(re.search(pattern, text) for pattern in patterns)


def _is_test(path: PurePosixPath) -> bool:
    name = path.name.lower()
    return (
        bool({"test", "tests", "__tests__"} & set(path.parts))
        or name.startswith("test_")
        or ".test." in name
        or ".spec." in name
    )


def _is_documentation(path: PurePosixPath) -> bool:
    return (
        "docs" in path.parts
        or path.name.startswith("README")
        or path.suffix.lower() in {".md", ".mdx", ".rst"}
    )


def _is_wiring(path: PurePosixPath, text: str) -> bool:
    path_terms = {part.lower() for part in path.parts}
    text_lower = text.lower()
    return bool(path_terms & WIRING_TERMS) or any(
        marker in text_lower
        for marker in (
            "register(",
            "register_blueprint",
            "route(",
            "add_url_rule",
            "import_module",
            "entry_points",
        )
    )


def categorize_matches(
    matches: Sequence[dict[str, object]],
    query: str,
    *,
    regex: bool = False,
) -> dict[str, list[dict[str, object]]]:
    """Group matches into heuristic investigative roles."""
    categorized: dict[str, list[dict[str, object]]] = defaultdict(list)
    for match in matches:
        path = PurePosixPath(str(match["path"]))
        text = str(match["text"])
        if _is_test(path):
            category = "tests"
        elif _is_documentation(path):
            category = "documentation"
        elif _looks_like_definition(text, query, regex):
            category = "definitions"
        elif _is_wiring(path, text):
            category = "wiring"
        else:
            category = "references"
        categorized[category].append(match)
    return {category: categorized.get(category, []) for category in CATEGORY_ORDER}


def filename_matches(
    root: Path,
    query: str,
    globs: Sequence[str],
    limit: int,
) -> dict[str, object]:
    """Return scoped files whose paths contain the literal query."""
    command = [_require_rg(), "--files", "--hidden"]
    _append_globs(command, globs)
    result = _run(command, root)
    if result.returncode != 0:
        return {
            "available": False,
            "entries": [],
            "error": result.stderr.strip() or "ripgrep file listing failed",
        }
    needle = query.casefold()
    values = sorted(
        path for path in result.stdout.splitlines() if needle in path.casefold()
    )
    return {
        "available": True,
        "entries": values[:limit],
        "truncated": len(values) > limit,
    }


def history_matches(root: Path, query: str, limit: int) -> dict[str, object]:
    """Return commits that added or removed the literal query."""
    result = _run(
        ["git", "log", f"-S{query}", "--oneline", f"--max-count={limit}", "--all"],
        root,
    )
    if result.returncode != 0:
        return {
            "requested": True,
            "available": False,
            "entries": [],
            "error": result.stderr.strip() or "git history unavailable",
        }
    return {
        "requested": True,
        "available": True,
        "entries": result.stdout.splitlines(),
    }


def build_report(
    root: Path,
    query: str,
    *,
    regex: bool = False,
    word: bool = False,
    globs: Sequence[str] = (),
    limit: int = 20,
    max_matches: int = 500,
    include_history: bool = False,
) -> dict[str, object]:
    """Build a bounded, categorized evidence report for a query."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Repository root is not a directory: {root}")

    matches, search_truncated = search_matches(
        root,
        query,
        regex=regex,
        word=word,
        globs=globs,
        max_matches=max_matches,
    )
    categorized = categorize_matches(matches, query, regex=regex)
    categories_truncated = any(len(values) > limit for values in categorized.values())
    limited = {
        category: category_matches[:limit]
        for category, category_matches in categorized.items()
    }
    filenames = (
        {"applicable": False, "reason": "disabled for regex queries"}
        if regex
        else {
            "applicable": True,
            **filename_matches(root, query, globs, limit),
        }
    )
    history = (
        history_matches(root, query, limit)
        if include_history
        else {"requested": False}
    )
    return {
        "root": str(root),
        "query": query,
        "collected_match_count": len(matches),
        "search_truncated": search_truncated,
        "filename_matches": filenames,
        "categories": limited,
        "categories_truncated": categories_truncated,
        "history": history,
        "classification": "heuristic; verify by reading source files",
    }


def _format_filenames(status: dict[str, object]) -> list[str]:
    if not status["applicable"]:
        return [f"- Not applicable: {status['reason']}"]
    if not status["available"]:
        return [f"- Unavailable: {status['error']}"]
    entries = status["entries"]
    lines = [f"- `{path}`" for path in entries] or ["- None found"]
    if status.get("truncated"):
        lines.append("- Additional filename matches omitted")
    return lines


def format_code-markdown(report: dict[str, object]) -> str:
    """Format categorized evidence as concise Markdown."""
    count_suffix = "+" if report["search_truncated"] else ""
    lines = [
        "# Symbol evidence",
        f"- Query: `{report['query']}`",
        f"- Root: `{report['root']}`",
        f"- Content matches collected: {report['collected_match_count']}{count_suffix}",
        f"- Classification: {report['classification']}",
    ]
    if report["search_truncated"]:
        lines.append("- Search collection hit its safety bound; absence is not established.")
    if report["categories_truncated"]:
        lines.append("- Some categories were truncated; narrow the query or add globs.")

    lines.append("\n## Filename matches")
    lines.extend(_format_filenames(report["filename_matches"]))

    for category in CATEGORY_ORDER:
        lines.append(f"\n## {CATEGORY_TITLES[category]}")
        values = report["categories"][category]
        lines.extend(
            f"- `{item['path']}:{item['line']}` — {item['text']}" for item in values
        )
        if not values:
            lines.append("- None found in collected matches")

    history = report["history"]
    if history["requested"]:
        lines.append("\n## History")
        if not history["available"]:
            lines.append(f"- Unavailable: {history['error']}")
        else:
            entries = history["entries"]
            lines.extend(f"- `{entry}`" for entry in entries)
            if not entries:
                lines.append("- No matching commits found")
    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find definitions, references, tests, and runtime wiring."
    )
    parser.add_argument("query", help="Exact symbol or distinctive literal")
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument("--regex", action="store_true", help="Treat query as regex")
    parser.add_argument("--word", action="store_true", help="Match whole words")
    parser.add_argument(
        "--glob",
        action="append",
        default=[],
        help="Restrict content and filename results; repeat as needed",
    )
    parser.add_argument("--history", action="store_true", help="Include git -S history")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--limit", type=int, default=20, help="Entries per category")
    parser.add_argument(
        "--max-matches",
        type=int,
        default=500,
        help="Global content-match safety bound (default: 500)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.limit < 1 or args.max_matches < 1:
        print("--limit and --max-matches must be at least 1", file=sys.stderr)
        return 2

    try:
        report = build_report(
            Path(args.root),
            args.query,
            regex=args.regex,
            word=args.word,
            globs=args.glob,
            limit=args.limit,
            max_matches=args.max_matches,
            include_history=args.history,
        )
    except (RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"Investigation search failed: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_code-markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
