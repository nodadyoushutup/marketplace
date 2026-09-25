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

## Pairing

- `global-host-url` — no localhost URLs to the user
- `vault` — durable secrets, not chat
- `github` — image publish / Actions when the ask is CI, not runtime Compose
- `code` YAML rules — Compose file shape when editing YAML

## Diagrams

- [`docs/compose-workflow.drawio`](docs/compose-workflow.drawio) — gate → act → evidence
