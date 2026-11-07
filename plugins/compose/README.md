# compose

Agnostic Docker Compose craft: multi-file `COMPOSE_FILE` layout, project-directory
anchors, overlays/profiles, day-to-day ops, and hard gates on destructive
downs/volume wipes.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `compose-files` | `COMPOSE_FILE` order, project-dir anchor, overlays, env paths |
| `compose-ops` | `config` / `up` / `ps` / `logs` / pull / pin tags |
| `compose-safety` | `down -v`, volume wipe, prune, secret-dump refuse |

## Skills

| Skill | Purpose |
| --- | --- |
| `compose` | Index / gate |

## Commands

- `/compose` → Docker Compose layout and ops craft

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/compose-workflow.drawio`](docs/compose-workflow.drawio) — gate → act → evidence
