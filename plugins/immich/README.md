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

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/immich-workflow.drawio`](docs/immich-workflow.drawio) — gate → act → evidence
