---
name: zot
description: >-
  Agnostic Zot OCI registry craft: repository/tag inventory and gated
  delete/GC. Prefer MCP when connected; otherwise API/UI. Skip when the user
  did not authorize this surface.
---

# zot

## Gate

No explicit Zot ask → **skip**. Other OCI registry products are out of scope —
do not absorb them here. Prefer a connected MCP; else Zot API/UI with a
resolved base URL.

## Load map

| Need | Rule |
| --- | --- |
| List repos / tags / referrers | `zot-inventory` |
| Delete tag / GC / auth mutate | `zot-safety` |

## Defaults

1. Never invent repository or tag names — list/resolve first.
2. Resolve the registry base URL from config/MCP/env — never hardcode a host.
3. Prefer tag delete over full repo wipe when that is enough.
4. This plugin owns Zot only.
