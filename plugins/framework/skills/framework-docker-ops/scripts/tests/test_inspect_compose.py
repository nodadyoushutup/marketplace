"""Tests for secret-safe, deterministic Compose inspection."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


def _load_module():
    path = Path(__file__).resolve().parents[1] / "inspect_compose.py"
    module = types.ModuleType("inspect_compose")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(path.read_text(), str(path), "exec"), module.__dict__)
    return module


inspect_compose = _load_module()


class InspectComposeTests(unittest.TestCase):
    def test_reports_framework_mcp_contract_risks(self) -> None:
        config = {
            "services": {
                "mcp-example": {
                    "build": {"dockerfile": "applications/mcp/Dockerfile"},
                    "environment": {"MCP_SERVER_NAME": "mcp"},
                    "ports": [{"target": 8080, "published": "8002"}],
                    "volumes": [
                        {
                            "type": "bind",
                            "source": "/repo/addons",
                            "target": "/app/addons",
                            "read_only": False,
                        }
                    ],
                }
            }
        }

        findings, summaries = inspect_compose.inspect_config(config)
        codes = {finding.code for finding in findings}

        self.assertEqual(summaries[0]["name"], "mcp-example")
        self.assertIn("healthcheck-missing", codes)
        self.assertIn("port-host-wide", codes)

    def test_digest_pinned_loopback_service_has_no_findings(self) -> None:
        config = {
            "services": {
                "example": {
                    "image": "example:1.0@sha256:" + ("a" * 64),
                    "healthcheck": {"test": ["CMD", "true"]},
                    "ports": [
                        {
                            "host_ip": "127.0.0.1",
                            "target": 8080,
                            "published": "8080",
                        }
                    ],
                }
            }
        }

        findings, _summaries = inspect_compose.inspect_config(config)

        self.assertEqual(findings, [])

    def test_local_build_output_name_is_not_treated_as_latest_input(self) -> None:
        config = {
            "services": {
                "example": {
                    "build": {
                        "context": "/repo",
                        "dockerfile": "applications/example/Dockerfile",
                    },
                    "image": "framework-example",
                    "pull_policy": "build",
                    "healthcheck": {"test": ["CMD", "true"]},
                }
            }
        }

        findings, _summaries = inspect_compose.inspect_config(config)

        self.assertNotIn(
            "image-latest",
            {finding.code for finding in findings},
        )

    def test_build_service_with_pullable_image_is_checked(self) -> None:
        config = {
            "services": {
                "example": {
                    "build": {"context": "/repo"},
                    "image": "registry.example.test/example:latest",
                    "pull_policy": "always",
                    "healthcheck": {"test": ["CMD", "true"]},
                }
            }
        }

        findings, _summaries = inspect_compose.inspect_config(config)

        self.assertIn("image-latest", {finding.code for finding in findings})

    def test_framework_mcp_warns_without_addons_mount(self) -> None:
        config = {
            "services": {
                "mcp-example": {
                    "build": {"dockerfile": "applications/mcp/Dockerfile"},
                    "environment": {
                        "MCP_SERVER_NAME": None,
                    },
                    "healthcheck": {"test": ["CMD", "true"]},
                    "volumes": [
                        {
                            "type": "bind",
                            "source": "/repo/not-addons",
                            "target": "/app/other",
                            "read_only": True,
                        }
                    ],
                }
            }
        }

        findings, _summaries = inspect_compose.inspect_config(config)
        codes = [finding.code for finding in findings]

        self.assertIn("mcp-addons-mount-missing", codes)

    def test_render_compose_bounds_execution_and_redacts_failure_output(self) -> None:
        failure = subprocess.CompletedProcess(
            args=["docker"],
            returncode=1,
            stdout="API_TOKEN=super-secret",
            stderr="bad value super-secret",
        )

        with (
            mock.patch.object(
                inspect_compose.subprocess,
                "run",
                return_value=failure,
            ) as run,
            self.assertRaisesRegex(RuntimeError, "exit code 1") as raised,
        ):
            inspect_compose.render_compose(Path("/repo/compose.yaml"))

        self.assertEqual(run.call_args.kwargs["timeout"], 30)
        self.assertNotIn("super-secret", str(raised.exception))

    def test_unknown_selected_service_is_an_error(self) -> None:
        findings, summaries = inspect_compose.inspect_config(
            {"services": {"api": {}}},
            selected_services={"missing"},
        )

        self.assertEqual(summaries, [])
        self.assertEqual(
            [(finding.level, finding.code) for finding in findings],
            [("error", "service-unknown")],
        )

    def test_missing_services_is_an_error(self) -> None:
        findings, summaries = inspect_compose.inspect_config({"services": {}})

        self.assertEqual(summaries, [])
        self.assertEqual(
            [(finding.level, finding.code) for finding in findings],
            [("error", "services-missing")],
        )

    def test_reports_latest_image_remote_build_and_cursor_mount(self) -> None:
        config = {
            "services": {
                "external-image": {
                    "image": "registry.example.test:5000/example:latest",
                    "healthcheck": {"test": ["CMD", "true"]},
                },
                "remote-build": {
                    "build": {
                        "context": "https://example.test/repository.git",
                    },
                    "healthcheck": {"test": ["CMD", "true"]},
                    "volumes": [
                        {
                            "type": "bind",
                            "source": "/repo/.cursor",
                            "target": "/workspace/.cursor",
                            "read_only": True,
                        }
                    ],
                }
            }
        }

        findings, _summaries = inspect_compose.inspect_config(config)

        self.assertEqual(
            {finding.code for finding in findings},
            {"cursor-mount", "image-latest", "remote-build-context"},
        )

    def test_json_output_does_not_expose_environment_values(self) -> None:
        config = {
            "services": {
                "example": {
                    "image": "example:1.0@sha256:" + ("a" * 64),
                    "healthcheck": {"test": ["CMD", "true"]},
                    "environment": {"API_TOKEN": "super-secret-value"},
                }
            }
        }
        stdout = io.StringIO()

        with tempfile.NamedTemporaryFile() as compose_file:
            with (
                mock.patch.object(
                    inspect_compose,
                    "render_compose",
                    return_value=config,
                ),
                contextlib.redirect_stdout(stdout),
            ):
                result = inspect_compose.main(
                    ["--file", compose_file.name, "--json"]
                )

        output = stdout.getvalue()
        payload = json.loads(output)
        self.assertEqual(result, 0)
        self.assertNotIn("super-secret-value", output)
        self.assertNotIn("environment", payload["services"][0])


if __name__ == "__main__":
    unittest.main()
