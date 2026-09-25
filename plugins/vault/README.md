# vault

HashiCorp Vault craft — secret posture, PKI hygiene, leak refuse. Install when
Vault MCP (or equivalent) is available.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `vault-secrets` | KV read/write/delete |
| `vault-pki` | PKI mounts / issue |
| `vault-refuse-leak` | No secrets in chat/commits |

## Skills

| Skill | Purpose |
| --- | --- |
| `vault` | Index / gate |

## Commands

- `/vault` → secret / PKI craft

## Pairing

- `global-mcp-first` — Vault MCP before `vault` CLI
- `homelab` (private) — site overlays that reference Vault paths
