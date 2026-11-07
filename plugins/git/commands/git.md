---
name: git
description: >-
 Operate on local git worktrees, merge/rebase conflicts, or commit message
 shape with agnostic craft.
---

# /git

1. If the user did not authorize worktree / merge / rebase / commit work and
 named no conflict or branch task, say so and stop.
2. Otherwise load `git` and follow the matching skill or rule
 (`git-worktrees`, `git-resolve-merge-conflicts`, `git-commit-messages`).
3. Never invent a default branch; detect it. Do not force-push the default
 branch.
4. Return the worktree path, conflict resolution status, or commit subject
 with evidence.
