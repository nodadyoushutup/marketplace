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
connected GitHub tool when GitHub work is in play.

## Load map

| Need | Rule / action |
| --- | --- |
| Wait for / report PR checks | `github-pr-checks` |
| Leave or reply to PR/issue comments | `github-pr-comments` |
| Edit `.github/workflows/**` | `github-actions` |
| Workflow live only after merge to default | `github-ci-from-main` |

## Defaults

1. Never invent owner/repo, PR number, workflow id, or check names.
2. Do not claim checks are green without a fresh MCP/API read.
3. Comments are operator-facing and brief — no secrets, no dump of raw logs.
4. Workflow YAML stays agnostic: no hard-coded product app paths or secrets.
5. This plugin owns the GitHub surface only. Do not implement product code
   from a checks or workflow ask.

## Procedure

1. Confirm the user named a pull request, check, comment, or workflow file.
   **Done when** you have that target, or you skipped this plugin.
2. Read the live object (PR, checks, or workflow file) before claiming a
   result. **Done when** the reply cites a fresh tool result, not memory.
3. Apply the load-map rule. For workflow YAML, also follow
   `github-ci-from-main`. **Done when** the edit or the comment matches that
   rule and contains no secret values.
4. Report evidence: PR URL, check names with pass/fail, or the workflow path.
   **Done when** a reader can verify the claim without re-running your search.
