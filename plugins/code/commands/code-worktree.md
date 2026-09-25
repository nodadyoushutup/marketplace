---
name: code-worktree
description: >-
  Create or use an isolated git worktree for the current task (Cursor-native
  remount when available; otherwise git worktree add under ~/.cursor/worktrees).
---

# Git worktree

1. Load `code-worktrees`.
2. If isolation is not warranted, stay on the open checkout and say so.
3. Prefer lane A/B (already remounted or Cursor `/worktree` / Agents Window)
   when that remounted the session; otherwise `git worktree add` under
   `~/.cursor/worktrees/<repo>/<name>` and edit only under that path.
4. Resolve the default remote branch (do not assume `main`).
5. Do not commit, push, or delete the worktree unless the user asked.
