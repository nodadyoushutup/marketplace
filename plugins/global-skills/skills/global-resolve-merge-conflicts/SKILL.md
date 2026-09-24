---
name: global-resolve-merge-conflicts
description: >-
  Resolve an in-progress git merge or rebase conflict: understand both intents,
  preserve behavior, run project checks, finish the merge. Use when git reports
  conflicts or merge/rebase is stopped mid-way.
version: 0.1.0
---

# Resolve merge conflicts

1. **See state** — `git status`, conflicting files, whether this is merge or
   rebase. Read recent history on both sides.
2. **Find primary sources** — Understand why each side changed. Commit
   messages, PRs, and linked issues when available. Look up facts yourself;
   do not ask the user for history you can fetch.
3. **Resolve each hunk** — Preserve both intents where possible. Where they
   conflict, pick the side that matches the merge's stated goal and note the
   trade-off. Do **not** invent new behavior.
4. **Abort only when blocked** — Prefer resolve and continue. `--abort` only
   if the user asks, the wrong base was used, or continuing would destroy
   work you cannot reconstruct.
5. **Run project checks** — Discover this repo's automated checks (typecheck,
   owner tests, format). Fix what the merge broke. Prefer the smallest
   relevant commands; honor stop-hook owner-test floors when present.
6. **Finish** — Stage resolutions and continue (`git merge --continue` /
   `git rebase --continue`) or commit the merge when appropriate. Do not
   leave the tree mid-conflict.

## Provenance

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills)
`resolving-merge-conflicts` (MIT). See `ORIGIN.md`.
