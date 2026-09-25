---
name: vault
description: >-
  HashiCorp Vault craft: gated secret reads/writes, mount and PKI hygiene, and
  hard refuse to paste credentials into chat or commits. Prefer Vault MCP.
  Skip when the user did not authorize Vault work.
---

# Vault

## Gate

No explicit Vault / secret path / mount / PKI ask → **skip**. Prefer a
connected Vault MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Read / write / delete secrets | `vault-secrets` |
| Mounts / PKI roles / certs | `vault-pki` |
| Leak / commit / chat hygiene | `vault-refuse-leak` (always with the above) |

## Defaults

1. Never invent mount paths, secret keys, or role names.
2. Prefer landing values in Vault over printing them in chat.
3. Delete and broad list operations need an explicit verb.
4. Pair with `code-workflow` for app wiring; this plugin owns the Vault
   surface only.
