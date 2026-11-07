---
name: agentmemory
description: >-
  Run gated AgentMemory recall and/or capture when the MCP is connected.
---

# /agentmemory

1. If AgentMemory is not connected/ready, say so and stop — no invented tool calls.
2. Resolve scope via
   `plugins/agentmemory/skills/agentmemory/scripts/agentmemory_scope.py`
   (user stamp required; repo stamp when `.git` is present).
3. Otherwise load `agentmemory` (index), then:
   - Need context → follow `agentmemory-recall` (scoped; drop foreign/unscoped hits)
   - Have a verified durable insight → follow `agentmemory-capture` (stamp every save)
   - Slots / actions / mesh / diagnose / export → follow `agentmemory-ops`
4. Never store secrets. Cap saves at about 1–3 this turn when insights warrant.
5. Never use another user’s memories. Do not dump raw memory payloads into the chat.
