#!/usr/bin/env python3
"""Verify generic framework MCP health metadata."""

from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Sequence
from typing import Any

LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
MAX_RESPONSE_BYTES = 1024 * 1024


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Refuse redirects so a validated local URL cannot escape its host gate."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


def validate_url(raw_url: str, *, allow_remote: bool) -> str:
    """Validate a health URL and return its normalized form."""
    parsed = urllib.parse.urlparse(raw_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("health URL must use http or https")
    if not parsed.hostname:
        raise ValueError("health URL must include a hostname")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("health URL must not include credentials, query, or fragment")
    if not allow_remote and parsed.hostname.lower() not in LOCAL_HOSTS:
        raise ValueError("remote health URL requires --allow-remote")
    return urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/healthz",
            "",
            "",
            "",
        )
    )


def fetch_health(url: str, *, timeout: float) -> dict[str, Any]:
    """Fetch and decode one MCP health response."""
    request = urllib.request.Request(  # noqa: S310 - URL is validated by caller.
        url,
        headers={"Accept": "application/json"},
        method="GET",
    )
    opener = urllib.request.build_opener(NoRedirectHandler())
    try:
        with opener.open(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"health request returned HTTP {exc.code}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"health request failed: {exc}") from exc
    if not 200 <= status < 300:
        raise RuntimeError(f"health request returned HTTP {status}")
    if len(body) > MAX_RESPONSE_BYTES:
        raise RuntimeError(
            f"health response exceeds maximum size of {MAX_RESPONSE_BYTES} bytes"
        )
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("health response is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("health response must be a JSON object")
    return payload


def validate_payload(
    payload: dict[str, Any],
    *,
    expected_server: str | None,
    expected_packs: set[str],
    exact_packs: bool,
    expected_auth: str,
) -> list[str]:
    """Return contract errors found in MCP health metadata."""
    errors: list[str] = []
    if payload.get("status") != "ok":
        errors.append("status must be 'ok'")
    if payload.get("check") != "liveness":
        errors.append("check must be 'liveness'")
    if expected_server and payload.get("server") != expected_server:
        errors.append(f"server must be {expected_server!r}")

    packs, pack_errors = _pack_names(payload)
    errors.extend(pack_errors)
    missing = sorted(expected_packs - packs)
    if missing:
        errors.append(f"missing expected packs: {', '.join(missing)}")
    unexpected = sorted(packs - expected_packs)
    if exact_packs and unexpected:
        errors.append(f"unexpected packs loaded: {', '.join(unexpected)}")

    auth_enabled = payload.get("api_key_auth_enabled")
    if expected_auth == "enabled" and auth_enabled is not True:
        errors.append("API key auth must be enabled")
    if expected_auth == "disabled" and auth_enabled is not False:
        errors.append("API key auth must be disabled")
    return errors


def _pack_names(payload: dict[str, Any]) -> tuple[set[str], list[str]]:
    raw_packs = payload.get("packs")
    if not isinstance(raw_packs, list):
        return set(), ["packs must be a list"]

    names: set[str] = set()
    errors: list[str] = []
    for index, item in enumerate(raw_packs):
        if not isinstance(item, dict):
            errors.append(f"packs[{index}] must be an object")
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"packs[{index}].name must be a non-empty string")
            continue
        names.add(name.strip())
    return names, errors


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify framework MCP /healthz metadata."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Health URL, normally http://127.0.0.1:<port>/healthz.",
    )
    parser.add_argument("--expected-server", help="Expected MCP server name.")
    parser.add_argument(
        "--expected-pack",
        action="append",
        default=[],
        help="Expected loaded pack name; repeat for multiple packs.",
    )
    parser.add_argument(
        "--exact-packs",
        action="store_true",
        help="Reject loaded packs not named by --expected-pack.",
    )
    parser.add_argument(
        "--expect-auth",
        choices=("any", "enabled", "disabled"),
        default="any",
        help="Expected API-key ingress state.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Request timeout in seconds (default: 5).",
    )
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help="Allow a non-loopback health URL.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the MCP health verification CLI."""
    args = _build_parser().parse_args(argv)
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        print("--timeout must be finite and greater than zero", file=sys.stderr)
        return 1
    try:
        url = validate_url(args.url, allow_remote=args.allow_remote)
        payload = fetch_health(url, timeout=args.timeout)
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    errors = validate_payload(
        payload,
        expected_server=args.expected_server,
        expected_packs=set(args.expected_pack),
        exact_packs=args.exact_packs,
        expected_auth=args.expect_auth,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    pack_names, _pack_errors = _pack_names(payload)
    print(
        "MCP health verified: "
        f"server={payload.get('server')!r} "
        f"packs={','.join(sorted(pack_names)) or '(none)'} "
        f"auth_enabled={payload.get('api_key_auth_enabled')!r}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
