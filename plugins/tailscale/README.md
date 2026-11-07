# tailscale

Agnostic Tailscale craft: devices, ACLs, and network inventory with gated ACL/device changes. Prefer MCP when connected; otherwise API/CLI. Never invent device ids.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `tailscale-devices` | List devices, status, and netmap |
| `tailscale-safety` | ACL/key/device mutate need an explicit verb; no key dumps |

## Skills

| Skill | Purpose |
| --- | --- |
| `tailscale` | Index / gate |

## Commands

- `/tailscale` → Tailscale devices or gated ACL mutate

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `fortigate` — edge firewall pairing
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/tailscale-workflow.drawio`](docs/tailscale-workflow.drawio) — gate → act → evidence
