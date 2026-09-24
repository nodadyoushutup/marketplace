---
name: jenkins
description: >-
  Agnostic Jenkins craft: watch builds, read console output, edit pipeline
  definitions without product-specific jobs, and remind that CI-from-main
  edits must land on the tracked branch. Prefer Jenkins MCP when ready. Skip
  when the user did not authorize Jenkins work.
---

# Jenkins

## Gate

No explicit build / console / queue / Jenkinsfile / pipeline ask and no named
job or build → **skip**. Prefer a connected Jenkins MCP when Jenkins work is
in play (`global-mcp-first`).

## Load map

| Need | Rule / action |
| --- | --- |
| Status / wait / console / stop | `jenkins-builds` |
| Edit Jenkinsfile or pipeline entrypoints | `jenkins-pipeline` (+ `code-yaml` when YAML) |
| Pipeline live only after merge to default | `jenkins-ci-from-main` |

## Defaults

1. Never invent job fullname, build number, node, or view path.
2. Do not claim a build succeeded without a fresh MCP/API read.
3. Console excerpts stay short and redacted — no secrets.
4. Pipeline definitions stay agnostic: no hard-coded product credentials.
5. Pair with `code-workflow` for product code; this plugin owns the Jenkins
   surface only.
