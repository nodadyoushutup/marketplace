---
name: agentmemory-capture
description: >-
  AgentMemory capture playbook: when and how to memory_lesson_save vs
  memory_save, refuse list, project scoping, policy-candidate tags. Use after
  verified durable insights when AgentMemory is connected.
---

# AgentMemory Capture

## Gate

Not connected/ready → skip saves; finish the primary task.

## When to save

Save autonomously after verification (0–2/turn) when any match:

- Non-obvious bug root cause + fix
- Architecture/decision + rationale + paths
- Failed approach + failure condition
- Stable cross-session preference
- Hard-won workflow
- Lesson reinforcement (corrected equivalent content)

No save for routine success, narration, or “task done.”

## Which tool

| Kind | Tool | Notes |
| --- | --- | --- |
| “When X, do Y” / avoid Z | `memory_lesson_save` | `context`, tags, confidence ∝ evidence |
| Typed durable record | `memory_save` | `type`: pattern \| preference \| architecture \| bug \| workflow \| fact |
| Path-scoped fact | `memory_save` | set `files` for later `memory_file_history` |
| Future rule/skill seed | either | tag `policy-candidate` + one domain tag |

Before save: quick search if a duplicate is plausible. Prefer reinforcing a
lesson over near-duplicate facts.

## Project scoping

- Pass `project` only for a **stable canonical** id already known.
- Never filesystem paths or display names.
- Autonomy / execute-first / no-grill preferences: **omit** `project`.

## Refuse

Secrets, credentials, PII, production payloads, todos, raw logs, guesses,
generic programming knowledge, code-obvious facts, chat dumps.

Never save “ask clarifying questions by default” or “Plan when unsure.”
Supersede disproved memories explicitly; do not leave known falsehoods current.

Save failure → finish the task; mention only if the missed capture matters.
