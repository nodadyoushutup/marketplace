---
name: cloudflare
description: >-
  Manage Cloudflare DNS records with explicit destructive gates (MCP first).
---

# /cloudflare

1. If the user did not authorize Cloudflare/DNS work, say so and stop.
2. Load `cloudflare` and follow `cloudflare-dns` / `cloudflare-safety`.
3. Prefer Cloudflare MCP. Never invent zone or record ids.
4. Confirm changes with FQDN, type, and content.
