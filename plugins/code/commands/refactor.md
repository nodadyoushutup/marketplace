---
name: refactor
description: >-
  Run a behavior-preserving Refactor pass on the current scope — ownership,
  decomposition, and structure without changing behavior.
---

# /refactor

Run the `code-refactor` skill now on the active scope (open files, named paths,
or the current change set if the user did not bound it).

## Do this

1. Load and follow `code-refactor` end to end.
2. Bound scope to named paths / languages (Python and/or JS/TS/JSX).
3. Establish the behavior contract before moving code (callers, tests,
   identities, side effects).
4. Inventory structural candidates; skip taste-only or out-of-scope platform
   extraction.
5. Apply language mechanics from `code-refactor`. Preserve public contracts.
6. Validate focused / owner checks.
7. Close out: what moved (or no structural candidates), deferred items, one
   next action if anything remains.

Do not ask permission to start. Execute.
