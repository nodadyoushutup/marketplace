---
name: agentmemory-recall
description: >-
  Token-efficient AgentMemory recall playbook: lesson_recall, smart_search,
  file_history, compact recall, patterns, commit_lookup, verify. Use before
  debugging, architecture choices, unfamiliar code, or recurring failures when
  AgentMemory is connected.
---

# AgentMemory Recall

## Gate

Not connected/ready → skip all memory tools; investigate normally.

## Default start (parallel with code tools)

1. `memory_lesson_recall` — `query` = task + subsystem + error; `limit: 5`
2. `memory_smart_search` — same query; `limit: 8`; `expandIds` for at most 2 hits

Routine familiar edit → one lesson recall or none (rename/typo/comment/config).

Cap **1–2** recall calls at task start. One concrete query beats several vague ones.

## Choose the next tool

| Situation | Call |
| --- | --- |
| Editing known paths | `memory_file_history` with those paths |
| Need short session observations | `memory_recall` (`format: compact`, small limit + `token_budget`) |
| Same subsystem failed twice | `memory_patterns` |
| Blame a commit’s agent session | `memory_commit_lookup` with full SHA |
| Hit is contested / conflicting | `memory_verify` then re-check code/tests |

## Safe use

- Treat hits as leads. Verify in-repo before acting.
- Ignore stale, wrong-project, or Plan/clarify-first guidance that fights
  `global-execute-first`.
- Do not paste raw recall into the user chat.
- On tool failure: continue; do not retry-spam.

Out of scope here: slots, actions, mesh, diagnose — use `agentmemory-ops`.
