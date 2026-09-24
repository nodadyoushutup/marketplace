"""Tests for project policy validation."""

from __future__ import annotations

import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


def _load_module(name: str):
    path = Path(__file__).resolve().parents[1] / f"{name}.py"
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
    return module


validate_policy = _load_module("validate_policy")
policy_config = _load_module("policy_config")


class ValidatePolicyTests(unittest.TestCase):
    def test_valid_rule_and_skill_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_rule(
                root,
                "demo.mdc",
                "---\ndescription: Demo rule\nalwaysApply: true\n---\n\n# Demo\n\n- Keep it short.\n",
            )
            skill = self._write_skill(
                root,
                "demo-skill",
                "---\nname: demo-skill\ndescription: Demo skill for validation tests.\n---\n\n# Demo\n\nSee [notes](references/notes.md).\n",
            )
            (skill / "references").mkdir()
            (skill / "references" / "notes.md").write_text("# Notes\n", encoding="utf-8")
            self._write_agent(root, "demo-agent")

            result = validate_policy.validate_repository(root)

            self.assertTrue(result.ok)
            self.assertEqual(result.errors, [])

    def test_agent_frontmatter_and_body_are_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = root / ".cursor" / "agents" / "broken.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "---\nname: wrong-name\ndescription: Broken agent\n"
                "model: custom\nreadonly: maybe\nis_background: false\n---\n",
                encoding="utf-8",
            )

            result = validate_policy.validate_repository(root)

            self.assertFalse(result.ok)
            messages = " ".join(item.message for item in result.errors)
            self.assertIn("must match filename", messages)
            self.assertIn("model must be inherit", messages)
            self.assertIn("readonly must be true or false", messages)
            self.assertIn("is_background must be true", messages)
            self.assertIn("requires a prompt body", messages)

    def test_symlink_agent_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            target = root / "agent.md"
            target.write_text(
                "---\nname: linked\ndescription: Linked\nmodel: inherit\n"
                "readonly: true\nis_background: true\n---\n\nPrompt.\n",
                encoding="utf-8",
            )
            agent = root / ".cursor" / "agents" / "linked.md"
            agent.parent.mkdir(parents=True)
            agent.symlink_to(target)

            result = validate_policy.validate_repository(root)

            self.assertFalse(result.ok)
            self.assertTrue(
                any(
                    "Agent definition must not be a symlink" in item.message
                    for item in result.errors
                )
            )

    def test_malformed_frontmatter_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_rule(
                root,
                "broken.mdc",
                "---\ndescription: Missing close\nalwaysApply: true\n\n# Body\n",
            )

            result = validate_policy.validate_repository(root)

            self.assertFalse(result.ok)
            self.assertTrue(
                any("Frontmatter is not closed" in item.message for item in result.errors)
            )

    def test_duplicate_skill_names_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_skill(
                root,
                "one",
                "---\nname: shared-name\ndescription: First skill.\n---\n\n# One\n",
            )
            self._write_skill(
                root,
                "two",
                "---\nname: shared-name\ndescription: Second skill.\n---\n\n# Two\n",
            )

            result = validate_policy.validate_repository(root)

            self.assertFalse(result.ok)
            self.assertTrue(
                any("Duplicate skill name" in item.message for item in result.errors)
            )

    def test_broken_and_escaping_links_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_skill(
                root,
                "links",
                "---\nname: links\ndescription: Link checks.\n---\n\n"
                "See [missing](references/missing.md) and [escape](../../../../etc/passwd).\n",
            )

            result = validate_policy.validate_repository(root)

            self.assertFalse(result.ok)
            messages = " ".join(item.message for item in result.errors)
            self.assertIn("Broken local markdown link", messages)
            self.assertIn("Markdown link escapes the repository", messages)

    def test_forbidden_policy_names_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_config(root, forbidden=["blocked-policy"])
            self._write_rule(
                root,
                "blocked-policy.mdc",
                "---\ndescription: Blocked\nalwaysApply: true\n---\n",
            )

            result = validate_policy.validate_repository(root)

            self.assertFalse(result.ok)
            self.assertTrue(
                any(
                    "forbidden by repository config" in item.message
                    for item in result.errors
                )
            )

    def test_unknown_policy_config_keys_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = root / ".cursor" / "policy-config.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps({"extraClaudePostToolUseCommandHooks": []}) + "\n",
                encoding="utf-8",
            )
            self._write_rule(
                root,
                "demo.mdc",
                "---\ndescription: Demo\nalwaysApply: true\n---\n\n# Demo\n",
            )

            result = validate_policy.validate_repository(root)

            self.assertFalse(result.ok)
            self.assertTrue(
                any(
                    "Invalid policy config" in item.message
                    for item in result.errors
                )
            )

    def test_load_policy_config_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.assertEqual(
                policy_config.load_policy_config(root),
                {"forbiddenPolicyNames": []},
            )

    @staticmethod
    def _write_rule(root: Path, name: str, content: str) -> Path:
        path = root / ".cursor" / "rules" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    @staticmethod
    def _write_skill(root: Path, name: str, content: str) -> Path:
        path = root / ".cursor" / "skills" / name
        path.mkdir(parents=True, exist_ok=True)
        (path / "SKILL.md").write_text(content, encoding="utf-8")
        return path

    @staticmethod
    def _write_agent(root: Path, name: str) -> Path:
        path = root / ".cursor" / "agents" / f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"---\nname: {name}\ndescription: Demo agent.\nmodel: inherit\n"
            "readonly: true\nis_background: true\n---\n\n# Agent\n\nInspect only.\n",
            encoding="utf-8",
        )
        return path

    @staticmethod
    def _write_config(
        root: Path,
        *,
        forbidden: list[str] | None = None,
    ) -> None:
        """Write a complete temporary repository overlay."""
        path = root / ".cursor/policy-config.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"forbiddenPolicyNames": forbidden or []}, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
