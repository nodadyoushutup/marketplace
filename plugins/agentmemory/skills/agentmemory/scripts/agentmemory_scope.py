#!/usr/bin/env python3
"""Resolve AgentMemory user + optional git-repo scope stamps (stdlib only).

Prints JSON on stdout for agents/rules to stamp every save and hard-filter
every recall so a shared AgentMemory service cannot cross user streams.

Usage:
  python3 agentmemory_scope.py
  python3 agentmemory_scope.py --cwd /path/to/workspace
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


def resolve_user() -> str:
    """whoami-equivalent username for Linux, macOS, and Windows."""
    try:
        name = getpass.getuser()
        if name and name.strip():
            return name.strip()
    except Exception:
        pass

    for key in ("USER", "USERNAME", "LOGNAME"):
        value = os.environ.get(key, "").strip()
        if value:
            return value

    try:
        completed = subprocess.run(
            ["whoami"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        name = (completed.stdout or "").strip()
        if completed.returncode == 0 and name:
            return name
    except Exception:
        pass

    raise SystemExit("agentmemory_scope: unable to resolve local username")


def _git(cwd: Path, *args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return None
    if completed.returncode != 0:
        return None
    out = (completed.stdout or "").strip()
    return out or None


def _find_git_root(start: Path) -> Path | None:
    cur = start.resolve()
    if not cur.is_dir():
        cur = cur.parent
    for path in (cur, *cur.parents):
        if (path / ".git").exists():
            return path
    return None


def _normalize_remote(url: str) -> str | None:
    raw = url.strip()
    if not raw:
        return None

    # git@host:owner/repo.git  → owner/repo (drop host; path is the repo id)
    scp = re.match(r"^[^@\s]+@([^:\s]+):(.+)$", raw)
    if scp:
        path = scp.group(2).removesuffix(".git").strip("/")
        return path or None

    parsed = urlparse(raw)
    if parsed.scheme and parsed.netloc:
        path = unquote(parsed.path or "").removesuffix(".git").strip("/")
        return path or None

    # Plain path or owner/repo
    cleaned = raw.removesuffix(".git").strip("/")
    return cleaned or None


def resolve_repo(cwd: Path) -> str | None:
    """Stable repo id when cwd is inside a git work tree; else None."""
    root = _find_git_root(cwd)
    if root is None:
        return None

    remote = _git(root, "remote", "get-url", "origin")
    if remote:
        normalized = _normalize_remote(remote)
        if normalized:
            return normalized

    toplevel = _git(root, "rev-parse", "--show-toplevel")
    if toplevel:
        return Path(toplevel).name
    return root.name


def build_scope(cwd: Path) -> dict:
    user = resolve_user()
    repo = resolve_repo(cwd)
    user_stamp = f"user:{user}"
    stamps = [user_stamp]
    repo_stamp = None
    if repo:
        repo_stamp = f"repo:{repo}"
        stamps.append(repo_stamp)

    joined = ",".join(stamps)
    return {
        "user": user,
        "repo": repo,
        "user_stamp": user_stamp,
        "repo_stamp": repo_stamp,
        "concepts": joined,
        "tags": joined,
        "project": repo,
        "query_prefix": user_stamp if not repo_stamp else f"{user_stamp} {repo_stamp}",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cwd",
        default=".",
        help="Workspace directory used to detect .git (default: .)",
    )
    args = parser.parse_args(argv)
    cwd = Path(args.cwd).expanduser()
    if not cwd.exists():
        print(f"agentmemory_scope: cwd does not exist: {cwd}", file=sys.stderr)
        return 2
    print(json.dumps(build_scope(cwd), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
