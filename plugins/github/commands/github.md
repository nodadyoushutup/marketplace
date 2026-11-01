---
name: github
description: >-
  Operate on GitHub PRs, checks, comments, or Actions workflows with agnostic
  craft (MCP first).
---

# /github

1. If the user did not authorize PR/check/comment/Actions work and named no
   PR or run, say so and stop.
2. Otherwise load `github` and follow the matching rule
   (`github-pr-checks`, `github-pr-comments`, `github-actions`,
   `github-ci-from-main`).
3. Prefer GitHub MCP tools. Never invent owner/repo/PR/workflow ids.
4. Return check conclusions, comment URLs, or workflow paths with evidence.
