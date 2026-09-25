# framework

Framework **monorepo** craft plugin. Ships from **marketplace-public**.
Install alongside other public stacks. Homelab **infra** site overlays stay in
**marketplace-private** (`homelab`). Framework-specific Cursor craft belongs
here, not under the consuming repo’s `.cursor/rules` / `skills` / `agents`.

## Owns

| Asset | Purpose |
| --- | --- |
| Addon isolation / substrate / modularity / hygiene | Monorepo stranger-test + removability |
| GUI visual language / appearance / page patterns | Flat full-bleed operator UI; peer archetypes; icon buttons |
| `framework-docker` / `framework-docker-ops` | This stack’s Compose/runtime model |
| `framework-git-workflow` | Multi-remote + issue worktrees overlay |
| `framework-jira-issues` / `framework-jira-status` | Host `project.env` + `framework`/`addon` labels |
| `framework-parity-porting` (+ assessor) | Foreign → custom-addon ports |
| Ceremony hooks | Stop-hook pytest / vitest floor |
| Framework agents | Impact / contracts / verify / runtime / parity |

## Does **not** own (install other plugins instead)

| Concern | Plugin |
| --- | --- |
| Plan / tech-lead / research / debug / QA | `business-analyst`, `code` |
| Jira / Confluence craft | `atlassian` (`atlassian-jira-*`, …) |
| Agnostic Compose layout | `compose` |
| Language standards / worktrees | `code` |
| Standing posture / commits | `global` |
| Memory / browser / diagrams | `agentmemory`, `browser`, `drawio`, `lucidchart` |
| Homelab infra site overlays | `homelab` (marketplace-private) |

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `framework-gui-appearance` | Visual language + tokens, seams, chrome, overlays, 4K scale |
| `framework-gui-page-patterns` | Page archetypes / peer composition cookbook |
| `framework-gui-live-updates` | Soft-nav paint, realtime coalesce, refresh races |
| `framework-icon-buttons` | Icon-only secondaries + stable action chrome |
| `framework-custom-addon-isolation` | Stranger-test / one-way dependency |
| … | Other `framework-*` runtime, addon, Jira, Docker rules |

## Skills

| Skill | Purpose |
| --- | --- |
| `framework` | Index / gate |
| `framework-addon-isolation` | Stranger-test / purpose leakage |
| `framework-addon-substrate` | Substrate Check |
| `framework-addon-modularity` | Removability / soft edges |
| `framework-docker` | Host Docker/Compose CLI |
| `framework-docker-ops` | Framework compose/runtime overlay |
| `framework-parity-porting` | Foreign → custom-addon ports |

## Agents

| Agent | Purpose |
| --- | --- |
| `framework-impact-researcher` | Pre-edit blast radius |
| `framework-contract-reviewer` | Post-edit contracts/boundaries |
| `framework-verification-runner` | Checks beyond the stop hook |
| `framework-runtime-observer` | After restart/migrate/seed |
| `framework-parity-assessor` | Parity assess/plan (read-only) |

## Hooks (Cursor)

Plugin hooks (`hooks/hooks.json`) using `${CURSOR_PLUGIN_ROOT}`:

- `afterFileEdit` → `framework-record-edit.py`
- `afterAgentResponse` → `framework-record-response.py`
- `stop` → `framework-workflow-gate.py` (owner pytest / GUI vitest floor)

## Commands

- `/framework` → index skill

## Diagrams

- [`docs/framework-workflow.drawio`](docs/framework-workflow.drawio) — gate → act → evidence
