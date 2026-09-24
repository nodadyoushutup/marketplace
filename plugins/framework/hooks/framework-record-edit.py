#!/usr/bin/env python3
"""File-edit recorder: track which files an editor session has changed.

The stop gate needs this because neither editor includes all edited paths in its
stop payload. Always exits 0 so a recorder failure can never block an edit.

Records edits under the live project root, under linked git worktrees of
that repo, and under ``WORKTREE_DIR`` clones so issue-keyed work is verified.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import framework_workflow_state as ws  # noqa: E402


def main() -> int:
    event = ws.read_event()
    conversation_id = event.get("conversation_id")
    raw_path = event.get("file_path")
    if not isinstance(conversation_id, str) or not isinstance(raw_path, str):
        return 0

    ws.record_path(ws.project_root(), conversation_id, raw_path)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except Exception:  # noqa: BLE001 - a recorder must never block an edit
        status = 0
    print("{}")
    raise SystemExit(status)
