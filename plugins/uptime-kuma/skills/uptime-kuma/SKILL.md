---
name: uptime-kuma
description: >-
  Agnostic Uptime Kuma craft: monitors, status pages, and notification channels
  with gated delete/pause. Prefer MCP when connected; otherwise API/UI. Skip
  when the user did not authorize this surface.
---

# uptime-kuma

## Gate

No explicit Uptime Kuma / uptime monitor / status page ask → **skip**. Prefer a
connected MCP (`global-mcp-first`); else API or browser UI with resolved base URL.

## Load map

| Need | Rule |
| --- | --- |
| List / create / update monitors and status pages | `uptime-kuma-monitors` |
| Delete / pause / bulk risk | `uptime-kuma-safety` |

## Defaults

1. Never invent monitor, tag, or status-page ids — list/resolve first.
2. Resolve the instance base URL from config/MCP/env — never hardcode a host.
3. Prefer pause over delete when the user only wants quiet.
4. Pair with `grafana` / `prometheus` for metrics; this plugin owns Kuma monitors.
