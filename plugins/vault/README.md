# vault

HashiCorp Vault craft — secret posture, PKI hygiene, leak refuse. Install when
Vault MCP (or equivalent) is available.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `vault-secrets` | KV read/write/delete |
| `vault-pki` | PKI mounts / issue |
| `vault-external-secrets` | Vault KV payloads for external secret sync (key honesty; no dumps) |
| `vault-refuse-leak` | No secrets in chat/commits |

## Skills

| Skill | Purpose |
| --- | --- |
| `vault` | Index / gate |

## Commands

- `/vault` → secret / PKI craft

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/vault-workflow.drawio`](docs/vault-workflow.drawio) — gate → act → evidence
