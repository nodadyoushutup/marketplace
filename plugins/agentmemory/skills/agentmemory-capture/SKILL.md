---
name: agentmemory-capture
description: >-
  AgentMemory capture playbook: memory_lesson_save vs memory_save with
  mandatory user (+ optional repo) stamps, refuse list, and aggressive
  verified-insight capture when AgentMemory is connected.
---

# AgentMemory Capture

## Gate

Not connected/ready → skip saves; finish the primary task.

## Resolve scope (once per session)

```bash
python3 ../agentmemory/scripts/agentmemory_scope.py --cwd .
```

(From the plugin tree: `plugins/agentmemory/skills/agentmemory/scripts/agentmemory_scope.py`.)

Every save must carry `user_stamp`. When `.git` / scope `repo` is present, also
stamp `repo:` and pass `project`.

## When to save

Save autonomously after verification (usually **1–3**/turn when distinct
insights land) when any match:

- Non-obvious bug root cause + fix
- Architecture/decision + rationale + paths
- Failed approach + failure condition
- Stable cross-session preference or user correction
- Hard-won workflow or non-obvious host/MCP/env quirk
- Lesson reinforcement (corrected equivalent content)

Bias toward saving what you would otherwise rediscover. No save for routine
success narration or “task done” with no insight.

## Which tool

| Kind | Tool | Notes |
| --- | --- | --- |
| “When X, do Y” / avoid Z | `memory_lesson_save` | `context`; `tags` = scope tags + domain; `project` when scoped |
| Typed durable record | `memory_save` | `type`: pattern \| preference \| architecture \| bug \| workflow \| fact |
| Path-scoped fact | `memory_save` | set `files`; `concepts` = scope concepts + aids |
| Future rule/skill seed | either | tag `policy-candidate` + one domain tag |

Cross-repo preferences: keep `user:` tag; omit `project` / `repo:` only for
those. Always keep the user stamp.

Before save: user-scoped search if a duplicate is plausible. Prefer reinforcing
a lesson over near-duplicate facts. Optional facets: `user=<name>`,
`repo=<id>`.

## Refuse

Secrets, credentials, PII, production payloads, todos, raw logs, guesses,
generic programming knowledge, code-obvious facts, chat dumps.

Never stamp another user’s identity. Never import another user’s memory into
this stream. Never save “ask clarifying questions by default” or “Plan when
unsure.” Supersede disproved memories explicitly.

Save failure → finish the task; mention only if the missed capture matters.
