#!/usr/bin/env python3
"""Bump plugin semver across manifests and all four marketplace catalogs.

Hosts that pin a computed version (Claude Code, Copilot, Codex) refuse to
replace the install cache when the version string is unchanged — even after
new commits land on GitHub. Bump before commit/push so
``scripts/refresh_marketplaces.py --plugins`` (and host update CLIs) actually
pull new content.

Examples:

  python3 scripts/bump_plugin_versions.py global code
  python3 scripts/bump_plugin_versions.py --changed
  python3 scripts/bump_plugin_versions.py security --level minor
  python3 scripts/bump_plugin_versions.py --changed --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "plugins"

MANIFEST_RELS = (
    ".cursor-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
)

CATALOGS = (
    ROOT / ".cursor-plugin" / "marketplace.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".github" / "plugin" / "marketplace.json",
    ROOT / ".agents" / "plugins" / "marketplace.json",
)

SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def parse_semver(version: str) -> tuple[int, int, int]:
    m = SEMVER.match(version.strip())
    if not m:
        raise SystemExit(f"not semver X.Y.Z: {version!r}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def bump_semver(version: str, level: str) -> str:
    major, minor, patch = parse_semver(version)
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise SystemExit(f"unknown level: {level}")


def plugin_dirs() -> list[str]:
    return sorted(p.name for p in PLUGINS.iterdir() if p.is_dir() and not p.name.startswith("."))


def read_manifest_version(short: str) -> str:
    path = PLUGINS / short / ".cursor-plugin" / "plugin.json"
    if not path.is_file():
        raise SystemExit(f"missing manifest: {path.relative_to(ROOT)}")
    version = load_json(path).get("version")
    if not isinstance(version, str):
        raise SystemExit(f"{short}: cursor plugin.json missing version")
    return version


def changed_plugin_shorts() -> list[str]:
    """Short keys with dirty or HEAD-diff paths under plugins/<short>/."""
    cmd = [
        "git",
        "-C",
        str(ROOT),
        "diff",
        "--name-only",
        "HEAD",
        "--",
        "plugins/",
    ]
    # Also include untracked under plugins/
    untracked = [
        "git",
        "-C",
        str(ROOT),
        "ls-files",
        "--others",
        "--exclude-standard",
        "--",
        "plugins/",
    ]
    paths: set[str] = set()
    for argv in (cmd, untracked):
        completed = subprocess.run(argv, check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            raise SystemExit(completed.stderr.strip() or f"git failed: {argv}")
        paths.update(line.strip() for line in completed.stdout.splitlines() if line.strip())

    shorts: set[str] = set()
    known = set(plugin_dirs())
    for rel in paths:
        parts = Path(rel).parts
        if len(parts) >= 2 and parts[0] == "plugins" and parts[1] in known:
            shorts.add(parts[1])
    return sorted(shorts)


def set_manifest_versions(short: str, version: str, *, dry_run: bool) -> list[str]:
    touched: list[str] = []
    for rel in MANIFEST_RELS:
        path = PLUGINS / short / rel
        if not path.is_file():
            raise SystemExit(f"{short}: missing {rel}")
        data = load_json(path)
        old = data.get("version")
        if old == version:
            continue
        data["version"] = version
        touched.append(f"{path.relative_to(ROOT)}: {old} -> {version}")
        if not dry_run:
            dump_json(path, data)
    return touched


def set_catalog_versions(short: str, version: str, *, dry_run: bool) -> list[str]:
    name = f"nodadyoushutup-{short}"
    touched: list[str] = []
    for path in CATALOGS:
        data = load_json(path)
        plugins = data.get("plugins")
        if not isinstance(plugins, list):
            raise SystemExit(f"{path.relative_to(ROOT)}: missing plugins[]")
        found = False
        for entry in plugins:
            if entry.get("name") != name:
                continue
            found = True
            old = entry.get("version")
            if old == version:
                break
            entry["version"] = version
            touched.append(f"{path.relative_to(ROOT)} [{name}]: {old} -> {version}")
            if not dry_run:
                dump_json(path, data)
            break
        if not found:
            raise SystemExit(
                f"{path.relative_to(ROOT)}: no catalog entry for {name}"
            )
    return touched


def bump_marketplace_metadata(*, dry_run: bool) -> list[str]:
    """Patch-bump catalog metadata.version when present (not Codex)."""
    touched: list[str] = []
    for path in CATALOGS:
        data = load_json(path)
        meta = data.get("metadata")
        if not isinstance(meta, dict) or "version" not in meta:
            continue
        old = meta["version"]
        if not isinstance(old, str):
            raise SystemExit(f"{path.relative_to(ROOT)}: metadata.version not a string")
        new = bump_semver(old, "patch")
        meta["version"] = new
        touched.append(f"{path.relative_to(ROOT)} [marketplace]: {old} -> {new}")
        if not dry_run:
            dump_json(path, data)
    return touched


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Bump plugin version in the three host manifests and all four "
            "marketplace catalogs."
        )
    )
    parser.add_argument(
        "plugins",
        nargs="*",
        help="Short plugin keys (folder stems). Required unless --changed.",
    )
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Bump every plugin with paths changed vs HEAD under plugins/.",
    )
    parser.add_argument(
        "--level",
        choices=("patch", "minor", "major"),
        default="patch",
        help="Semver component to bump (default: patch).",
    )
    parser.add_argument(
        "--no-marketplace",
        action="store_true",
        help="Do not patch-bump catalog metadata.version.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes without modifying files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    known = set(plugin_dirs())

    shorts: list[str] = []
    if args.changed:
        shorts.extend(changed_plugin_shorts())
    shorts.extend(args.plugins)

    # Preserve order, drop dupes.
    seen: set[str] = set()
    ordered: list[str] = []
    for short in shorts:
        if short in seen:
            continue
        seen.add(short)
        ordered.append(short)

    if not ordered:
        raise SystemExit(
            "no plugins to bump — pass short keys or use --changed "
            "(with dirty/HEAD diffs under plugins/)"
        )

    unknown = [s for s in ordered if s not in known]
    if unknown:
        raise SystemExit(f"unknown plugin(s): {', '.join(unknown)}")

    all_touched: list[str] = []
    for short in ordered:
        old = read_manifest_version(short)
        new = bump_semver(old, args.level)
        print(f"{short}: {old} -> {new}", flush=True)
        all_touched.extend(set_manifest_versions(short, new, dry_run=args.dry_run))
        all_touched.extend(set_catalog_versions(short, new, dry_run=args.dry_run))

    if not args.no_marketplace:
        all_touched.extend(bump_marketplace_metadata(dry_run=args.dry_run))

    if not all_touched:
        print("nothing to write (already at target versions)", flush=True)
        return 0

    prefix = "would write" if args.dry_run else "wrote"
    for line in all_touched:
        print(f"  {prefix}: {line}", flush=True)

    if not args.dry_run:
        print(
            "\nNext: python3 scripts/validate_marketplace.py && commit/push, "
            "then python3 scripts/refresh_marketplaces.py --plugins",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
