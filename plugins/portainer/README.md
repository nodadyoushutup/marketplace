# portainer

Agnostic Portainer craft: endpoint/stack/container inventory and gated stack/container mutations. Prefer MCP when connected; otherwise API/UI. Never invent endpoint ids.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `portainer-inventory` | List endpoints, stacks, and containers |
| `portainer-safety` | Deploy/stop/delete/prune need an explicit verb naming the object |

## Skills

| Skill | Purpose |
| --- | --- |
| `portainer` | Index / gate |

## Commands

- `/portainer` → Portainer inventory or gated mutate

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/portainer-workflow.drawio`](docs/portainer-workflow.drawio) — gate → act → evidence
