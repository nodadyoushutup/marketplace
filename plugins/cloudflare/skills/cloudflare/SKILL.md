---
name: cloudflare
description: >-
  Cloudflare DNS craft: list and change DNS records via MCP with hard gates on
  delete and broad rewrites. Prefer Cloudflare MCP. Skip when the user did
  not authorize DNS work.
---

# Cloudflare

## Gate

No explicit Cloudflare / DNS / record ask → **skip**. Prefer a connected
Cloudflare MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| List / create / update records | `cloudflare-dns` |
| Delete / replace / bulk risk | `cloudflare-safety` |

## Defaults

1. Never invent zone id or record id — list/resolve first.
2. Prefer update-in-place over delete+create when changing a value.
3. Deletes and “point everything at X” need an explicit verb.
4. Report FQDN + type + content after changes (no API tokens in chat).
