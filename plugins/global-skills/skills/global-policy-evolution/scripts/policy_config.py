#!/usr/bin/env python3
"""Load the optional Cursor project policy overlay.

``.cursor/policy-config.json`` may forbid policy basenames. MCP servers stay
user-level editor config and are not project-owned.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

POLICY_CONFIG_KEYS = frozenset({"forbiddenPolicyNames"})
POLICY_CONFIG_DEFAULTS: dict[str, list[Any]] = {key: [] for key in POLICY_CONFIG_KEYS}


def load_policy_config(root: Path) -> dict[str, list[Any]]:
    """Load and validate the optional ``.cursor/policy-config.json`` overlay.

    Args:
        root: Repository root holding the optional overlay.

    Returns:
        A mapping with ``forbiddenPolicyNames`` (list of unique non-empty strings).

    Raises:
        ValueError: If the overlay is missing required shape or uses unknown keys.
    """
    path = root / ".cursor" / "policy-config.json"
    if not path.is_file():
        return {key: [] for key in POLICY_CONFIG_KEYS}
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError("policy config must be a JSON object")
    unknown = sorted(set(loaded) - POLICY_CONFIG_KEYS)
    if unknown:
        raise ValueError("unknown policy config keys: " + ", ".join(unknown))
    config = {key: loaded.get(key, []) for key in POLICY_CONFIG_KEYS}
    values = config["forbiddenPolicyNames"]
    if not isinstance(values, list) or any(
        not isinstance(v, str) or not v.strip() for v in values
    ):
        raise ValueError("forbiddenPolicyNames must be a list of non-empty strings")
    if len(values) != len(set(values)):
        raise ValueError("forbiddenPolicyNames must not contain duplicates")
    return config
