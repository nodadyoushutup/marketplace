---
name: git-worktrees
description: >-
  Isolate feature work with git worktree add under ~/.cursor/worktrees so
  Cursor discovers the checkout. Do not call move_agent_to_root and do not
  ask the user to type /worktree. A declared worktree directory is the
  emergency fallback only after git worktree add fails. Use when starting
  issue-keyed or isolation-required work.
version: 0.2.0
---

# Git worktrees (portable)

**Core principle:** When isolation is required, run `git worktree add` under
`~/.cursor/worktrees/<repo-directory-name>/<name>`. Cursor discovers that
path. Do not call `move_agent_to_root`. Do not ask the user to type
`/worktree`.

A project worktree-directory preference is the emergency fallback, and only
after `git worktree add` fails. If that preference is also blank, edit the
open checkout.

Announce only when you create or reuse an isolated tree.

## When isolation applies

Isolation is **on** when the user asked for a worktree, or the repo overlay
says this task is isolated (for this framework, an explicit issue key and
not “on main” / “on live” / “skip the worktree”).

If isolation is off: edit the current checkout.

If the user says work **on main**, **on live**, **in the open checkout**, or
**skip the worktree**: stay put.

## Unexpected tree content — do not auto-revert

Before `git restore`, `git checkout --`, `git reset`, or any silent revert:

1. Confirm which checkout `git status` belongs to.
2. Separate uncommitted dirt from content already in `HEAD`.
3. If the tree is clean or the content is committed: read `git log` for that
   path. Report the commit. Do not discard it because this chat did not
   author it.

Discard only on an explicit operator ask, or when the dirt is uncommitted,
you created it this session, and undoing it is the task.

## Step 0 — Reuse

```bash
git worktree list
git rev-parse --show-toplevel
```

Record the open checkout path before creating a tree. Later refresh steps
need that path.

| Result | Action |
| --- | --- |
| `git worktree list` already has this branch or path | Use that path |
| Current toplevel is already that worktree | Stay there |
| Otherwise | Step 1 |

## Step 1 — `git worktree add`

`<repo-directory-name>` is the basename of `git rev-parse --show-toplevel`.
`<name>` is the branch name the overlay requires (the issue key when the
overlay says so).

```bash
git fetch origin
git worktree add -b "<name>" \
  "$HOME/.cursor/worktrees/<repo-directory-name>/<name>" \
  origin/main
```

Use `HEAD` only when `origin/main` does not exist. If the branch already
exists, omit `-b` and pass the branch name as the start point.

Cursor’s worktree manager scans only
`~/.cursor/worktrees/<repo-directory-name>/<name>`. A worktree anywhere
else is invisible to that scan. Do not put the tree inside the open
checkout.

Do not call `move_agent_to_root` or `move_agent_to_cloned_root`. If the
session root moves to the new path on its own, continue there. If it stays
on the open checkout, edit the worktree with absolute paths and Shell
`working_directory`. A stayed root is not a failure.

**Creation failed** only when `git worktree add` fails, or the path is not
a checkout of this repo. Then go to Step 2. Do not retry with another
directory.

## Step 2 — Emergency fallback

1. If the repo declares a non-blank worktree parent (this framework:
   `WORKTREE_DIR` in gitignored `project.env`), follow that overlay’s clone
   layout. Edit those clones by absolute path. Do not call
   `move_agent_to_root`.
2. If that parent is blank, edit the open checkout on the current branch.
   Say that in one sentence. Do not invent a directory.

## Step 3 — Setup and finish

Run the repo’s bootstrap against the checkout you actually created. Commit
from that checkout when the user asks. After required merges, refresh the
**original** open checkout from Step 0. Do not delete the worktree unless
the user or the repo runbook says to.

## Provenance

Informed by [obra/superpowers](https://github.com/obra/superpowers)
`using-git-worktrees` (MIT). See `ORIGIN.md`.
