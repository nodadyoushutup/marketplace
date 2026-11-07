#!/usr/bin/env python3
"""Unit tests for agentmemory_scope.py (stdlib unittest)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "agentmemory_scope.py"
sys.path.insert(0, str(SCRIPT.parent))

import agentmemory_scope as scope  # noqa: E402


class NormalizeRemoteTests(unittest.TestCase):
    def test_https_github(self) -> None:
        self.assertEqual(
            scope._normalize_remote("https://github.com/acme/widgets.git"),
            "acme/widgets",
        )

    def test_ssh_github(self) -> None:
        self.assertEqual(
            scope._normalize_remote("git@github.com:acme/widgets.git"),
            "acme/widgets",
        )

    def test_ssh_gitlab_nested(self) -> None:
        self.assertEqual(
            scope._normalize_remote("git@gitlab.com:group/sub/widgets.git"),
            "group/sub/widgets",
        )


class ResolveRepoTests(unittest.TestCase):
    def test_no_git_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(scope.resolve_repo(Path(tmp)))

    def test_git_repo_uses_origin_or_basename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://github.com/acme/demo.git"],
                cwd=root,
                check=True,
                capture_output=True,
            )
            self.assertEqual(scope.resolve_repo(root), "acme/demo")


class BuildScopeTests(unittest.TestCase):
    def test_user_stamp_always_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data = scope.build_scope(Path(tmp))
            self.assertTrue(data["user"])
            self.assertEqual(data["user_stamp"], f"user:{data['user']}")
            self.assertIn(data["user_stamp"], data["concepts"])
            self.assertIn(data["user_stamp"], data["tags"])
            self.assertIsNone(data["repo"])
            self.assertIsNone(data["project"])

    def test_cli_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--cwd", tmp],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            self.assertIn("user_stamp", payload)
            self.assertTrue(payload["user_stamp"].startswith("user:"))


if __name__ == "__main__":
    unittest.main()
