# immich

Agnostic Immich craft: library/album/asset inventory and gated delete/share changes. Prefer MCP when connected; otherwise API/UI. Never invent asset ids; refuse credential dumps.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `immich-library` | List libraries, albums, assets, and people |
| `immich-safety` | Permanent delete / share / admin need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `immich` | Index / gate |

## Commands

- `/immich` → Immich library or gated mutate

## Pairing

- `global-mcp-first` — MCP before CLI/REST/UI
- `yarr` — Plex/*arr media automation (different surface)
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/immich-workflow.drawio`](docs/immich-workflow.drawio) — gate → act → evidence
