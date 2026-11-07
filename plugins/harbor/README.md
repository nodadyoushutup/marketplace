# harbor

Agnostic Harbor registry craft: projects/repos/artifacts inventory and gated delete/retention/robot changes. Prefer MCP when connected; otherwise API/UI. Sibling to `zot` — install what you run.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `harbor-inventory` | List projects, repositories, and artifacts |
| `harbor-safety` | Delete/retention/robot/member need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `harbor` | Index / gate |

## Commands

- `/harbor` → Harbor inventory or gated mutate

## Pairing

- `global-mcp-first` — MCP before CLI/REST/UI
- `zot` — sibling OCI registry craft (do not mix)
- `kubernetes` / `compose` — when Harbor is deployed as a workload
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/harbor-workflow.drawio`](docs/harbor-workflow.drawio) — gate → act → evidence
