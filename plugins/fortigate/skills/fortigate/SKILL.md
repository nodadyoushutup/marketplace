---
name: fortigate
description: >-
  Agnostic FortiGate craft: inventory policies/addresses/routes and gated firewall changes via MCP. Prefer FortiGate MCP; never invent policy ids; destructive needs explicit verb. Skip when the user did not authorize this surface.
---

# fortigate

## Gate

No explicit FortiGate / firewall / policy ask → **skip**. Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Inventory / status / health | `fortigate-inventory` |
| Policy / route mutations | `fortigate-safety` |

## Defaults

1. Never invent policy id, address object, or VDOM.
2. Read-only is the default for network devices.
3. Irreversible ACL/NAT changes: state risk; require clear authorization.
