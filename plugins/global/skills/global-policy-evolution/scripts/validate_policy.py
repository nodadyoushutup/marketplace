#!/usr/bin/env python3
"""Validate repo-local project policy across Cursor, Claude, Copilot, and Codex.

Canonical authoring lives under ``.cursor/`` plus root ``AGENTS.md``. Host
mirrors (``.claude/``, ``.github/instructions/``, ``.agents/skills/``,
``CLAUDE.md``, ``.github/copilot-instructions.md``) are validated when present.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

import yaml

from policy_config import load_policy_config
from policy_hosts import (
    HOST_CLAUDE,
    HOST_CODEX,
    HOST_COPILOT,
    HOST_CURSOR,
    HOST_LAYOUTS,
    policy_present,
    resolve_repo_root,
)

RULE_SOFT_ALWAYS_APPLY_LINES = 40
RULE_SOFT_GLOB_LINES = 50
SKILL_SOFT_LINES = 500
DESCRIPTION_MAX = 1024
NAME_MAX = 64
NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
SECRET_PATTERNS = (
    re.compile(
        r"(?i)\b(api[_-]?key|secret|password|token|access[_-]?key)\b\s*[:=]\s*"
        r"['\"]?[^'\"\s]{8,}"
    ),
    re.compile(r"(?i)\bx-api-key\b\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"(?i)-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9\-_\.=]{20,}"),
    re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
)
TEXT_SUFFIXES = {
    ".md",
    ".mdc",
    ".txt",
    ".py",
    ".sh",
    ".js",
    ".mjs",
    ".cjs",
    ".json",
    ".yaml",
    ".yml",
}
SECRET_SCAN_EXCLUDED_SUFFIXES = (
    "/scripts/tests/",
    "/EVALS.md",
)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_FENCE = "---"


@dataclass(frozen=True)
class Finding:
    severity: str
    path: str
    message: str


@dataclass
class ValidationResult:
    errors: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_repository(
    root: Path,
    *,
    changed_files: Sequence[str] | None = None,
) -> ValidationResult:
    """Validate project policy for every present enabled host tree.

    Args:
        root: Repository root (resolved to git root when present).
        changed_files: Optional repo-relative paths that limit which packages
            are validated. Promotion must leave this unset.

    Returns:
        Aggregated errors and warnings for the selected policy assets.
    """
    result = ValidationResult()
    root = resolve_repo_root(root)
    if not policy_present(root):
        result.errors.append(
            Finding(
                "error",
                ".",
                "No project policy found under this git root "
                "(expected AGENTS.md and/or .cursor/.claude/.agents/.github policy)",
            )
        )
        return result

    try:
        config = load_policy_config(root)
    except Exception as exc:  # noqa: BLE001
        result.errors.append(
            Finding(
                "error",
                ".cursor/policy-config.json",
                f"Invalid policy config: {exc}",
            )
        )
        return result

    selected = _normalize_changed(root, changed_files) if changed_files else None
    enabled = set(config["enabledHosts"])
    _validate_forbidden_policy_names(root, config["forbiddenPolicyNames"], result)

    if HOST_CURSOR in enabled:
        _validate_cursor_tree(root, selected, result)
    if HOST_CLAUDE in enabled:
        _validate_claude_tree(root, selected, result)
    if HOST_COPILOT in enabled:
        _validate_copilot_tree(root, selected, result)
    if HOST_CODEX in enabled:
        _validate_codex_tree(root, selected, result)

    for standing in ("AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md"):
        path = root / standing
        if path.is_file() and (selected is None or standing in selected):
            text = _read_text(path, standing, result)
            if text is not None:
                _scan_secrets(standing, text, result)
                _scan_markdown_links(root, path, text, result)

    return result


def _validate_forbidden_policy_names(
    root: Path,
    names: Sequence[str],
    result: ValidationResult,
) -> None:
    """Reject policy names forbidden by the repository overlay."""
    for name in sorted(names):
        candidates = (
            root / ".cursor" / "rules" / f"{name}.mdc",
            root / ".cursor" / "agents" / f"{name}.md",
            root / ".cursor" / "skills" / name,
            root / ".claude" / "rules" / f"{name}.md",
            root / ".claude" / "agents" / f"{name}.md",
            root / ".claude" / "skills" / name,
            root / ".agents" / "skills" / name,
            root / ".github" / "instructions" / f"{name}.instructions.md",
        )
        for path in candidates:
            if path.exists():
                result.errors.append(
                    Finding(
                        "error",
                        path.relative_to(root).as_posix(),
                        f"Policy name {name!r} is forbidden by repository config",
                    )
                )


def _validate_cursor_tree(
    root: Path,
    selected: set[str] | None,
    result: ValidationResult,
) -> None:
    layout = HOST_LAYOUTS[HOST_CURSOR]
    rules_dir = root / layout.rules_dir  # type: ignore[operator]
    agents_dir = root / layout.agents_dir  # type: ignore[operator]
    skills_dir = root / layout.skills_dir  # type: ignore[operator]
    if not rules_dir.is_dir() and not agents_dir.is_dir() and not skills_dir.is_dir():
        return

    if rules_dir.is_dir():
        for path in sorted(rules_dir.glob("*.mdc")):
            relative = path.relative_to(root).as_posix()
            if selected is not None and relative not in selected:
                continue
            _validate_cursor_rule(root, path, result)
    elif selected is None and (agents_dir.is_dir() or skills_dir.is_dir()):
        result.warnings.append(
            Finding("warning", ".cursor/rules", "Rules directory is missing")
        )

    agent_names: dict[str, str] = {}
    if agents_dir.is_dir():
        for path in sorted(agents_dir.glob("*.md")):
            relative = path.relative_to(root).as_posix()
            if selected is not None and relative not in selected:
                continue
            _validate_cursor_agent(root, path, agent_names, result)

    skill_names: dict[str, str] = {}
    if skills_dir.is_dir():
        _validate_skill_packages(root, skills_dir, skill_names, selected, result)


def _validate_claude_tree(
    root: Path,
    selected: set[str] | None,
    result: ValidationResult,
) -> None:
    layout = HOST_LAYOUTS[HOST_CLAUDE]
    rules_dir = root / layout.rules_dir  # type: ignore[operator]
    agents_dir = root / layout.agents_dir  # type: ignore[operator]
    skills_dir = root / layout.skills_dir  # type: ignore[operator]
    if not rules_dir.is_dir() and not agents_dir.is_dir() and not skills_dir.is_dir():
        return

    if rules_dir.is_dir():
        for path in sorted(rules_dir.glob("*.md")):
            relative = path.relative_to(root).as_posix()
            if selected is not None and relative not in selected:
                continue
            _validate_claude_rule(root, path, result)

    agent_names: dict[str, str] = {}
    if agents_dir.is_dir():
        for path in sorted(agents_dir.glob("*.md")):
            relative = path.relative_to(root).as_posix()
            if selected is not None and relative not in selected:
                continue
            _validate_claude_agent(root, path, agent_names, result)

    skill_names: dict[str, str] = {}
    if skills_dir.is_dir():
        _validate_skill_packages(root, skills_dir, skill_names, selected, result)


def _validate_copilot_tree(
    root: Path,
    selected: set[str] | None,
    result: ValidationResult,
) -> None:
    instructions = root / ".github" / "instructions"
    if not instructions.is_dir():
        return
    for path in sorted(instructions.rglob("*.instructions.md")):
        relative = path.relative_to(root).as_posix()
        if selected is not None and relative not in selected:
            continue
        _validate_copilot_instruction(root, path, result)


def _validate_codex_tree(
    root: Path,
    selected: set[str] | None,
    result: ValidationResult,
) -> None:
    skills_dir = root / ".agents" / "skills"
    if not skills_dir.is_dir():
        return
    skill_names: dict[str, str] = {}
    _validate_skill_packages(root, skills_dir, skill_names, selected, result)


def _validate_skill_packages(
    root: Path,
    skills_dir: Path,
    skill_names: dict[str, str],
    selected: set[str] | None,
    result: ValidationResult,
) -> None:
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        relative_skill = skill_file.relative_to(root).as_posix()
        package_prefix = skill_dir.relative_to(root).as_posix() + "/"
        package_selected = selected is None or any(
            item == relative_skill or item.startswith(package_prefix)
            for item in selected
        )
        if not package_selected:
            continue
        if skill_dir.is_symlink():
            result.errors.append(
                Finding(
                    "error",
                    skill_dir.relative_to(root).as_posix(),
                    "Skill package must not be a symlink",
                )
            )
            continue
        if not skill_file.is_file():
            result.errors.append(
                Finding(
                    "error",
                    skill_dir.relative_to(root).as_posix(),
                    "Skill package requires SKILL.md",
                )
            )
            continue
        _validate_skill(root, skill_dir, skill_file, skill_names, result)
        _validate_skill_tree(root, skill_dir, result)


def _validate_cursor_rule(root: Path, path: Path, result: ValidationResult) -> None:
    relative = path.relative_to(root).as_posix()
    if path.is_symlink():
        result.errors.append(Finding("error", relative, "Rule file must not be a symlink"))
        return
    text = _read_text(path, relative, result)
    if text is None:
        return
    metadata, body = _parse_frontmatter(text, relative, result)
    if metadata is None:
        return
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        result.errors.append(
            Finding("error", relative, "Rule frontmatter requires description")
        )
    always_apply = metadata.get("alwaysApply", False)
    globs = metadata.get("globs")
    if always_apply not in (True, False):
        result.errors.append(
            Finding("error", relative, "alwaysApply must be true or false when set")
        )
        always_apply = False
    if always_apply and globs not in (None, ""):
        result.warnings.append(
            Finding(
                "warning",
                relative,
                "alwaysApply rules usually omit globs; keep one clear application mode",
            )
        )
    if not always_apply and globs in (None, ""):
        result.warnings.append(
            Finding(
                "warning",
                relative,
                "Non-alwaysApply rules should declare globs",
            )
        )
    body_lines = len(body.splitlines())
    soft_limit = (
        RULE_SOFT_ALWAYS_APPLY_LINES if always_apply else RULE_SOFT_GLOB_LINES
    )
    if body_lines > soft_limit:
        result.warnings.append(
            Finding(
                "warning",
                relative,
                f"Rule body has {body_lines} lines; soft budget is {soft_limit}",
            )
        )
    _scan_secrets(relative, text, result)
    _scan_markdown_links(root, path, body, result)


def _validate_claude_rule(root: Path, path: Path, result: ValidationResult) -> None:
    relative = path.relative_to(root).as_posix()
    if path.is_symlink():
        result.errors.append(Finding("error", relative, "Rule file must not be a symlink"))
        return
    text = _read_text(path, relative, result)
    if text is None:
        return
    metadata, body = _parse_frontmatter(text, relative, result, required=False)
    if metadata is None:
        metadata = {}
    paths = metadata.get("paths")
    if paths is not None and not isinstance(paths, (str, list)):
        result.errors.append(
            Finding("error", relative, "Claude rule paths must be a string or list")
        )
    _scan_secrets(relative, text, result)
    _scan_markdown_links(root, path, body if body else text, result)


def _validate_copilot_instruction(
    root: Path,
    path: Path,
    result: ValidationResult,
) -> None:
    relative = path.relative_to(root).as_posix()
    if path.is_symlink():
        result.errors.append(
            Finding("error", relative, "Instruction file must not be a symlink")
        )
        return
    text = _read_text(path, relative, result)
    if text is None:
        return
    metadata, body = _parse_frontmatter(text, relative, result)
    if metadata is None:
        return
    apply_to = metadata.get("applyTo")
    if not isinstance(apply_to, str) or not apply_to.strip():
        result.errors.append(
            Finding(
                "error",
                relative,
                "Copilot instruction frontmatter requires applyTo",
            )
        )
    _scan_secrets(relative, text, result)
    _scan_markdown_links(root, path, body, result)


def _validate_cursor_agent(
    root: Path,
    path: Path,
    agent_names: dict[str, str],
    result: ValidationResult,
) -> None:
    relative = path.relative_to(root).as_posix()
    if path.is_symlink():
        result.errors.append(
            Finding("error", relative, "Agent definition must not be a symlink")
        )
        return
    text = _read_text(path, relative, result)
    if text is None:
        return
    metadata, body = _parse_frontmatter(text, relative, result)
    if metadata is None:
        return
    name = metadata.get("name")
    if not isinstance(name, str) or not name.strip():
        result.errors.append(
            Finding("error", relative, "Agent frontmatter requires name")
        )
    else:
        _validate_agent_name(path, relative, name, agent_names, result)
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        result.errors.append(
            Finding("error", relative, "Agent frontmatter requires description")
        )
    elif len(description) > DESCRIPTION_MAX:
        result.errors.append(
            Finding(
                "error",
                relative,
                f"Agent description exceeds {DESCRIPTION_MAX} characters",
            )
        )
    if metadata.get("model") != "inherit":
        result.errors.append(
            Finding("error", relative, "Agent model must be inherit")
        )
    if metadata.get("readonly") not in (True, False):
        result.errors.append(
            Finding(
                "error",
                relative,
                "Agent readonly must be true or false "
                "(true for advisory/review; false when shell checks are required)",
            )
        )
    if metadata.get("is_background") is not True:
        result.errors.append(
            Finding("error", relative, "Agent is_background must be true")
        )
    if not body.strip():
        result.errors.append(
            Finding("error", relative, "Agent definition requires a prompt body")
        )
    _scan_secrets(relative, text, result)
    _scan_markdown_links(root, path, body, result)


def _validate_claude_agent(
    root: Path,
    path: Path,
    agent_names: dict[str, str],
    result: ValidationResult,
) -> None:
    relative = path.relative_to(root).as_posix()
    if path.is_symlink():
        result.errors.append(
            Finding("error", relative, "Agent definition must not be a symlink")
        )
        return
    text = _read_text(path, relative, result)
    if text is None:
        return
    metadata, body = _parse_frontmatter(text, relative, result)
    if metadata is None:
        return
    name = metadata.get("name")
    if not isinstance(name, str) or not name.strip():
        result.errors.append(
            Finding("error", relative, "Agent frontmatter requires name")
        )
    else:
        _validate_agent_name(path, relative, name, agent_names, result)
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        result.errors.append(
            Finding("error", relative, "Agent frontmatter requires description")
        )
    if not body.strip():
        result.errors.append(
            Finding("error", relative, "Agent definition requires a prompt body")
        )
    _scan_secrets(relative, text, result)
    _scan_markdown_links(root, path, body, result)


def _validate_agent_name(
    path: Path,
    relative: str,
    name: str,
    agent_names: dict[str, str],
    result: ValidationResult,
) -> None:
    if len(name) > NAME_MAX or not NAME_PATTERN.fullmatch(name):
        result.errors.append(
            Finding(
                "error",
                relative,
                "Agent name must be lowercase letters, numbers, and hyphens "
                f"(max {NAME_MAX})",
            )
        )
    owner = agent_names.get(name)
    if owner:
        result.errors.append(
            Finding(
                "error",
                relative,
                f"Duplicate agent name {name!r}; also defined in {owner}",
            )
        )
    else:
        agent_names[name] = relative
    if name != path.stem:
        result.errors.append(
            Finding(
                "error",
                relative,
                f"Agent name {name!r} must match filename {path.stem!r}",
            )
        )


def _validate_skill(
    root: Path,
    skill_dir: Path,
    skill_file: Path,
    skill_names: dict[str, str],
    result: ValidationResult,
) -> None:
    relative = skill_file.relative_to(root).as_posix()
    if skill_file.is_symlink():
        result.errors.append(
            Finding("error", relative, "SKILL.md must not be a symlink")
        )
        return
    text = _read_text(skill_file, relative, result)
    if text is None:
        return
    metadata, body = _parse_frontmatter(text, relative, result)
    if metadata is None:
        return
    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not name.strip():
        result.errors.append(
            Finding("error", relative, "Skill frontmatter requires name")
        )
    else:
        if len(name) > NAME_MAX or not NAME_PATTERN.fullmatch(name):
            result.errors.append(
                Finding(
                    "error",
                    relative,
                    "Skill name must be lowercase letters, numbers, and hyphens "
                    f"(max {NAME_MAX})",
                )
            )
        owner = skill_names.get(name)
        if owner:
            result.errors.append(
                Finding(
                    "error",
                    relative,
                    f"Duplicate skill name {name!r}; also defined in {owner}",
                )
            )
        else:
            skill_names[name] = relative
        if name != skill_dir.name:
            result.warnings.append(
                Finding(
                    "warning",
                    relative,
                    f"Skill name {name!r} differs from directory {skill_dir.name!r}",
                )
            )
    if not isinstance(description, str) or not description.strip():
        result.errors.append(
            Finding("error", relative, "Skill frontmatter requires description")
        )
    elif len(description) > DESCRIPTION_MAX:
        result.errors.append(
            Finding(
                "error",
                relative,
                f"Skill description exceeds {DESCRIPTION_MAX} characters",
            )
        )
    body_lines = len(body.splitlines())
    if body_lines > SKILL_SOFT_LINES:
        result.warnings.append(
            Finding(
                "warning",
                relative,
                f"SKILL.md has {body_lines} lines; soft budget is {SKILL_SOFT_LINES}",
            )
        )
    _scan_secrets(relative, text, result)
    _scan_markdown_links(root, skill_file, body, result)


def _validate_skill_tree(root: Path, skill_dir: Path, result: ValidationResult) -> None:
    package_root = skill_dir.resolve()
    for path in sorted(skill_dir.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            result.errors.append(
                Finding("error", relative, "Skill package may not contain symlinks")
            )
            continue
        try:
            resolved = path.resolve()
            resolved.relative_to(package_root)
        except ValueError:
            result.errors.append(
                Finding("error", relative, "Skill path escapes its package directory")
            )
            continue
        if not path.is_file() or path.name == "SKILL.md":
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if _skip_secret_scan(relative):
            continue
        text = _read_text(path, relative, result)
        if text is None:
            continue
        _scan_secrets(relative, text, result)


def _skip_secret_scan(relative: str) -> bool:
    return any(marker in relative for marker in SECRET_SCAN_EXCLUDED_SUFFIXES)


def _scan_markdown_links(
    root: Path,
    source: Path,
    body: str,
    result: ValidationResult,
) -> None:
    relative = source.relative_to(root).as_posix()
    for match in MARKDOWN_LINK.finditer(body):
        target = match.group(1).strip().strip("\"'")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        if target.startswith("@"):
            continue
        path_part = target.split("#", 1)[0].split("?", 1)[0].strip()
        if not path_part:
            continue
        candidate = (source.parent / path_part).resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            result.errors.append(
                Finding(
                    "error",
                    relative,
                    f"Markdown link escapes the repository: {target}",
                )
            )
            continue
        if not candidate.exists():
            result.errors.append(
                Finding(
                    "error",
                    relative,
                    f"Broken local markdown link: {target}",
                )
            )


def _scan_secrets(relative: str, text: str, result: ValidationResult) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            result.errors.append(
                Finding(
                    "error",
                    relative,
                    "Possible secret material detected; remove credentials before promoting",
                )
            )
            return


def _parse_frontmatter(
    text: str,
    relative: str,
    result: ValidationResult,
    *,
    required: bool = True,
) -> tuple[dict[str, object] | None, str]:
    lines = text.splitlines()
    # Skip HTML sync markers before frontmatter.
    start = 0
    while start < len(lines) and (
        not lines[start].strip() or lines[start].strip().startswith("<!--")
    ):
        start += 1
    if start >= len(lines) or lines[start].strip() != FRONTMATTER_FENCE:
        if required:
            result.errors.append(
                Finding(
                    "error",
                    relative,
                    "File requires YAML frontmatter starting with ---",
                )
            )
            return None, text
        return {}, text
    closing = next(
        (
            index
            for index, line in enumerate(lines[start + 1 :], start=start + 1)
            if line.strip() == FRONTMATTER_FENCE
        ),
        None,
    )
    if closing is None:
        result.errors.append(
            Finding("error", relative, "Frontmatter is not closed with ---")
        )
        return None, text
    block = "\n".join(lines[start + 1 : closing])
    metadata = _load_frontmatter(block, relative, result)
    body = "\n".join(lines[closing + 1 :])
    return metadata, body


def _load_frontmatter(
    block: str,
    relative: str,
    result: ValidationResult,
) -> dict[str, object] | None:
    try:
        loaded = yaml.safe_load(block) or {}
    except yaml.YAMLError as exc:
        result.errors.append(
            Finding("error", relative, f"Invalid YAML frontmatter: {exc}")
        )
        return None
    if not isinstance(loaded, dict):
        result.errors.append(Finding("error", relative, "Frontmatter must be a mapping"))
        return None
    return dict(loaded)


def _read_text(path: Path, relative: str, result: ValidationResult) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        result.errors.append(Finding("error", relative, f"Unable to read file: {exc}"))
        return None
    except UnicodeDecodeError:
        result.errors.append(Finding("error", relative, "File must be UTF-8 text"))
        return None


def _normalize_changed(root: Path, changed_files: Sequence[str]) -> set[str]:
    normalized: set[str] = set()
    root_resolved = root.resolve()
    for item in changed_files:
        path = Path(item)
        if not path.is_absolute():
            path = root / path
        try:
            relative = path.resolve().relative_to(root_resolved).as_posix()
        except ValueError:
            continue
        normalized.add(relative)
    return normalized


def _print_findings(findings: Iterable[Finding]) -> None:
    for finding in findings:
        print(f"{finding.severity.upper()}: {finding.path}: {finding.message}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate repo-local project policy across Cursor, Claude, "
            "Copilot, and Codex"
        )
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root (default: current directory)",
    )
    parser.add_argument(
        "--changed",
        action="append",
        default=[],
        help=(
            "Limit validation to these repo-relative paths (repeatable). "
            "For iteration only; promotion must validate the full repository."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    result = validate_repository(root, changed_files=args.changed or None)
    if args.json:
        payload = {
            "ok": result.ok,
            "errors": [asdict(item) for item in result.errors],
            "warnings": [asdict(item) for item in result.warnings],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_findings(result.errors)
        _print_findings(result.warnings)
        if result.ok:
            print(
                f"OK: {len(result.warnings)} warning(s), {len(result.errors)} error(s)"
            )
        else:
            print(
                f"FAILED: {len(result.errors)} error(s), "
                f"{len(result.warnings)} warning(s)"
            )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
