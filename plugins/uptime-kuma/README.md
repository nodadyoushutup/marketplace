# uptime-kuma

Agnostic Uptime Kuma craft: monitors, status pages, and notification channels with gated delete/pause. Prefer MCP when connected; otherwise API/UI. Never invent monitor ids.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `uptime-kuma-monitors` | List/create/update monitors, status pages, and notification channels |
| `uptime-kuma-safety` | Delete/pause/bulk changes need an explicit verb naming the object |

## Skills

| Skill | Purpose |
| --- | --- |
| `uptime-kuma` | Index / gate |

## Commands

- `/uptime-kuma` → Uptime Kuma monitors or gated mutate

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/uptime-kuma-workflow.drawio`](docs/uptime-kuma-workflow.drawio) — gate → act → evidence
