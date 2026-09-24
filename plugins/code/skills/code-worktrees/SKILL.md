---
name: code-worktrees
description: >-
  Isolate feature work with git worktree add under ~/.cursor/worktrees so
  Cursor discovers the checkout. Do not call move_agent_to_root and do not
  ask the user to type /worktree. A declared worktree directory is the
  emergency fallback only after git worktree add fails. Use when starting
  issue-keyed or isolation-required work.
---

# Git worktrees

When isolation is required, create the tree with `git worktree add` under
`~/.cursor/worktrees/<repo-directory-name>/<name>`. Cursor discovers that path.
Do **not** call `move_agent_to_root`. Do **not** ask the user to type
`/worktree`.

A project-declared worktree parent is emergency fallback only after
`git worktree add` fails. If that preference is blank too, edit the open
checkout.

Announce only when you create or reuse an isolated tree.

## When isolation applies

Isolation is **on** when the user asked for a worktree, or the repo’s own
instructions say this task is isolated (for example an issue-keyed branch and
not “on main” / “skip the worktree”).

If isolation is off — or the user says work **on main**, **on live**, **in the
open checkout**, or **skip the worktree** — stay put.

## Unexpected tree content — do not auto-revert

Before `git restore`, `git checkout --`, `git reset`, or any silent revert:

1. Confirm which checkout `git status` belongs to.
2. Separate uncommitted dirt from content already in `HEAD`.
3. If the tree is clean or the content is committed: read `git log` for that
   path. Report the commit. Do not discard it because this chat did not author
   it.

Discard only on an explicit operator ask, or when the dirt is uncommitted, you
created it this session, and undoing it *is* the task.

## Step 0 — Reuse

```bash
git worktree list
git rev-parse --show-toplevel
```

Record the open checkout path before creating a tree (refresh steps need it).

| Result | Action |
| --- | --- |
| List already has this branch or path | Use that path |
| Current toplevel is already that worktree | Stay |
| Otherwise | Step 1 |

## Step 1 — `git worktree add`

`<repo-directory-name>` = basename of `git rev-parse --show-toplevel`.
`<name>` = branch name the task requires (often the issue key).

```bash
git fetch origin
git worktree add -b "<name>" \
  "$HOME/.cursor/worktrees/<repo-directory-name>/<name>" \
  origin/main
```

Use `HEAD` only when `origin/main` does not exist. If the branch already
exists, omit `-b` and pass the branch as the start point.

Cursor’s manager scans only
`~/.cursor/worktrees/<repo-directory-name>/<name>`. Trees elsewhere are
invisible to that scan. Do not nest the worktree inside the open checkout.

Do not call `move_agent_to_root` / `move_agent_to_cloned_root`. If the session
root moves on its own, continue there. If it stays on the open checkout, edit
the worktree with absolute paths and Shell `working_directory`. A stayed root
is not a failure.

**Creation failed** only when `git worktree add` fails or the path is not a
checkout of this repo. Then Step 2 — do not retry a different directory.

## Step 2 — Emergency fallback

1. If the repo declares a non-blank worktree parent (for example `WORKTREE_DIR`
   in a gitignored env file), follow that overlay’s layout. Edit by absolute
   path. Still no `move_agent_to_root`.
2. If blank, edit the open checkout on the current branch. Say so in one
   sentence. Do not invent a directory.

## Step 3 — Setup and finish

Bootstrap the checkout you actually created. Commit from that checkout when
the user asks. After required merges, refresh the **original** open checkout
from Step 0. Do not delete the worktree unless the user or repo runbook says
to.
