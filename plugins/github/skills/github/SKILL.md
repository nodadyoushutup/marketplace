---
name: github
description: >-
  Agnostic GitHub craft: wait for PR checks, leave PR/issue comments, edit
  Actions workflows without product-specific pipelines, and remind that
  CI-from-main edits must land on the tracked branch. Prefer GitHub MCP when
  ready. Skip when the user did not authorize GitHub/PR/Actions work.
---

# GitHub

## Gate

No explicit PR / check / comment / Actions / workflow ask and no named PR or
run → **skip**. Do not open GitHub to “cover” ordinary coding. Prefer a
connected GitHub MCP when GitHub work is in play (`global-mcp-first`).

## Load map

| Need | Rule / action |
| --- | --- |
| Wait for / report PR checks | `github-pr-checks` |
| Leave or reply to PR/issue comments | `github-pr-comments` |
| Edit `.github/workflows/**` | `github-actions` + `code-yaml` |
| Workflow live only after merge to default | `github-ci-from-main` |

## Defaults

1. Never invent owner/repo, PR number, workflow id, or check names.
2. Do not claim checks are green without a fresh MCP/API read.
3. Comments are operator-facing and brief — no secrets, no dump of raw logs.
4. Workflow YAML stays agnostic: no hard-coded product app paths or secrets.
5. Pair with `code-workflow` for product code; this plugin owns the GitHub
   surface only.
