---
name: vaultwarden
description: >-
  Agnostic Vaultwarden craft: admin/ops posture and Bitwarden-compatible API
  hygiene with hard refuse to dump vault contents or credentials into chat.
  Prefer MCP when connected. Skip when the user did not authorize this surface.
---

# vaultwarden

## Gate

No explicit Vaultwarden / Bitwarden-compatible vault / VW admin ask → **skip**.
HashiCorp Vault asks belong in `vault` — do not absorb them here. Prefer a
connected MCP (`global-mcp-first`); else admin API/UI with resolved base URL.

## Load map

| Need | Rule |
| --- | --- |
| Admin/ops inventory and config shape | `vaultwarden-ops` |
| Leak / dump / chat hygiene | `vaultwarden-refuse-leak` |

## Defaults

1. Never invent org, collection, or user ids — list/resolve first when authorized.
2. Resolve the instance base URL from config/MCP/env — never hardcode a host.
3. Prefer landing secrets in the vault product — never paste vault item values
   into chat or commits (`vaultwarden-refuse-leak`).
4. Pair with `vault` for HashiCorp infrastructure secrets; this plugin owns
   Vaultwarden / Bitwarden-compatible password vault ops.
