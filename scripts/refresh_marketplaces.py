#!/usr/bin/env python3
"""Refresh registered copies of this marketplace across agent harnesses.

Runs each host's marketplace update CLI when that binary is on PATH:

  Cursor   agent plugin marketplace update …
  Claude   claude plugin marketplace update …
  Codex    codex plugin marketplace upgrade …
  Copilot  copilot plugin marketplace update …

Cursor personal imports can stay pinned to the first-import commit. Use
``--force`` to remove + re-add with ``--git-ref`` (may require reinstalling
plugins in Customize). Claude/Codex/Copilot usually advance with a plain
update; ``--plugins`` also asks those CLIs to refresh installed plugins when
they expose that command.

Examples:

  python3 scripts/refresh_marketplaces.py
  python3 scripts/refresh_marketplaces.py --harness cursor,claude
  python3 scripts/refresh_marketplaces.py --force
  python3 scripts/refresh_marketplaces.py --plugins
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable


DEFAULT_NAME = "nodadyoushutup-marketplace"
DEFAULT_URL = "https://github.com/nodadyoushutup/marketplace"
DEFAULT_GIT_REF = "main"


@dataclass(frozen=True)
class Harness:
    key: str
    label: str
    binaries: tuple[str, ...]
    update: Callable[[str, list[str]], list[str]]
    force: Callable[[str, list[str], str, str], list[str]] | None = None
    plugins: Callable[[str, list[str]], list[str]] | None = None


def which_first(names: tuple[str, ...]) -> str | None:
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def run(argv: list[str], *, dry_run: bool) -> int:
    print("+", " ".join(argv), flush=True)
    if dry_run:
        return 0
    completed = subprocess.run(argv, check=False)
    return int(completed.returncode)


def cursor_update(binary: str, args: list[str]) -> list[str]:
    # Cursor requires a name or URL.
    target = args[0] if args else DEFAULT_NAME
    return [binary, "plugin", "marketplace", "update", target]


def cursor_force(binary: str, _args: list[str], url: str, git_ref: str) -> list[str]:
    # Sequence handled specially in main (remove then add).
    return [binary, "plugin", "marketplace", "remove", DEFAULT_NAME]


def claude_update(binary: str, args: list[str]) -> list[str]:
    # No name → refresh every registered marketplace.
    cmd = [binary, "plugin", "marketplace", "update"]
    cmd.extend(args)
    return cmd


def claude_plugins(binary: str, args: list[str]) -> list[str]:
    # Claude has no update-all-plugins; marketplace update with a name also
    # refreshes installed plugins from that marketplace in the UI path.
    # From shell, update the marketplace listing then leave plugin bumps to
    # `claude plugin update <id>@<marketplace>` when the user names them.
    name = args[0] if args else DEFAULT_NAME
    return [binary, "plugin", "marketplace", "update", name]


def codex_update(binary: str, args: list[str]) -> list[str]:
    cmd = [binary, "plugin", "marketplace", "upgrade"]
    cmd.extend(args)
    return cmd


def copilot_update(binary: str, args: list[str]) -> list[str]:
    cmd = [binary, "plugin", "marketplace", "update"]
    cmd.extend(args)
    return cmd


def copilot_plugins(binary: str, _args: list[str]) -> list[str]:
    return [binary, "plugin", "update", "--all"]


HARNESSES: tuple[Harness, ...] = (
    Harness(
        key="cursor",
        label="Cursor (agent)",
        binaries=("agent", "cursor-agent"),
        update=cursor_update,
        force=cursor_force,
    ),
    Harness(
        key="claude",
        label="Claude Code",
        binaries=("claude",),
        update=claude_update,
        plugins=claude_plugins,
    ),
    Harness(
        key="codex",
        label="OpenAI Codex",
        binaries=("codex",),
        update=codex_update,
    ),
    Harness(
        key="copilot",
        label="GitHub Copilot",
        binaries=("copilot",),
        update=copilot_update,
        plugins=copilot_plugins,
    ),
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Refresh nodadyoushutup-marketplace (or another name) on every "
            "agent harness CLI found on PATH."
        )
    )
    parser.add_argument(
        "--harness",
        default="all",
        help=(
            "Comma list: cursor,claude,codex,copilot — or 'all' (default). "
            "Skipped when the binary is missing."
        ),
    )
    parser.add_argument(
        "--marketplace",
        default=DEFAULT_NAME,
        help=f"Marketplace name (default: {DEFAULT_NAME})",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Git URL used for Cursor --force re-add (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--git-ref",
        default=DEFAULT_GIT_REF,
        help=f"Git ref for Cursor --force re-add (default: {DEFAULT_GIT_REF})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Cursor only: remove + re-add the marketplace with --git-ref to "
            "break a personal-import pin. You may need to reinstall plugins."
        ),
    )
    parser.add_argument(
        "--plugins",
        action="store_true",
        help=(
            "Also refresh installed plugins where the harness supports it "
            "(Copilot: plugin update --all; Claude: named marketplace update)."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without running them.",
    )
    return parser.parse_args(argv)


def selected_harnesses(spec: str) -> list[Harness]:
    if spec.strip().lower() == "all":
        return list(HARNESSES)
    wanted = {part.strip().lower() for part in spec.split(",") if part.strip()}
    unknown = wanted - {h.key for h in HARNESSES}
    if unknown:
        raise SystemExit(f"unknown harness(es): {', '.join(sorted(unknown))}")
    return [h for h in HARNESSES if h.key in wanted]


def refresh_cursor(
    binary: str,
    *,
    marketplace: str,
    url: str,
    git_ref: str,
    force: bool,
    dry_run: bool,
) -> int:
    if not force:
        return run(cursor_update(binary, [marketplace]), dry_run=dry_run)

    print(
        "Cursor --force: remove + add (may require reinstalling plugins "
        "in Customize). Personal pins often ignore plain update.",
        flush=True,
    )
    # Prefer URL for remove when name fails on some builds.
    rc = run([binary, "plugin", "marketplace", "remove", marketplace], dry_run=dry_run)
    if rc != 0:
        rc = run([binary, "plugin", "marketplace", "remove", url], dry_run=dry_run)
    if rc != 0 and not dry_run:
        print("warning: remove failed; continuing with add", file=sys.stderr)
    return run(
        [binary, "plugin", "marketplace", "add", url, "--git-ref", git_ref],
        dry_run=dry_run,
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    harnesses = selected_harnesses(args.harness)
    market_args = [args.marketplace] if args.marketplace else []

    ran = 0
    failed = 0
    skipped: list[str] = []

    for harness in harnesses:
        binary = which_first(harness.binaries)
        if not binary:
            skipped.append(f"{harness.label} ({'/'.join(harness.binaries)} not on PATH)")
            continue

        print(f"\n== {harness.label} ({binary}) ==", flush=True)
        ran += 1

        if harness.key == "cursor":
            rc = refresh_cursor(
                binary,
                marketplace=args.marketplace,
                url=args.url,
                git_ref=args.git_ref,
                force=args.force,
                dry_run=args.dry_run,
            )
        else:
            rc = run(harness.update(binary, market_args), dry_run=args.dry_run)

        if rc != 0:
            failed += 1
            print(f"failed ({rc}): {harness.label}", file=sys.stderr)
            continue

        if args.plugins and harness.plugins is not None:
            prc = run(harness.plugins(binary, market_args), dry_run=args.dry_run)
            if prc != 0:
                failed += 1
                print(f"plugin refresh failed ({prc}): {harness.label}", file=sys.stderr)

    print("\n== summary ==", flush=True)
    print(f"ran: {ran}", flush=True)
    print(f"failed: {failed}", flush=True)
    for item in skipped:
        print(f"skipped: {item}", flush=True)

    if ran == 0:
        print(
            "No harness CLIs found. Install agent/claude/codex/copilot on PATH.",
            file=sys.stderr,
        )
        return 2

    if failed:
        return 1

    print(
        "\nNext: reload the host (Cursor: Developer: Reload Window; "
        "Claude: /reload-plugins; Codex/Copilot: new session).",
        flush=True,
    )
    if not args.force:
        print(
            "Cursor still stale after update? Re-run with --force.",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
