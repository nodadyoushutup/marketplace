---
name: yarr
description: >-
  Agnostic *arr / Plex / qBittorrent / Seerr craft via the yarr MCP fleet: search, status, and gated mutations. Prefer yarr MCP; never invent instance ids. Skip when the user did not authorize this surface.
---

# yarr

## Gate

No explicit *arr / Plex / qBit / Seerr / Tautulli ask → **skip**. Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Search / status / sessions | `yarr-inventory` |
| Delete / purge / profile risk | `yarr-safety` |

## Defaults

1. Never invent Sonarr/Radarr/Plex ids or qBit torrent hashes.
2. Read/search is the default; mutations need an explicit verb.
3. Site library classification overlays stay in private `homelab`.
4. Prefer yarr MCP over ad-hoc *arr REST wrappers (`global-mcp-first`).
