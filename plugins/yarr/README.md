# yarr

Agnostic *arr / Plex / qBittorrent / Seerr craft via the yarr MCP fleet: search, status, and gated mutations. Prefer yarr MCP; never invent instance ids.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `yarr-inventory` | List/search library and download state via yarr MCP tools |
| `yarr-safety` | Delete media, purge queue, or change quality profiles need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `yarr` | Index / gate |

## Commands

- `/yarr` → Media fleet (*arr/Plex/qBit) via yarr MCP

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/yarr-workflow.drawio`](docs/yarr-workflow.drawio) — gate → act → evidence
