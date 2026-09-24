#!/usr/bin/env python3
"""Validate rendered Compose configuration and report framework risks."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

COMPOSE_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class Finding:
    """One actionable Compose inspection result."""

    level: str
    code: str
    service: str
    message: str


def repository_root() -> Path:
    """Return the repository root containing the project skill."""
    return Path(__file__).resolve().parents[4]


def render_compose(
    compose_file: Path,
    *,
    profiles: Sequence[str] = (),
) -> dict[str, Any]:
    """Render Compose configuration as JSON through the Docker CLI."""
    command = [
        "docker",
        "compose",
        "--project-directory",
        str(repository_root() / "docker"),
        "-f",
        str(compose_file),
    ]
    for profile in profiles:
        command.extend(["--profile", profile])
    command.extend(["config", "--format", "json"])
    try:
        result = subprocess.run(
            command,
            cwd=repository_root(),
            check=False,
            capture_output=True,
            text=True,
            timeout=COMPOSE_TIMEOUT_SECONDS,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("docker CLI is not installed or not on PATH") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"docker compose config exceeded {COMPOSE_TIMEOUT_SECONDS} seconds"
        ) from exc
    if result.returncode != 0:
        raise RuntimeError(
            "docker compose config failed "
            f"(exit code {result.returncode}); rerun it directly for diagnostics"
        )
    try:
        rendered = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("docker compose did not return valid JSON") from exc
    if not isinstance(rendered, dict):
        raise RuntimeError("rendered Compose configuration must be a JSON object")
    return rendered


def inspect_config(
    config: dict[str, Any],
    *,
    selected_services: set[str] | None = None,
) -> tuple[list[Finding], list[dict[str, Any]]]:
    """Return findings and secret-safe service summaries."""
    services = config.get("services")
    if not isinstance(services, dict) or not services:
        return (
            [
                Finding(
                    "error",
                    "services-missing",
                    "",
                    "rendered Compose configuration has no services",
                )
            ],
            [],
        )

    unknown = sorted((selected_services or set()) - set(services))
    findings = [
        Finding(
            "error",
            "service-unknown",
            service,
            "requested service is not present in rendered Compose configuration",
        )
        for service in unknown
    ]
    summaries: list[dict[str, Any]] = []

    for name, raw_service in sorted(services.items()):
        if selected_services and name not in selected_services:
            continue
        service = raw_service if isinstance(raw_service, dict) else {}
        findings.extend(_inspect_service(name, service))
        summaries.append(_service_summary(name, service))

    return findings, summaries


def _inspect_service(name: str, service: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    build = service.get("build")
    image = str(service.get("image") or "").strip()
    if image and _image_can_be_pulled(service) and "@sha256:" not in image:
        code = "image-latest" if _uses_latest_tag(image) else "image-not-digest"
        message = (
            "image uses a latest tag"
            if code == "image-latest"
            else "image is tag-pinned but not digest-pinned"
        )
        findings.append(Finding("warning", code, name, message))

    if not service.get("healthcheck"):
        findings.append(
            Finding(
                "warning",
                "healthcheck-missing",
                name,
                "service has no Compose healthcheck; verify whether one is required",
            )
        )

    for port in _as_dict_list(service.get("ports")):
        if port.get("published") and str(port.get("host_ip") or "") in {"", "0.0.0.0"}:
            findings.append(
                Finding(
                    "warning",
                    "port-host-wide",
                    name,
                    f"published container port {port.get('target')} is not loopback-bound",
                )
            )

    volumes = _as_dict_list(service.get("volumes"))
    for volume in volumes:
        target = str(volume.get("target") or "")
        source = str(volume.get("source") or "")
        if _is_mcp_mount_target(target) and not bool(volume.get("read_only")):
            findings.append(
                Finding(
                    "warning",
                    "mcp-pack-writable",
                    name,
                    f"MCP pack mount at {target} is writable",
                )
            )
        if ".cursor" in {Path(target).name, Path(source).name}:
            findings.append(
                Finding(
                    "warning",
                    "cursor-mount",
                    name,
                    "service mounts Cursor project metadata; keep this development-only",
                )
            )

    if isinstance(build, dict):
        context = str(build.get("context") or "")
        if context.startswith(("http://", "https://", "git://", "ssh://")):
            findings.append(
                Finding(
                    "warning",
                    "remote-build-context",
                    name,
                    "service builds from a remote context; verify immutable revision and provenance",
                )
            )
        dockerfile = str(build.get("dockerfile") or "")
        if dockerfile.endswith("applications/mcp/Dockerfile"):
            findings.extend(_inspect_framework_mcp_service(name, service))

    return findings


def _inspect_framework_mcp_service(
    name: str,
    service: dict[str, Any],
) -> list[Finding]:
    environment = service.get("environment")
    findings: list[Finding] = []
    # Shared allowlist; do not require MCP_PACKS_DIR / MCP_ADDONS.
    for key in ("MCP_SERVER_NAME",):
        value = environment.get(key) if isinstance(environment, dict) else None
        if not str(value or "").strip():
            # Optional: default server name is fine; only warn when explicitly empty.
            if isinstance(environment, dict) and key in environment:
                findings.append(
                    Finding(
                        "error",
                        "mcp-config-missing",
                        name,
                        f"framework MCP service declares empty {key}",
                    )
                )
    volumes = _as_dict_list(service.get("volumes"))
    has_addons_mount = any(
        str(volume.get("target") or "").rstrip("/").endswith("/addons")
        or str(volume.get("target") or "") in {"/app/addons", "../addons"}
        for volume in volumes
    )
    # String-form Compose volumes: ../addons:/app/addons
    if not has_addons_mount:
        raw_volumes = service.get("volumes") or []
        if isinstance(raw_volumes, list):
            has_addons_mount = any(
                isinstance(item, str) and ":/app/addons" in item for item in raw_volumes
            )
    if not has_addons_mount:
        findings.append(
            Finding(
                "warning",
                "mcp-addons-mount-missing",
                name,
                "framework MCP service has no /app/addons mount; verify addons are baked in",
            )
        )
    return findings


def _service_summary(name: str, service: dict[str, Any]) -> dict[str, Any]:
    build = service.get("build")
    dockerfile = build.get("dockerfile") if isinstance(build, dict) else None
    ports = [
        {
            "host_ip": port.get("host_ip"),
            "published": port.get("published"),
            "target": port.get("target"),
        }
        for port in _as_dict_list(service.get("ports"))
    ]
    return {
        "name": name,
        "profiles": list(service.get("profiles") or []),
        "image": service.get("image"),
        "dockerfile": dockerfile,
        "has_healthcheck": bool(service.get("healthcheck")),
        "ports": ports,
    }


def _as_dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _image_can_be_pulled(service: dict[str, Any]) -> bool:
    if not isinstance(service.get("build"), dict):
        return True
    pull_policy = str(service.get("pull_policy") or "").strip().lower()
    return pull_policy not in {"build", "never"}


def _is_mcp_mount_target(target: str) -> bool:
    normalized = target.rstrip("/")
    return normalized == "/app/mcp" or normalized.startswith("/app/mcp/")


def _uses_latest_tag(image: str) -> bool:
    name_without_digest = image.split("@", 1)[0]
    final_segment = name_without_digest.rsplit("/", 1)[-1]
    return ":" not in final_segment or final_segment.endswith(":latest")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Docker Compose and report framework-relevant risks without "
            "printing environment values."
        )
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=repository_root()
        / "docker"
        / "application"
        / "application.yaml",
        help="Compose file (default: docker/application/application.yaml).",
    )
    parser.add_argument(
        "--service",
        action="append",
        default=[],
        help="Inspect only this service; repeat for multiple services.",
    )
    parser.add_argument(
        "--profile",
        action="append",
        default=[],
        help="Enable this Compose profile; repeat for multiple profiles.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 2 when warnings are present.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Compose inspection CLI."""
    args = _build_parser().parse_args(argv)
    compose_file = args.file.resolve()
    if not compose_file.is_file():
        print(f"Compose file does not exist: {compose_file}", file=sys.stderr)
        return 1
    try:
        config = render_compose(compose_file, profiles=args.profile)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    selected = set(args.service) or None
    findings, summaries = inspect_config(config, selected_services=selected)
    if args.json:
        print(
            json.dumps(
                {
                    "compose_file": str(compose_file),
                    "services": summaries,
                    "findings": [asdict(finding) for finding in findings],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(f"Compose configuration valid: {compose_file}")
        print(f"Services inspected: {', '.join(row['name'] for row in summaries)}")
        for finding in findings:
            service = f"[{finding.service}] " if finding.service else ""
            print(
                f"{finding.level.upper()} {finding.code}: "
                f"{service}{finding.message}"
            )

    has_errors = any(finding.level == "error" for finding in findings)
    has_warnings = any(finding.level == "warning" for finding in findings)
    if has_errors:
        return 1
    if args.strict and has_warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
