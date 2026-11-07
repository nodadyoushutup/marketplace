---
name: harbor
description: >-
  Agnostic Harbor registry craft: projects/repos/artifacts inventory and gated
  delete/retention/robot changes. Prefer MCP when connected; otherwise API/UI.
  Skip when the user did not authorize this surface.
---

# harbor

## Gate

No explicit Harbor / project / artifact / robot-account ask → **skip**. Zot
asks belong in `zot` — do not absorb Zot craft here. Prefer a connected MCP
(`global-mcp-first`); else Harbor API/UI with a resolved base URL.

## Load map

| Need | Rule |
| --- | --- |
| List projects / repos / artifacts | `harbor-inventory` |
| Delete / retention / robot / member gates | `harbor-safety` |

## Defaults

1. Never invent project, repository, or artifact digests — list/resolve first.
2. Resolve the Harbor base URL from config/MCP/env — never hardcode a host.
3. Prefer artifact/tag delete over project wipe when that is enough.
4. Never paste robot account tokens or admin passwords into chat.
5. Sibling product choice vs `zot` — this plugin owns Harbor only.
