"""Tests for the coding-workflow stop-gate hooks."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parents[1]


def _load(name: str, filename: str):
    path = HOOKS_DIR / filename
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
    return module


gate = _load("workflow_gate_under_test", "framework-workflow-gate.py")


class OwnerTestDirTests(unittest.TestCase):
    def test_addon_source_maps_to_addon_tests(self) -> None:
        self.assertEqual(
            gate._owner_test_dir("addons/example/api/components/models/lead.py"),
            "addons/example/api/tests",
        )

    def test_nested_addon_source_maps_to_nested_owner_tests(self) -> None:
        self.assertEqual(
            gate._owner_test_dir(
                "addons/enterprise/example/api/components/models/lead.py"
            ),
            "addons/enterprise/example/api/tests",
        )
        self.assertEqual(
            gate._runtime_test_dir("addons/community/example/gui/index.js"),
            "addons/community/example/gui/tests",
        )

    def test_api_runtime_maps_to_runtime_tests(self) -> None:
        self.assertEqual(
            gate._owner_test_dir("framework/runtimes/api/app/registry/service.py"),
            "framework/runtimes/api/tests",
        )

    def test_mcp_runtime_maps_to_runtime_tests(self) -> None:
        self.assertEqual(
            gate._owner_test_dir("framework/runtimes/mcp/app/discovery.py"),
            "framework/runtimes/mcp/tests",
        )

    def test_framework_package_maps_to_its_tests(self) -> None:
        self.assertEqual(
            gate._owner_test_dir("framework/runtimes/api/app/factory.py"),
            "framework/runtimes/api/tests",
        )

    def test_system_addon_maps_to_system_tests(self) -> None:
        self.assertEqual(
            gate._owner_test_dir("framework/addons/system/api/foo.py"),
            "framework/addons/system/api/tests",
        )

    def test_custom_addon_root_maps_to_addon_tests(self) -> None:
        self.assertEqual(
            gate._owner_test_dir("addons/example/api/components/models/record.py"),
            "addons/example/api/tests",
        )

    def test_operator_script_maps_to_scripts_tests(self) -> None:
        self.assertEqual(
            gate._owner_test_dir("scripts/workspace/sync_operator_env.py"),
            "scripts/tests",
        )

    def test_unowned_path_returns_none(self) -> None:
        self.assertIsNone(gate._owner_test_dir("applications/api/wsgi.py"))


class PythonTargetTests(unittest.TestCase):
    def test_source_change_selects_owning_tests_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "addons/example/api/tests").mkdir(parents=True)
            targets = gate._python_targets(
                root, ["addons/example/api/components/models/lead.py"]
            )
            self.assertEqual(targets, ["addons/example/api/tests"])

    def test_addon_runtime_change_selects_that_runtime_tests_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "addons/example/mcp/tests").mkdir(parents=True)
            (root / "addons/example/api/tests").mkdir(parents=True)
            targets = gate._python_targets(
                root,
                ["addons/example/mcp/utils/engine.py"],
            )
            self.assertEqual(targets, ["addons/example/mcp/tests"])

    def test_addon_runtime_without_own_tests_falls_back_to_api_tests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "addons/example/api/tests").mkdir(parents=True)
            targets = gate._python_targets(
                root,
                ["addons/example/mcp/utils/engine.py"],
            )
            self.assertEqual(targets, ["addons/example/api/tests"])

    def test_touched_test_file_is_selected_directly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            test_file = root / "addons/example/api/tests/test_lead.py"
            test_file.parent.mkdir(parents=True)
            test_file.write_text("def test_x():\n    assert True\n", encoding="utf-8")
            targets = gate._python_targets(root, ["addons/example/api/tests/test_lead.py"])
            self.assertEqual(targets, ["addons/example/api/tests/test_lead.py"])

    def test_missing_tests_dir_yields_no_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            targets = gate._python_targets(
                root,
                ["addons/example_missing/api/x.py"],
            )
            self.assertEqual(targets, [])

    def test_generated_and_migration_paths_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "addons/example/api/tests").mkdir(parents=True)
            targets = gate._python_targets(
                root,
                [
                    "addons/example/api/migrations/versions/abc_init.py",
                    "docs/sphinx/source/code/addons/example/index.py",
                ],
            )
            self.assertEqual(targets, [])


class GuiTouchedTests(unittest.TestCase):
    def test_gui_runtime_source_triggers(self) -> None:
        self.assertTrue(gate._gui_touched(["framework/runtimes/gui/src/App.jsx"]))

    def test_addon_gui_source_triggers(self) -> None:
        self.assertTrue(gate._gui_touched(["addons/example/gui/components/Board.js"]))

    def test_generated_gui_ignored(self) -> None:
        self.assertFalse(
            gate._gui_touched(["framework/runtimes/gui/src/addonGui.generated.js"])
        )

    def test_python_change_does_not_trigger(self) -> None:
        self.assertFalse(gate._gui_touched(["addons/example/api/components/x.py"]))


class GuiTargetTests(unittest.TestCase):
    def test_addon_gui_change_selects_owner_gui_tests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "addons/community/example/gui/tests").mkdir(parents=True)
            targets = gate._gui_targets(
                root,
                ["addons/community/example/gui/components/Board.jsx"],
            )
            self.assertEqual(targets, ["addons/community/example/gui/tests"])

    def test_framework_gui_change_selects_full_suite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "addons/example/gui/tests").mkdir(parents=True)
            targets = gate._gui_targets(
                root,
                [
                    "framework/runtimes/gui/src/App.jsx",
                    "addons/example/gui/components/Board.jsx",
                ],
            )
            self.assertIsNone(targets)

    def test_missing_owner_gui_tests_yields_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            targets = gate._gui_targets(
                root,
                ["addons/example/gui/components/Board.jsx"],
            )
            self.assertEqual(targets, [])


class PlanChecksTests(unittest.TestCase):
    def test_any_change_runs_custom_addon_isolation_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "scripts" / "addon" / "check_addon_isolation.py"
            script.parent.mkdir(parents=True)
            script.write_text("", encoding="utf-8")

            checks = gate.plan_checks(root, ["README.md"])

            self.assertEqual(len(checks), 1)
            label, command, cwd, _env = checks[0]
            self.assertEqual(label, "custom addon isolation")
            self.assertEqual(command, [gate._python_bin(root), str(script)])
            self.assertEqual(cwd, root)

    def test_python_check_uses_pytest_with_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "addons/example/api/tests").mkdir(parents=True)
            checks = gate.plan_checks(
                root, ["addons/example/api/components/models/lead.py"]
            )
            self.assertEqual(len(checks), 1)
            label, command, cwd, _env = checks[0]
            self.assertIn("pytest", label)
            self.assertIn("-m", command)
            self.assertIn("pytest", command)
            self.assertIn("addons/example/api/tests", command)
            self.assertEqual(cwd, root)

    def test_gui_change_without_node_modules_skips(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checks = gate.plan_checks(root, ["framework/runtimes/gui/src/App.jsx"])
            self.assertEqual(checks, [])

    def test_addon_gui_change_scopes_vitest_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gui_root = root / "framework" / "runtimes" / "gui"
            (gui_root / "node_modules").mkdir(parents=True)
            (root / "addons/community/example/gui/tests").mkdir(parents=True)
            checks = gate.plan_checks(
                root,
                ["addons/community/example/gui/components/Board.jsx"],
            )
            self.assertEqual(len(checks), 1)
            label, command, cwd, _env = checks[0]
            self.assertIn("addons/community/example/gui/tests", label)
            self.assertIn("--", command)
            expected = str(
                (root / "addons/community/example/gui/tests").resolve()
            )
            self.assertIn(expected, command)
            self.assertEqual(cwd, gui_root)


class QualityReminderTests(unittest.TestCase):
    def test_below_threshold_returns_none(self) -> None:
        record = {"deslop_announced": False}
        changed = ["addons/example/api/a.py", "addons/example/api/b.py"]
        self.assertIsNone(gate.quality_reminder(record, changed))

    def test_threshold_crossed_returns_reminder(self) -> None:
        record = {"deslop_announced": False}
        changed = [f"addons/example/api/f{i}.py" for i in range(gate.QUALITY_FILE_THRESHOLD)]
        message = gate.quality_reminder(record, changed)
        self.assertIsNotNone(message)
        self.assertIn("deslop suite", message)

    def test_generated_files_excluded_from_count(self) -> None:
        record = {"deslop_announced": False}
        changed = [
            "framework/runtimes/gui/src/addonGui.generated.js",
            "addons/example/api/migrations/versions/x.py",
        ] + [f"addons/example/api/f{i}.py" for i in range(gate.QUALITY_FILE_THRESHOLD - 1)]
        self.assertIsNone(gate.quality_reminder(record, changed))

    def test_announced_suppresses_reminder(self) -> None:
        record = {"deslop_announced": True}
        changed = [f"addons/example/api/f{i}.py" for i in range(gate.QUALITY_FILE_THRESHOLD)]
        self.assertIsNone(gate.quality_reminder(record, changed))

    def test_emitting_reminder_marks_announced_once(self) -> None:
        """Stop-hook follow-up must not re-fire every turn until a sentinel echo."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            conversation_id = "conv-deslop-once"
            gate.ws.update(
                root,
                conversation_id,
                lambda record: record["files"].extend(
                    [f"addons/example/api/f{i}.py" for i in range(gate.QUALITY_FILE_THRESHOLD)]
                ),
            )
            record = gate.ws.load(root, conversation_id)
            self.assertFalse(record["deslop_announced"])
            changed = list(record["files"])
            reminder = gate.quality_reminder(record, changed)
            self.assertIsNotNone(reminder)
            gate.ws.update(root, conversation_id, gate._mark_deslop_announced)
            again = gate.ws.load(root, conversation_id)
            self.assertTrue(again["deslop_announced"])
            self.assertIsNone(gate.quality_reminder(again, changed))


