# harbor

Agnostic Harbor registry craft: projects/repos/artifacts inventory and gated delete/retention/robot changes. Prefer MCP when connected; otherwise API/UI. Sibling to zot — install what you run.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `harbor-inventory` | List projects, repositories, and artifacts |
| `harbor-safety` | Delete/retention/robot/member need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `harbor` | Index / gate |

## Commands

- `/harbor` → Harbor inventory or gated mutate

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/harbor-workflow.drawio`](docs/harbor-workflow.drawio) — gate → act → evidence
