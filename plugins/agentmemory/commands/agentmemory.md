---
name: agentmemory
description: >-
  Run gated AgentMemory recall and/or capture when the MCP is connected.
---

# /agentmemory

1. If AgentMemory is not connected/ready, say so and stop — no invented tool calls.
2. Otherwise load `agentmemory` (index), then:
   - Need context → follow `agentmemory-recall`
   - Have a verified durable insight → follow `agentmemory-capture`
   - Slots / actions / mesh / diagnose / export → follow `agentmemory-ops`
3. Never store secrets. Cap saves at 0–2 this turn.
4. Do not dump raw memory payloads into the chat.