class ChangedSetTests(unittest.TestCase):
    """The gate attributes only this conversation's work, not pre-existing dirt."""

    def setUp(self) -> None:
        self._real_git_dirty = gate.ws.git_dirty

    def tearDown(self) -> None:
        gate.ws.git_dirty = self._real_git_dirty

    def _with_dirty(self, dirty: set[str]) -> None:
        gate.ws.git_dirty = lambda root: set(dirty)

    def test_preexisting_dirt_is_excluded(self) -> None:
        self._with_dirty({
            "addons/example_existing/api/x.py",
            "framework/runtimes/api/app/y.py",
        })
        record = {
            "files": [],
            "unverified": [],
            "baseline": [
                "addons/example_existing/api/x.py",
                "framework/runtimes/api/app/y.py",
            ],
        }
        self.assertEqual(gate._changed_set(Path("/repo"), record), [])

    def test_new_dirt_after_baseline_is_attributed(self) -> None:
        self._with_dirty({
            "addons/example_existing/api/x.py",
            "addons/example/api/new.py",
        })
        record = {
            "files": [],
            "unverified": [],
            "baseline": ["addons/example_existing/api/x.py"],
        }
        self.assertEqual(
            gate._changed_set(Path("/repo"), record), ["addons/example/api/new.py"]
        )

    def test_recorded_edit_survives_baseline_overlap(self) -> None:
        self._with_dirty({"addons/example/api/edited.py"})
        record = {
            "files": ["addons/example/api/edited.py"],
            "unverified": ["addons/example/api/edited.py"],
            "baseline": ["addons/example/api/edited.py"],
        }
        self.assertEqual(
            gate._changed_set(Path("/repo"), record), ["addons/example/api/edited.py"]
        )

    def test_state_dir_is_never_attributed(self) -> None:
        self._with_dirty({f"{gate.ws.STATE_DIR}/conv.json"})
        record = {"files": [], "unverified": [], "baseline": []}
        self.assertEqual(gate._changed_set(Path("/repo"), record), [])


