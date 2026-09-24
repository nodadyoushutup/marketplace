---
name: agentmemory
description: >-
  Gated AgentMemory MCP usage: when the memory server is connected, recall
  before re-investigation and save verified durable insights. Skip entirely
  when AgentMemory is not ready. Use at session start and on recurring
  failures. Cursor also ships matching alwaysApply rules in this plugin.
---

# AgentMemory (gated)

If AgentMemory is **not** connected/ready, **skip all memory tools** and
continue normally.

When it **is** available:

## Recall

- Before debugging, architecture choices, unfamiliar code, or recurring
  failures: `memory_lesson_recall` + `memory_smart_search` (parallel, small
  limits).
- Routine localized edits in familiar code: one lesson recall or none.
- Treat hits as leads — verify against current code/tests/runtime.

## Save

- After a verified non-obvious bug fix, architecture decision, failed
  approach, stable preference, or rediscovered workflow: usually 0–2 saves
  per turn.
- Use `memory_lesson_save` for reusable “when X, do Y”; `memory_save` for
  facts/decisions/preferences.
- Never save secrets, chat narration, or routine successful tool calls.

## Refuse

Do not block the primary task if memory tools fail — say so briefly and
continue.
