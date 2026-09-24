---
name: framework
description: >-
  Homelab framework monorepo index: addon isolation/substrate/modularity,
  Docker ops, parity porting, git/Jira overlays, and workflow hooks. Use when
  working in the framework repo with marketplace plugins installed. Pair with
  global, code, business-analyst, jira, agentmemory, browser, drawio.
---

# Framework

Assume marketplace plugins are installed. This plugin owns **framework-only**
craft. Portable posture/coding/Jira/browser/drawio/memory live in sibling
plugins — do not duplicate them here.

## Load map

| Need | Asset |
| --- | --- |
| Ceremony / stop-hook floor | `framework-change-ceremony` (+ plugin hooks) |
| Custom-addon isolation | `framework-custom-addon-isolation`, `framework-addon-isolation` |
| Substrate / modularity / hygiene | `framework-addon-substrate`, `framework-addon-modularity`, `framework-addon-hygiene-checks` |
| Docker/Compose for this stack | `framework-docker`, then `framework-docker-ops` |
| Git remotes / issue worktrees | `framework-git-workflow` (+ `code-worktrees`) |
| Jira host wiring | `framework-jira-issues`, `framework-jira-status` (needs `jira` plugin) |
| Foreign → addon parity | `framework-parity-porting` (+ optional `framework-parity-assessor`) |
| Blast radius / contracts / verify extras | `framework-impact-researcher`, `framework-contract-reviewer`, `framework-verification-runner`, `framework-runtime-observer` |
| GUI / runtime / auth / cache / … | matching `framework-*` rules |

## Do not re-add portable craft

If it exists in `global`, `code`, `business-analyst`, `jira`, `agentmemory`,
`browser`, or `drawio`, use that plugin — not a fork under `.cursor/` in the
repo.
