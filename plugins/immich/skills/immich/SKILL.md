---
name: immich
description: >-
  Agnostic Immich craft: library/album/asset inventory and gated delete/share
  changes. Prefer MCP when connected; otherwise API/UI. Skip when the user did
  not authorize this surface.
---

# immich

## Gate

No explicit Immich / photo library / album / asset ask → **skip**. Nextcloud
asks belong in a Nextcloud plugin when present; Plex/*arr stay in `yarr`. Prefer
a connected MCP (`global-mcp-first`); else Immich API/UI with a resolved base URL.

## Load map

| Need | Rule |
| --- | --- |
| List libraries / albums / assets / people | `immich-library` |
| Delete / share / admin mutate gates | `immich-safety` |

## Defaults

1. Never invent album, asset, or person ids — list/resolve first.
2. Resolve the Immich base URL from config/MCP/env — never hardcode a host.
3. Prefer trash/archive over permanent delete when silence is enough.
4. Never paste API keys or user passwords into chat.
