# velero

Agnostic Velero craft: list backups/schedules/restores and gated create/delete via MCP. Prefer Velero MCP; restores are irreversible without explicit ask.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `velero-inventory` | List backups, schedules, restores, and BSL status via MCP |
| `velero-safety` | Create restore / delete backup need an explicit verb naming the object |

## Skills

| Skill | Purpose |
| --- | --- |
| `velero` | Index / gate |

## Commands

- `/velero` → Velero inventory or gated restore

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/velero-workflow.drawio`](docs/velero-workflow.drawio) — gate → act → evidence
