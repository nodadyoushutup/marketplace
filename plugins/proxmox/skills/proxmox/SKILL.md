---
name: proxmox
description: >-
  Agnostic Proxmox VE craft: list nodes/VMs, status, and gated power/clone/migrate via MCP. Prefer Proxmox MCP; never invent VMID or touch sacred hosts. Skip when the user did not authorize this surface.
---

# proxmox

## Gate

No explicit Proxmox / VM / LXC / node ask and no named VMID → **skip**. Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| List / status / config | `proxmox-inventory` |
| Power / clone / migrate / delete | `proxmox-safety` |

## Defaults

1. Never invent node name, VMID, or storage id — list/resolve.
2. Read-only inventory is the default.
3. Respect host sacred VMs / deny-lists when the consuming repo defines them (e.g. TrueNAS).
4. Pair with `kubernetes` for guest workloads; this plugin owns the hypervisor surface.
