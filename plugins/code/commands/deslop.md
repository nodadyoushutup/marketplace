---
name: deslop
description: >-
  Run a Deslop pass on the current scope — remove verified dead paths, shims,
  and hygiene residue, then hand structure debt to refactor when needed.
---

# /deslop

Run the `code-deslop` skill now on the active scope (open files, named paths,
or the current change set if the user did not bound it).

## Do this

1. Load and follow `code-deslop` end to end (Phases A → B → C as applicable).
2. Bound scope tightly. Prefer deletion and inlining over new abstraction.
3. Phase A: remove verified dead / obsolete / duplicated paths.
4. Phase B: if live-code structure debt remains, continue with `code-refactor`
   (same scope) — do not invent shared platform packages.
5. Phase C: review touched tests (delete one-offs, promote durable contracts,
   fill clear gaps only).
6. Validate focused / owner checks before claiming clean.
7. Close out: what was removed, what moved to refactor, what was deferred, one
   next action if anything remains.

Do not ask permission to start. Execute.