class BaselineCaptureTests(unittest.TestCase):
    def test_first_write_snapshots_dirty_set(self) -> None:
        state = _load("framework_workflow_state_under_test", "framework_workflow_state.py")
        real_git_dirty = state.git_dirty
        state.git_dirty = lambda root: {"preexisting/refactor.py"}
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                state.update(root, "conv", lambda record: record["files"].append("a.py"))
                first = state.load(root, "conv")
                self.assertEqual(first["baseline"], ["preexisting/refactor.py"])

                state.git_dirty = lambda root: {"preexisting/refactor.py", "later.py"}
                state.update(root, "conv", lambda record: record["files"].append("b.py"))
                second = state.load(root, "conv")
                self.assertEqual(second["baseline"], ["preexisting/refactor.py"])
        finally:
            state.git_dirty = real_git_dirty


class RecorderSubprocessTests(unittest.TestCase):
    def _run(
        self,
        script: str,
        payload: object,
        root: Path,
    ) -> subprocess.CompletedProcess:
        """Run one hook with Cursor's project environment.

        Args:
            script: Hook basename under ``.cursor/hooks``.
            payload: JSON-serializable stdin event.
            root: Temporary repository root exported as ``CURSOR_PROJECT_DIR``.

        Returns:
            Completed subprocess result.
        """
        return subprocess.run(
            [sys.executable, str(HOOKS_DIR / script)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env={"CURSOR_PROJECT_DIR": str(root), "PATH": ""},
        )

    def test_record_edit_writes_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = {
                "conversation_id": "conv-1",
                "file_path": str(root / "addons/example/api/x.py"),
            }
            completed = self._run("framework-record-edit.py", payload, root)
            self.assertEqual(completed.returncode, 0)
            state = json.loads(
                (root / ".cursor/.workflow-state/conv-1.json").read_text()
            )
            self.assertIn("addons/example/api/x.py", state["files"])
            self.assertIn("addons/example/api/x.py", state["unverified"])

    def test_record_response_sets_deslop_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = {
                "conversation_id": "conv-2",
                "text": "Deslop suite: phase A complete.",
            }
            completed = self._run("framework-record-response.py", payload, root)
            self.assertEqual(completed.returncode, 0)
            state = json.loads(
                (root / ".cursor/.workflow-state/conv-2.json").read_text()
            )
            self.assertTrue(state["deslop_announced"])

    def test_malformed_stdin_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            completed = subprocess.run(
                [sys.executable, str(HOOKS_DIR / "framework-record-edit.py")],
                input="not json",
                capture_output=True,
                text=True,
                env={"CURSOR_PROJECT_DIR": str(root), "PATH": ""},
            )
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(completed.stdout.strip(), "{}")

    def test_record_edit_under_configured_worktree(self) -> None:
        """Edits under WORKTREE_DIR/<name>/ are recorded on the live state file."""
        with tempfile.TemporaryDirectory() as tmp:
            live = Path(tmp) / "live"
            trees = Path(tmp) / "trees"
            wt = trees / "ISSUE-99"
            live.mkdir()
            wt.mkdir(parents=True)
            (wt / "framework").mkdir()
            (wt / ".git").mkdir()
            target = wt / "addons" / "example" / "api" / "x.py"
            target.parent.mkdir(parents=True)
            target.write_text("x=1\n", encoding="utf-8")
            (live / "project.env").write_text(f"WORKTREE_DIR={trees}\n", encoding="utf-8")

            payload = {
                "conversation_id": "wt-1",
                "file_path": str(target),
            }
            completed = self._run("framework-record-edit.py", payload, live)
            self.assertEqual(completed.returncode, 0)
            state = json.loads(
                (live / ".cursor/.workflow-state/wt-1.json").read_text()
            )
            self.assertIn("ISSUE-99", state.get("worktrees", {}))
            entry = state["worktrees"]["ISSUE-99"]
            self.assertIn("addons/example/api/x.py", entry["files"])

    def test_record_edit_under_linked_worktree_without_env(self) -> None:
        """Edits in a linked worktree are recorded when WORKTREE_DIR is blank."""
        with tempfile.TemporaryDirectory() as tmp:
            live = Path(tmp) / "live"
            live.mkdir()
            subprocess.run(
                ["git", "init", "-b", "main"],
                cwd=live,
                check=True,
                capture_output=True,
            )
            (live / "README").write_text("a\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", "README"],
                cwd=live,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.email=t@example.com",
                    "-c",
                    "user.name=t",
                    "commit",
                    "-m",
                    "init",
                ],
                cwd=live,
                check=True,
                capture_output=True,
            )
            wt = Path(tmp) / "cursorish" / "ISSUE-7"
            subprocess.run(
                ["git", "worktree", "add", "-b", "ISSUE-7", str(wt), "HEAD"],
                cwd=live,
                check=True,
                capture_output=True,
            )
            target = wt / "addons" / "example" / "api" / "x.py"
            target.parent.mkdir(parents=True)
            target.write_text("x=1\n", encoding="utf-8")
            (live / "project.env").write_text("WORKTREE_DIR=\n", encoding="utf-8")

            completed = self._run(
                "framework-record-edit.py",
                {"conversation_id": "wt-link", "file_path": str(target)},
                live,
            )
            self.assertEqual(completed.returncode, 0)
            state = json.loads(
                (live / ".cursor/.workflow-state/wt-link.json").read_text()
            )
            self.assertIn("ISSUE-7", state.get("worktrees", {}))
            entry = state["worktrees"]["ISSUE-7"]
            self.assertIn("addons/example/api/x.py", entry["files"])
            self.assertEqual(state.get("files") or [], [])

    def test_record_edit_ignores_foreign_worktree_without_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            live = Path(tmp) / "live"
            trees = Path(tmp) / "trees"
            wt = trees / "ISSUE-99"
            live.mkdir()
            wt.mkdir(parents=True)
            (wt / "framework").mkdir()
            target = wt / "addons" / "example" / "api" / "x.py"
            target.parent.mkdir(parents=True)
            target.write_text("x=1\n", encoding="utf-8")
            (live / "project.env").write_text("WORKTREE_DIR=\n", encoding="utf-8")

            payload = {
                "conversation_id": "wt-off",
                "file_path": str(target),
            }
            completed = self._run("framework-record-edit.py", payload, live)
            self.assertEqual(completed.returncode, 0)
            state_path = live / ".cursor/.workflow-state/wt-off.json"
            if state_path.is_file():
                state = json.loads(state_path.read_text())
                self.assertEqual(state.get("worktrees") or {}, {})
                self.assertEqual(state.get("files") or [], [])


class GateStatusTests(unittest.TestCase):
    def test_non_completed_status_emits_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            completed = subprocess.run(
                [sys.executable, str(HOOKS_DIR / "framework-workflow-gate.py")],
                input=json.dumps({"status": "aborted", "conversation_id": "c"}),
                capture_output=True,
                text=True,
                env={"CURSOR_PROJECT_DIR": str(root), "PATH": ""},
            )
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(json.loads(completed.stdout), {})


if __name__ == "__main__":
    unittest.main()
