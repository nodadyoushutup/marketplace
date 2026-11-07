---
name: tailscale
description: >-
  Agnostic Tailscale craft: devices, ACLs, and network inventory with gated
  ACL/device changes. Prefer MCP when connected; otherwise API/CLI. Skip when
  the user did not authorize this surface.
---

# tailscale

## Gate

No explicit Tailscale / tailnet / ACL / device ask → **skip**. WireGuard-only or
Headscale asks belong elsewhere when present. Prefer a connected MCP
(`global-mcp-first`); else Tailscale API or `tailscale` CLI with resolved auth.

## Load map

| Need | Rule |
| --- | --- |
| List devices / status / netmap | `tailscale-devices` |
| ACL / key / device mutate gates | `tailscale-safety` |

## Defaults

1. Never invent device id, node name, or ACL tag — list/resolve first.
2. Prefer narrow ACL changes over rewriting the whole policy file.
3. Never paste auth keys, OAuth client secrets, or API keys into chat.
4. Pair with `fortigate` for edge firewall; this plugin owns Tailscale craft.
