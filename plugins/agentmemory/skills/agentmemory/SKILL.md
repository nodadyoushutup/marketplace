---
name: agentmemory
description: >-
  Gated AgentMemory MCP index: skip when disconnected; otherwise recall before
  re-investigation and capture verified durable insights. Use at session start,
  on recurring failures, or when unsure which memory skill to load. Deeper
  playbooks: agentmemory-recall, agentmemory-capture, agentmemory-ops.
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

## Session defaults

1. Hard or unfamiliar work → parallel `memory_lesson_recall` +
   `memory_smart_search` (small limits) with first investigation tools.
2. After a verified durable insight → `memory_lesson_save` and/or `memory_save`
   (0–2/turn). Never secrets.
3. Ordinary single-agent coding → do **not** open actions, mesh, reflect, or
   diagnose.

Cursor alwaysApply rules `agentmemory-recall` and `agentmemory-capture` already
encode the default loop; this skill is the Claude / explicit entry point.
