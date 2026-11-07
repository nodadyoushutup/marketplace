# vaultwarden

Agnostic Vaultwarden craft: admin/ops posture and Bitwarden-compatible API hygiene with hard refuse to dump vault contents or credentials into chat.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `vaultwarden-ops` | Admin/ops inventory and config without dumping cipher plaintext |
| `vaultwarden-refuse-leak` | Hard refuse vault dumps, password paste, and secret commits |

## Skills

| Skill | Purpose |
| --- | --- |
| `vaultwarden` | Index / gate |

## Commands

- `/vaultwarden` → Vaultwarden admin/ops with leak refuse

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/vaultwarden-workflow.drawio`](docs/vaultwarden-workflow.drawio) — gate → act → evidence
