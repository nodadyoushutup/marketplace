# authentik

Agnostic Authentik IdP craft: applications, providers, flows, and groups with gated destructive changes. Prefer MCP when connected; otherwise API/UI. Never invent object ids.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `authentik-apps` | List/craft applications, providers, flows, and groups |
| `authentik-safety` | Delete/disable/ACL widen need an explicit verb; no secret dumps |

## Skills

| Skill | Purpose |
| --- | --- |
| `authentik` | Index / gate |

## Commands

- `/authentik` → Authentik apps or gated mutate

## Pairing

- `global-mcp-first` — MCP before CLI/REST/UI
- `traefik` / `nginx-proxy-manager` — edge proxy wiring
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/authentik-workflow.drawio`](docs/authentik-workflow.drawio) — gate → act → evidence
