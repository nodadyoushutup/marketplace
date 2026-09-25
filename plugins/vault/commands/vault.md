---
name: vault
description: >-
  Read or write Vault secrets and PKI with leak-safe craft (MCP first).
---

# /vault

1. If the user did not authorize Vault/secret work, say so and stop.
2. Load `vault` and follow `vault-secrets` / `vault-pki` / `vault-refuse-leak`.
3. Prefer Vault MCP. Never invent paths or dump secrets into chat.
4. Confirm write/delete outcomes with a non-secret receipt (path + version).
