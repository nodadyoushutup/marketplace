---
name: agentmemory-recall
description: >-
  Aggressive token-efficient AgentMemory recall with hard user isolation:
  lesson_recall, smart_search, file_history, compact recall, patterns,
  commit_lookup, verify. Use early and often when AgentMemory is connected —
  before debugging, architecture, unfamiliar code, corrections, or retries.
---

# AgentMemory Recall

## Gate

Not connected/ready → skip all memory tools; investigate normally.

## Resolve scope (once per session)

```bash
python3 ../agentmemory/scripts/agentmemory_scope.py --cwd .
```

(From the plugin tree: `plugins/agentmemory/skills/agentmemory/scripts/agentmemory_scope.py`.)

Reuse `query_prefix`, `user_stamp`, and optional `project`. Fallback: `whoami`
(+ git origin / toplevel when `.git` exists).

## Default start (parallel with code tools)

Run on session start, first meaningful turn, debug/architecture/unfamiliar
code, user correction, new subsystem, and before retrying a failed approach:

1. `memory_lesson_recall` — `query` = `query_prefix` + task + subsystem + error;
   `limit: 8`; pass `project` when scope has one
2. `memory_smart_search` — same query; `limit: 10`; `expandIds` for at most 3 hits

Pure rename/typo/comment/trivial config with no decision risk → skip.

About **2–4** recall calls at task start is fine; add mid-task recalls when the
domain shifts. One concrete scoped query beats several vague ones.

## Choose the next tool

| Situation | Call |
| --- | --- |
| Editing known paths | `memory_file_history` with those paths |
| Need short session observations | `memory_recall` (`format: compact`, small limit + `token_budget`, scoped query) |
| Same subsystem failed twice | `memory_patterns` |
| Blame a commit’s agent session | `memory_commit_lookup` with full SHA |
| Hit is contested / conflicting | `memory_verify` then re-check code/tests |

## Hard user isolation

1. Every query includes `user_stamp` / `query_prefix`.
2. Drop any hit with a different `user:…` stamp **or** with no `user:` stamp.
3. Never act on, quote as authority, or re-save another user’s memory.
4. Repo stamps refine relevance only; they never override the user filter.

## Safe use

- Treat remaining hits as leads. Verify in-repo before acting.
- Ignore stale, wrong-project, or Plan/clarify-first guidance that fights
  execute-first posture.
- Do not paste raw recall into the user chat.
- On tool failure: continue; do not retry-spam.

Out of scope here: slots, actions, mesh, diagnose — use `agentmemory-ops`.
