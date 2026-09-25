---
name: framework
description: >-
  Framework monorepo index: addon isolation/substrate/modularity, Docker ops,
  parity porting, git/Jira host overlays, and workflow hooks. Use when working
  in a framework-style monorepo with marketplace plugins installed. Pair with
  global, code, business-analyst, atlassian, agentmemory, browser, drawio,
  lucidchart — do not duplicate them here. Skip when the ask is not framework
  monorepo work.
---

# Framework

Assume sibling marketplace plugins are installed. This plugin owns
**framework monorepo** craft (addon isolation, substrate, Docker ops, parity,
ceremony hooks, thin host Jira/git overlays). Agnostic posture, coding agents,
Atlassian craft, browser/drawio/memory, etc. live in other plugins — never fork
them under `framework-*`.

## Gate

No explicit framework / addon / monorepo substrate / Docker-ops overlay /
parity-port / ceremony ask (and not already in a framework repo context the
user named) → **skip**. Ordinary app coding uses `code` / `compose` / other
plugins.

## Load map

| Need | Asset |
| --- | --- |
| Ceremony / stop-hook floor | `framework-change-ceremony` (+ plugin hooks) |
| Custom-addon isolation | `framework-custom-addon-isolation`, `framework-addon-isolation` |
| Substrate / modularity / hygiene | `framework-addon-substrate`, `framework-addon-modularity`, `framework-addon-hygiene-checks` |
| Docker/Compose for this stack | `framework-docker`, then `framework-docker-ops` |
| Git remotes / issue worktrees | `framework-git-workflow` (+ public `code-worktrees`) |
| Jira host wiring | `framework-jira-issues`, `framework-jira-status` (needs public `atlassian`) |
| Foreign → addon parity | `framework-parity-porting` (+ optional `framework-parity-assessor`) |
| Blast radius / contracts / verify extras | `framework-impact-researcher`, `framework-contract-reviewer`, `framework-verification-runner`, `framework-runtime-observer` |
| GUI visual language / appearance / pages / icons | `framework-gui-appearance`, `framework-gui-page-patterns`, `framework-gui-live-updates`, `framework-icon-buttons` |
| API / worker / beat process roles | `framework-runtime-boundaries` (ready vs health, CPU/GPU/beat, jobs, bootstrap) |
| Which platform addon to depend on | `framework-platform-capabilities` |
| Stable author imports (no deep private paths) | `framework-public-imports` |
| HTTP client / dual `/api` / CSRF / CRUD verbs | `framework-api-integration` |
| Addon pytest conftest recipe | `framework-addon-testing` |
| GUI / runtime / auth / cache / … | matching `framework-*` rules |
| L3 plan / tech-lead / research / debug / QA | public `business-analyst-*` / `code-*` agents |

## Defaults

1. Prefer other marketplace plugins for portable craft — do not re-home them
   under `framework-*`.
2. Resolve addon / Compose / host overlays from repo evidence before inventing
   paths or labels.
3. Ceremony hooks are a floor, not a substitute for named verify agents when
   the change needs deeper checks.
4. Keep secrets out of chat; land durable credentials in Vault / gitignored
   env files.
5. Pair with `compose` for agnostic Compose layout; use `framework-docker-ops`
   for this stack’s container model.

## Do not re-add portable craft

If it exists elsewhere in this marketplace (`global`, `code`,
`business-analyst`, `atlassian`, `github`, `jenkins`, `agentmemory`, `browser`,
`drawio`, `lucidchart`, `compose`, …), **use that plugin**. This plugin keeps
monorepo substrate, addon isolation, Docker/Compose ops, parity, ceremony
hooks, and thin host overlays (`project.env` Jira labels, multi-remote Done
bar).
