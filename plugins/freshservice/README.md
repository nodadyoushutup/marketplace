# freshservice

Agnostic Freshservice ITSM craft — create gates, ticket body shape, status
honesty. Install when the project uses Freshservice (MCP or API).

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `freshservice-create` | Create-only filing gate |
| `freshservice-ticket` | Description shape |
| `freshservice-status` | Status / priority honesty |

All rules are **agent-requested** (`alwaysApply: false`).

## Skills

| Skill | Purpose |
| --- | --- |
| `freshservice` | Index / gate |

## Commands

- `/freshservice` → ticket craft

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/freshservice-workflow.drawio`](docs/freshservice-workflow.drawio) — gate → act → evidence
