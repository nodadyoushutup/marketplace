# zot

Agnostic Zot OCI registry craft: repository/tag inventory and gated delete/GC. Prefer MCP when connected; otherwise API/UI. Sibling to `harbor` — install what you run.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `zot-inventory` | List repositories, tags, and referrers |
| `zot-safety` | Delete tag/repo / GC / auth need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `zot` | Index / gate |

## Commands

- `/zot` → Zot inventory or gated mutate

## Pairing

- `global-mcp-first` — MCP before CLI/REST/UI
- `harbor` — sibling OCI registry craft (do not mix)
- `kubernetes` / `compose` — when Zot is deployed as a workload
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/zot-workflow.drawio`](docs/zot-workflow.drawio) — gate → act → evidence
