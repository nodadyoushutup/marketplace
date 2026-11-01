---
name: code-execute-issue
description: >-
  Execute a named tracker issue through a worktree to an open pull request.
  Pass the issue key. Stops when the pull request is ready — never merges.
---

# Execute a tracker issue

Slash UX: `/code-execute-issue <ISSUE-KEY>`.

1. Require an issue key in the argument or the message. If it is missing, ask once.
2. Follow `code-execute-issue` end to end.
3. Prefer a connected tool for the tracker application and for the git host.
   Use a CLI only when that tool is missing or has failed.
4. Stop at an open pull request. Report the URL. Do not merge. Do not mark
   the issue done.
