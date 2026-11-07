---
name: git
description: >-
 Agnostic local git craft: worktrees, merge/rebase conflicts, commit message
 shape, and safe git CLI use. Skip when the user did not authorize git/SCM
 work.
---

# Git

## Gate

No explicit worktree, merge, rebase, commit, branch, or conflict ask →
**skip**. Do not open git ops to “cover” ordinary coding that never named
SCM work.

## Load map

| Need | Rule / skill |
| --- | --- |
| Isolate checkout | skill `git-worktrees` |
| Merge/rebase conflicts | skill `git-resolve-merge-conflicts` |
| Commit message shape | rule `git-commit-messages` |

## Defaults

1. Prefer the repo’s existing branch and remote names — never invent a
 default branch; detect it.
2. Do not force-push to `main` / `master` / the tracked default branch.
3. Do not update git config. Do not skip hooks unless the user asked.
4. Commit and push only when the user asked (or the consuming project has an
 explicit commit-and-push preference).
5. This plugin owns local SCM only. Pull requests and Actions live in the
 git-host plugin (for example `github`).

## Procedure

1. Confirm the user named a worktree, merge/rebase, commit, or branch task.
 **Done when** you have that target, or you skipped this plugin.
2. Apply the load-map skill or rule. **Done when** the tree state matches the
 ask (isolated path, conflict-free merge, or drafted commit subject).
3. Report evidence: worktree path, `git status` summary, or the commit
 subject. **Done when** a reader can verify without re-running your search.
