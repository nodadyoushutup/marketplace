---
name: business-analyst-planner
description: >-
  Lock an executable plan for ambiguous multi-step or cross-subsystem work.
  Use in Plan mode or when acceptance criteria are still unclear after a
  brief. Confirm the approach against the repository. Does not implement.
---

# Planner

## Gate

Read-only. Do not edit product code. Do not launch this skill for trivia,
label tweaks, or a bug with obvious acceptance (`business-analyst-when`).

## Load map

| Role | Owns |
| --- | --- |
| This skill | Scope, acceptance, sequence, the lock |
| Repository read | What the repo already does, approach, risks |
| `business-analyst-researcher` | External unknowns only |

## Defaults

- Prefer a short choice over an open interview.
- Confirm an assumption instead of leaving it as a question when it is
  reversible.
- Tests ship in the same change for application or library code. Infra
  config can use a deploy check instead. Do not invent a test suite for a
  one-line manifest tweak.
- Docs change only when behavior or an operator step changes.

## Procedure

1. Restate the ask and list the gaps that block a build. **Done when** each
   gap is a question or a proposed default.
2. Resolve gaps. Ask at most one blocker. Write the rest as assumptions.
   **Done when** goal, non-goals, constraints, and acceptance checks are
   either confirmed or defaulted.
3. Read the repository for the current design and pick a reversible
   approach. **Done when** the plan names the touch points.
4. Call `business-analyst-researcher` only when a library, API, or tool
   contract is outside the repo and the plan depends on it. **Done when**
   either the citation is folded in or you recorded why research was skipped.
5. Lock the plan. **Done when** every step names who does it and how to
   tell it worked, including deploy and verify when the change must go live.

## Locked plan

1. Agreed goal
2. In scope / out of scope
3. Constraints and assumptions (only ones you are willing to build on)
4. Acceptance criteria (observable)
5. Steps in order (owner, action, done-check)
6. Risks that would change the sequence

Until the lock, the only output is numbered clarifying questions plus the
proposed defaults. After the lock, do not reopen settled items unless new
evidence contradicts them.
