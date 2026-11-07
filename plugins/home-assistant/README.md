# home-assistant

Agnostic Home Assistant craft: entity/state inventory, service calls, and automation hygiene with gated destructive actions. Prefer MCP when connected; otherwise API/UI.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `home-assistant-entities` | List entities, states, areas, and devices |
| `home-assistant-safety` | Destructive service calls / deletes need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `home-assistant` | Index / gate |

## Commands

- `/home-assistant` → HA entities or gated service call

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/home-assistant-workflow.drawio`](docs/home-assistant-workflow.drawio) — gate → act → evidence
