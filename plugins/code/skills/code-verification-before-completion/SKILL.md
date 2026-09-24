---
name: code-verification-before-completion
description: >-
  Require fresh verification evidence before claiming work is complete, fixed,
  or passing, and before commit or PR success claims. Use at handoff and before
  any “done / green / fixed” assertion.
---

# Verification before completion

**Rule:** no completion claim without fresh evidence this turn.

If you have not run (or received this turn) the check that proves the claim,
you cannot say it passes.

## Gate

Before claiming status or sounding finished:

1. **Name** the command, hook receipt, or probe that proves the claim.
2. **Run / observe** it fresh this turn (or accept a stop-hook receipt for the
   same claim).
3. **Read** full output, exit code, failure count.
4. **Match** — does it confirm the claim? If not, report actual status.
5. **Then** claim — with the evidence attached.

## Respect repo automation

When a stop hook / owner-test gate already ran the relevant owner suite for
files this conversation touched, that receipt **is** verification for those
targets. Do not re-run the same suite only to satisfy this skill.

Still verify yourself when:

- The claim is broader than the hook (full suite, deploy ready, browser check,
  remote PR merge).
- The hook did not run or failed.
- You claim a bug is fixed — re-check the symptom or owning test.

## Common failures

| Claim | Requires | Not enough |
| --- | --- | --- |
| Tests pass | Suite/hook output: 0 failures | “Should pass”, prior turn |
| Bug fixed | Symptom or owning test passes | Diff alone |
| Build succeeds | Build exit 0 | Linter alone |
| Agent finished | Diff + verification | Subagent said “success” |

## Stop signs

- “Should”, “probably”, “seems to” as the only proof
- “Done!” / “Perfect!” before evidence
- Commit / push / PR success without checks
- Trusting a subagent report without reading the tree
