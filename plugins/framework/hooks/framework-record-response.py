#!/usr/bin/env python3
"""afterAgentResponse recorder: note when the deslop suite was announced.

`code-deslop` requires announcing the suite with a
line beginning ``Deslop suite:``. Reusing that existing sentinel lets the
``stop`` gate tell whether the quality pass actually ran. Always exits 0.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import framework_workflow_state as ws  # noqa: E402

SENTINEL = ws.DESLOP_SENTINEL


def main() -> int:
    """Record a deslop announcement for the active conversation.

    Returns:
        Always ``0`` so Cursor never blocks on recorder failures.
    """
    event = ws.read_event()
    conversation_id = event.get("conversation_id")
    text = event.get("text")
    if not isinstance(conversation_id, str) or not isinstance(text, str):
        return 0
    if SENTINEL not in text.lower():
        return 0

    def mark(record: dict) -> None:
        record["deslop_announced"] = True

    ws.update(ws.project_root(), conversation_id, mark)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except Exception:  # noqa: BLE001 - a recorder must never block a response
        status = 0
    print("{}")
    raise SystemExit(status)
