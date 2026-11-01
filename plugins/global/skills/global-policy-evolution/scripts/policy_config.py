#!/usr/bin/env python3
"""Load the optional project policy overlay.

``.cursor/policy-config.json`` may forbid policy basenames and configure which
hosts participate in local policy sync. MCP servers stay user-level editor
config and are not project-owned.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from policy_hosts import ALL_HOSTS, CANONICAL_HOST, policy_config_path

POLICY_CONFIG_KEYS = frozenset(
    {
        "forbiddenPolicyNames",
        "enabledHosts",
        "syncEnabled",
    }
)
DEFAULT_ENABLED_HOSTS = list(ALL_HOSTS)


def load_policy_config(root: Path) -> dict[str, Any]:
    """Load and validate the optional ``.cursor/policy-config.json`` overlay.

    Args:
        root: Repository root holding the optional overlay.

    Returns:
        Mapping with ``forbiddenPolicyNames``, ``enabledHosts``, and
        ``syncEnabled``.

    Raises:
        ValueError: If the overlay is missing required shape or uses unknown keys.
    """
    path = policy_config_path(root)
    if not path.is_file():
        return {
            "forbiddenPolicyNames": [],
            "enabledHosts": list(DEFAULT_ENABLED_HOSTS),
            "syncEnabled": True,
        }
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError("policy config must be a JSON object")
    unknown = sorted(set(loaded) - POLICY_CONFIG_KEYS)
    if unknown:
        raise ValueError("unknown policy config keys: " + ", ".join(unknown))

    forbidden = loaded.get("forbiddenPolicyNames", [])
    if not isinstance(forbidden, list) or any(
        not isinstance(v, str) or not v.strip() for v in forbidden
    ):
        raise ValueError("forbiddenPolicyNames must be a list of non-empty strings")
    if len(forbidden) != len(set(forbidden)):
        raise ValueError("forbiddenPolicyNames must not contain duplicates")

    hosts = loaded.get("enabledHosts", list(DEFAULT_ENABLED_HOSTS))
    if not isinstance(hosts, list) or not hosts:
        raise ValueError("enabledHosts must be a non-empty list of host ids")
    if any(not isinstance(h, str) or h not in ALL_HOSTS for h in hosts):
        raise ValueError(
            "enabledHosts must be a subset of: " + ", ".join(ALL_HOSTS)
        )
    if len(hosts) != len(set(hosts)):
        raise ValueError("enabledHosts must not contain duplicates")
    if CANONICAL_HOST not in hosts:
        raise ValueError(f"enabledHosts must include canonical host {CANONICAL_HOST!r}")

    sync_enabled = loaded.get("syncEnabled", True)
    if sync_enabled not in (True, False):
        raise ValueError("syncEnabled must be true or false")

    return {
        "forbiddenPolicyNames": forbidden,
        "enabledHosts": list(hosts),
        "syncEnabled": sync_enabled,
    }
