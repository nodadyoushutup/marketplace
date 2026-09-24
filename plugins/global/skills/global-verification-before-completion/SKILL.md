---
name: global-verification-before-completion
description: >-
  Use before claiming work is complete, fixed, or passing, and before commit
  or PR claims — require fresh verification evidence; evidence before
  assertions. Adapted from obra/superpowers verification-before-completion.
version: 0.1.0
---

# Verification before completion

**Core principle:** Evidence before claims, always.

## Iron law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run (or received this turn) the verification that proves the
claim, you cannot claim it passes.

## Gate

Before claiming status or expressing satisfaction:

1. **IDENTIFY** — What command or hook output proves this claim?
2. **RUN / OBSERVE** — Fresh, complete evidence this turn (or a stop-hook
   receipt for the same claim).
3. **READ** — Full output, exit code, failure count.
4. **VERIFY** — Does it confirm the claim? If no, state actual status.
5. **ONLY THEN** — Make the claim, with the evidence.

## Repository automation (do not fight it)

When the repo has a stop hook / owner-test gate that already ran the relevant
owner `pytest` / GUI `vitest` for files this conversation touched, that
receipt **is** verification for those targets. Do not re-run the same suite
only to satisfy this skill.

Still verify yourself when:

- The claim is broader than what the hook covers (full suite, Docker ready,
  visual browser check, cross-remote PR merge).
- The hook did not run or failed.
- You claim a bug is fixed — re-check the original symptom or the owning test.

## Common failures

| Claim | Requires | Not enough |
| --- | --- | --- |
| Tests pass | Test or hook output: 0 failures | "Should pass", prior turn |
| Bug fixed | Symptom or owning test passes | Code changed only |
| Build succeeds | Build exit 0 | Linter alone |
| Agent finished | Diff + verification | Subagent said "success" |

## Red flags — stop

- "Should", "probably", "seems to" as the only proof
- Satisfaction before verification ("Done!", "Perfect!")
- Commit / push / PR success claims without evidence
- Trusting a subagent report without checking the tree

## Provenance

Adapted from [obra/superpowers](https://github.com/obra/superpowers)
`skills/verification-before-completion` (MIT). See `ORIGIN.md`.
