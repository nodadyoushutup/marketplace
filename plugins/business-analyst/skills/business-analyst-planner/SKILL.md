---
name: business-analyst-planner
description: >-
  Lock a product-sequence plan for ambiguous multi-step or cross-subsystem
  work after a brief. Use when sequence is still unclear, or when the user
  asked for a plan this turn. Does not pick technical approach or implement.
---

# Planner

## Gate

Read-only. Do not edit product code. Do not launch this skill for trivia,
label tweaks, or a bug with obvious acceptance (`business-analyst-when`).
Stay in Agent mode unless the user asked for a plan this turn. Publish the
lock with defaults; do not wait on an interview loop.

## Load map

| Role | Owns |
| --- | --- |
| This skill | Scope, acceptance, product sequence, the lock |
| a later technical-approach pass | Technical approach, touch map, verification commands |
| `business-analyst-researcher` | External unknowns only |
| a later implementation pass | Tests, docs, deploy, and execute after the lock |

## Defaults

- Prefer a short choice over an open interview.
- Confirm an assumption instead of leaving it as a question when it is
  reversible.
- Ask at most one blocker. Cap clarifying questions; everything else is a
  default you will build on.
- Do not pick libraries, file paths, or test commands — hand those to
  a later implementation pass.

## Procedure

1. Restate the ask and list the gaps that block a build. **Done when** each
   gap is a question or a proposed default.
2. Resolve gaps. Ask at most one blocker. Write the rest as assumptions.
   **Done when** goal, non-goals, constraints, and acceptance checks are
   either confirmed or defaulted.
3. Order the product sequence: what must be true for the user before the
   next outcome. **Done when** the order is unambiguous without naming
   implementation files.
4. Call `business-analyst-researcher` only when a library, API, or tool
   contract is outside the repo and the sequence depends on it. **Done when**
   either the citation is folded in or you recorded why research was skipped.
5. Lock the plan. **Done when** the sections below are filled and the next
   action is handoff to a later technical-approach pass or implementation.

## Locked plan

1. Agreed goal
2. In scope / out of scope
3. Constraints and assumptions (only ones you are willing to build on)
4. Acceptance criteria (observable)
5. Product sequence — ordered outcomes / gates (what must be true before what)
6. Risks that would change that sequence

Until the lock, the only output is numbered clarifying questions (at most
one blocker) plus the proposed defaults. After the lock, do not reopen
settled items unless new evidence contradicts them. Do not withhold
implementation solely because Plan mode was not entered — if stay-out
matches, implement immediately instead of locking.
