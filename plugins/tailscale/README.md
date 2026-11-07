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

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/tailscale-workflow.drawio`](docs/tailscale-workflow.drawio) — gate → act → evidence
