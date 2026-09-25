---
name: code-execute-jira
description: >-
  Execute a named Jira issue through a worktree to an open GitHub PR.
  Pass the issue key (for example PROJ-123). Stops when the PR is ready —
  never merges.
---

# Execute Jira issue

Slash UX: `/code-execute-jira <ISSUE-KEY>`.

1. Require an issue key in the argument or message. If missing, ask once.
2. Load `code-execute-jira` and run it end to end.
3. Pair with ready Jira/Atlassian MCP (read + status) and GitHub MCP (PR)
   when available (`global-mcp-first`).
4. Stop at an open PR. Report the URL. Do **not** merge. Do **not** mark
   the issue Done.
