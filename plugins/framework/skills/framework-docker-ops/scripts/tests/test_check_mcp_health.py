"""Tests for bounded, secret-safe MCP health validation."""

from __future__ import annotations

import contextlib
import io
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


def _load_module():
    path = Path(__file__).resolve().parents[1] / "check_mcp_health.py"
    module = types.ModuleType("check_mcp_health")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(path.read_text(), str(path), "exec"), module.__dict__)
    return module


check_mcp_health = _load_module()


class _FakeResponse:
    def __init__(self, body: bytes, *, status: int = 200) -> None:
        self.body = body
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        return self.body if size < 0 else self.body[:size]


class CheckMcpHealthTests(unittest.TestCase):
    def test_validate_url_rejects_remote_by_default(self) -> None:
        with self.assertRaisesRegex(ValueError, "requires --allow-remote"):
            check_mcp_health.validate_url(
                "https://mcp.example.test/healthz",
                allow_remote=False,
            )

    def test_validate_url_normalizes_local_default_path(self) -> None:
        self.assertEqual(
            check_mcp_health.validate_url(
                "http://[::1]:8002",
                allow_remote=False,
            ),
            "http://[::1]:8002/healthz",
        )

    def test_validate_url_rejects_sensitive_or_ambiguous_components(self) -> None:
        invalid_urls = (
            "http://user:secret@localhost/healthz",
            "http://localhost/healthz?token=secret",
            "http://localhost/healthz#fragment",
            "file:///healthz",
        )

        for url in invalid_urls:
            with self.subTest(url=url), self.assertRaises(ValueError):
                check_mcp_health.validate_url(url, allow_remote=False)

    def test_validate_payload_accepts_expected_contract(self) -> None:
        payload = {
            "status": "ok",
            "check": "liveness",
            "server": "mcp-example",
            "packs": [{"name": "example", "version": "0.1.0"}],
            "api_key_auth_enabled": True,
        }

        errors = check_mcp_health.validate_payload(
            payload,
            expected_server="mcp-example",
            expected_packs={"example"},
            exact_packs=True,
            expected_auth="enabled",
        )

        self.assertEqual(errors, [])

    def test_validate_payload_reports_pack_mismatches(self) -> None:
        payload = {
            "status": "ok",
            "check": "liveness",
            "packs": [{"name": "example"}],
            "api_key_auth_enabled": False,
        }

        errors = check_mcp_health.validate_payload(
            payload,
            expected_server=None,
            expected_packs={"expected"},
            exact_packs=True,
            expected_auth="any",
        )

        self.assertEqual(
            errors,
            [
                "missing expected packs: expected",
                "unexpected packs loaded: example",
            ],
        )

    def test_validate_payload_rejects_malformed_packs(self) -> None:
        payload = {
            "status": "ok",
            "check": "liveness",
            "packs": None,
            "api_key_auth_enabled": False,
        }

        errors = check_mcp_health.validate_payload(
            payload,
            expected_server=None,
            expected_packs=set(),
            exact_packs=False,
            expected_auth="any",
        )

        self.assertEqual(errors, ["packs must be a list"])

    def test_fetch_health_disables_redirects_and_bounds_response(self) -> None:
        oversized = b"{" + (b"x" * check_mcp_health.MAX_RESPONSE_BYTES)
        opener = mock.Mock()
        opener.open.return_value = _FakeResponse(oversized)

        with (
            mock.patch.object(
                check_mcp_health.urllib.request,
                "build_opener",
                return_value=opener,
            ) as build_opener,
            self.assertRaisesRegex(RuntimeError, "maximum size"),
        ):
            check_mcp_health.fetch_health(
                "http://127.0.0.1:8002/healthz",
                timeout=5.0,
            )

        handler = build_opener.call_args.args[0]
        self.assertIsInstance(handler, check_mcp_health.NoRedirectHandler)
        self.assertEqual(
            opener.open.call_args.kwargs["timeout"],
            5.0,
        )

    def test_redirect_handler_refuses_redirects(self) -> None:
        handler = check_mcp_health.NoRedirectHandler()

        redirected = handler.redirect_request(
            mock.Mock(),
            mock.Mock(),
            302,
            "Found",
            {},
            "https://remote.example.test/healthz",
        )

        self.assertIsNone(redirected)

    def test_validate_payload_reports_liveness_server_and_auth_mismatches(
        self,
    ) -> None:
        payload = {
            "status": "degraded",
            "check": "readiness",
            "server": "wrong-server",
            "packs": [],
            "api_key_auth_enabled": False,
        }

        errors = check_mcp_health.validate_payload(
            payload,
            expected_server="expected-server",
            expected_packs=set(),
            exact_packs=False,
            expected_auth="enabled",
        )

        self.assertEqual(
            errors,
            [
                "status must be 'ok'",
                "check must be 'liveness'",
                "server must be 'expected-server'",
                "API key auth must be enabled",
            ],
        )

    def test_main_rejects_invalid_url_before_request(self) -> None:
        stderr = io.StringIO()

        with (
            mock.patch.object(check_mcp_health, "fetch_health") as fetch_health,
            contextlib.redirect_stderr(stderr),
        ):
            result = check_mcp_health.main(
                ["--url", "https://mcp.example.test/healthz"]
            )

        self.assertEqual(result, 1)
        self.assertIn("requires --allow-remote", stderr.getvalue())
        fetch_health.assert_not_called()

    def test_main_rejects_nonfinite_timeout(self) -> None:
        stderr = io.StringIO()

        with (
            mock.patch.object(check_mcp_health, "fetch_health") as fetch_health,
            contextlib.redirect_stderr(stderr),
        ):
            result = check_mcp_health.main(
                [
                    "--url",
                    "http://127.0.0.1:8002/healthz",
                    "--timeout",
                    "nan",
                ]
            )

        self.assertEqual(result, 1)
        self.assertIn("finite", stderr.getvalue())
        fetch_health.assert_not_called()

    def test_main_prints_pack_names_in_deterministic_order(self) -> None:
        payload = {
            "status": "ok",
            "check": "liveness",
            "server": "mcp-example",
            "packs": [{"name": "zeta"}, {"name": "alpha"}],
            "api_key_auth_enabled": True,
        }
        stdout = io.StringIO()

        with (
            mock.patch.object(
                check_mcp_health,
                "fetch_health",
                return_value=payload,
            ),
            contextlib.redirect_stdout(stdout),
        ):
            result = check_mcp_health.main(
                [
                    "--url",
                    "http://127.0.0.1:8002/healthz",
                    "--expected-pack",
                    "alpha",
                    "--expected-pack",
                    "zeta",
                    "--exact-packs",
                ]
            )

        self.assertEqual(result, 0)
        self.assertIn("packs=alpha,zeta", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
