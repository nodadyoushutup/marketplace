# kopia

Agnostic Kopia craft: repository and snapshot inventory plus gated snapshot/restore/forget. Prefer MCP when connected; otherwise kopia CLI. Complements Velero for non-K8s backups.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `kopia-inventory` | List repositories, snapshots, and policies |
| `kopia-safety` | Snapshot/restore/forget need an explicit verb naming the object |

## Skills

| Skill | Purpose |
| --- | --- |
| `kopia` | Index / gate |

## Commands

- `/kopia` → Kopia inventory or gated restore

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/kopia-workflow.drawio`](docs/kopia-workflow.drawio) — gate → act → evidence
