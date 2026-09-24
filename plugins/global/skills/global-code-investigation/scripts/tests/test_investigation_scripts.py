"""Tests for global-code-investigation utility scripts."""

from __future__ import annotations

import base64
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import repo_map  # noqa: E402
import symbol_evidence  # noqa: E402


class RepositoryMapTests(unittest.TestCase):
    def test_snapshot_identifies_high_signal_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write(root / "AGENTS.md", "# Instructions")
            self._write(root / "package.json", "{}")
            self._write(root / "src" / "service.py", "def run():\n    return True\n")
            self._write(root / "tests" / "test_service.py", "def test_run():\n    pass\n")
            self._write(root / "migrations" / "001.sql", "SELECT 1;\n")
            self._write(root / "docs" / "guide.md", "# Guide")
            self._write(
                root / ".cursor" / "skills" / "external" / "SKILL.md",
                "# External skill",
            )
            self._write(root / "node_modules" / "package" / "index.js", "ignored")

            snapshot = repo_map.build_snapshot(root)

            self.assertEqual(snapshot["file_count"], 6)
            self.assertEqual(snapshot["collection_mode"], "filesystem fallback")
            self.assertIn("AGENTS.md", snapshot["categories"]["instructions"])
            self.assertIn("package.json", snapshot["categories"]["manifests"])
            self.assertIn("tests/test_service.py", snapshot["categories"]["tests"])
            self.assertIn("migrations/001.sql", snapshot["categories"]["migrations"])
            self.assertEqual(snapshot["languages"]["Python"], 2)
            self.assertFalse(snapshot["working_tree"]["available"])

    def test_git_inventory_excludes_tracked_generated_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write(root / "src" / "service.py", "VALUE = 1\n")
            self._write(root / "node_modules" / "package" / "index.js", "tracked")
            subprocess.run(
                ["git", "init", "-q"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "add", "-f", "src/service.py", "node_modules/package/index.js"],
                cwd=root,
                check=True,
            )

            snapshot = repo_map.build_snapshot(root)

            self.assertEqual(snapshot["collection_mode"], "git")
            self.assertEqual(snapshot["file_count"], 1)
            self.assertEqual(snapshot["languages"], {"Python": 1})

    @staticmethod
    def _write(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class SymbolEvidenceTests(unittest.TestCase):
    def test_report_categorizes_definition_tests_wiring_and_docs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write(root / "src" / "models.py", "class Widget:\n    pass\n")
            self._write(
                root / "src" / "registry.py",
                "registry.register(Widget)\n",
            )
            self._write(
                root / "tests" / "test_widget.py",
                "def test_widget():\n    assert Widget\n",
            )
            self._write(root / "docs" / "widgets.md", "Use Widget for examples.\n")

            report = symbol_evidence.build_report(root, "Widget", word=True)

            categories = report["categories"]
            self.assertEqual(categories["definitions"][0]["path"], "src/models.py")
            self.assertEqual(categories["tests"][0]["path"], "tests/test_widget.py")
            self.assertEqual(categories["wiring"][0]["path"], "src/registry.py")
            self.assertEqual(categories["documentation"][0]["path"], "docs/widgets.md")
            self.assertIn(
                "tests/test_widget.py",
                report["filename_matches"]["entries"],
            )
            self.assertEqual(report["collected_match_count"], 4)
            self.assertFalse(report["search_truncated"])

    def test_hidden_files_are_searched_and_globs_scope_filenames(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write(root / ".github" / "Widget.yaml", "name: Widget\n")
            self._write(root / "src" / "Widget.py", "Widget = object()\n")
            self._write(root / "docs" / "Widget.md", "Widget documentation\n")

            report = symbol_evidence.build_report(
                root,
                "Widget",
                globs=["*.py"],
            )

            self.assertEqual(report["collected_match_count"], 1)
            self.assertEqual(
                report["filename_matches"]["entries"],
                ["src/Widget.py"],
            )

            hidden_report = symbol_evidence.build_report(
                root,
                "Widget",
                globs=["*.yaml"],
            )
            self.assertEqual(hidden_report["collected_match_count"], 1)
            self.assertEqual(
                hidden_report["filename_matches"]["entries"],
                [".github/Widget.yaml"],
            )

    def test_global_match_bound_is_reported_as_partial(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for index in range(3):
                self._write(root / "src" / f"module_{index}.py", "SharedSymbol\n")

            report = symbol_evidence.build_report(
                root,
                "SharedSymbol",
                max_matches=2,
            )

            self.assertEqual(report["collected_match_count"], 2)
            self.assertTrue(report["search_truncated"])

    def test_exact_match_bound_is_not_reported_as_partial(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write(root / "src" / "module.py", "SharedSymbol\n")

            report = symbol_evidence.build_report(
                root,
                "SharedSymbol",
                max_matches=1,
            )

            self.assertEqual(report["collected_match_count"], 1)
            self.assertFalse(report["search_truncated"])

    def test_documentation_examples_are_not_definitions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write(root / "docs" / "example.md", "class Widget:\n")

            report = symbol_evidence.build_report(root, "Widget")

            self.assertFalse(report["categories"]["definitions"])
            self.assertEqual(
                report["categories"]["documentation"][0]["path"],
                "docs/example.md",
            )

    def test_byte_values_and_excerpts_are_safely_normalized(self) -> None:
        encoded = base64.b64encode("value\x00`<tag>`".encode()).decode()

        decoded = symbol_evidence._decode_rg_value({"bytes": encoded})
        excerpt = symbol_evidence._safe_excerpt(decoded)

        self.assertEqual(decoded, "value\x00`<tag>`")
        self.assertEqual(excerpt, "value \\`&lt;tag&gt;\\`")

    def test_external_command_failures_are_explicit(self) -> None:
        failure = subprocess.CompletedProcess([], 2, "", "command failed")
        with mock.patch.object(symbol_evidence, "_run", return_value=failure):
            filenames = symbol_evidence.filename_matches(
                Path("."),
                "Widget",
                (),
                5,
            )
            history = symbol_evidence.history_matches(Path("."), "Widget", 5)

        self.assertFalse(filenames["available"])
        self.assertEqual(filenames["error"], "command failed")
        self.assertFalse(history["available"])
        self.assertEqual(history["error"], "command failed")

    @staticmethod
    def _write(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
