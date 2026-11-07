# cloudflare

Cloudflare DNS craft — record changes with destructive gates. Install when
Cloudflare MCP is available.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `cloudflare-dns` | List / create / update |
| `cloudflare-safety` | Delete / bulk risk gates |

## Skills

| Skill | Purpose |
| --- | --- |
| `cloudflare` | Index / gate |

## Commands

- `/cloudflare` → DNS craft

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/cloudflare-workflow.drawio`](docs/cloudflare-workflow.drawio) — gate → act → evidence
