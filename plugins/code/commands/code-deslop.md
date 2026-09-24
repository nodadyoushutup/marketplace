---
name: code-deslop
description: >-
  Dead-path and hygiene cleanup audit (deslop) for a bounded scope.
---

# Deslop

1. Load `code-deslopify`.
2. Bound scope. Prefer deletion/inlining over new abstraction.
3. Phase A (dead paths) then Phase B via `code-refactor` when structure debt remains.
4. Validate focused/owner checks before claiming clean.
