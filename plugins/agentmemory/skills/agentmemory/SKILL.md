---
name: agentmemory
description: >-
  Gated AgentMemory MCP index: skip when disconnected; otherwise recall early
  and often, capture verified durable insights, and hard-isolate by local user
  (+ git repo when present). Use at session start, on retries/corrections, or
  when unsure which memory skill to load. Deeper playbooks: agentmemory-recall,
  agentmemory-capture, agentmemory-ops.
---

# AgentMemory

## Gate

If AgentMemory is **not** connected/ready → **no memory tools**; continue the
task. Do not invent calls.

When connected, prefer the smallest tool set:

| Need | Load |
| --- | --- |
| Search / lessons / file history / verify | `agentmemory-recall` |
| Save lessons / typed memories / refuse list | `agentmemory-capture` |
| Slots, actions, mesh, diagnose, exports, … | `agentmemory-ops` (+ rule `agentmemory-tools`) |

## Scope (required)

Before recall or save, resolve identity once per session:

```bash
python3 skills/agentmemory/scripts/agentmemory_scope.py --cwd .
```

- **Always** stamp / filter with `user:<whoami>` (Linux / macOS / Windows).
- When the cwd tree has `.git`, also stamp `repo:<stable-id>` and pass
  `project` for repo-local memories.
- On recall: drop any hit without this user’s stamp or with another user’s
  stamp. Shared services must not cross streams.

## Session defaults

1. Meaningful work → parallel `memory_lesson_recall` + `memory_smart_search`
   (scoped queries; limits ~8 / ~10) with first investigation tools — and again
   on corrections, new subsystems, or failed approaches.
2. After a verified durable insight → `memory_lesson_save` and/or `memory_save`
   with scope tags/concepts (usually 1–3/turn). Never secrets.
3. Ordinary single-agent coding → do **not** open actions, mesh, reflect, or
   diagnose.

Cursor alwaysApply rules `agentmemory-recall` and `agentmemory-capture` already
encode the default loop; this skill is the Claude / explicit entry point.
