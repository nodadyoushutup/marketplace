# jenkins

Agnostic Jenkins craft for Claude Code and Cursor — build status, console
triage, and pipeline hygiene. Install when the project uses Jenkins (Jenkins
MCP or equivalent). No product-specific job names hard-coded.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `jenkins-builds` | Status / console / queue / trigger / stop |
| `jenkins-pipeline` | Agnostic Jenkinsfile / pipeline entrypoints |
| `jenkins-ci-from-main` | Pipeline edits must be on the SCM ref the job builds |

All rules are **agent-requested** (`alwaysApply: false`) so cold clones without
Jenkins do not load them every turn.

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `jenkins` | Index / gate for Claude + explicit entry |

## Commands

- `/jenkins` → builds, console, or pipeline craft

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/jenkins-workflow.drawio`](docs/jenkins-workflow.drawio) — gate → act → evidence
