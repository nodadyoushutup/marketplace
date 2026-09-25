---
name: velero
description: >-
  Agnostic Velero craft: list backups/schedules/restores and gated create/delete via MCP. Prefer Velero MCP; restores are irreversible without explicit ask. Skip when the user did not authorize this surface.
---

# velero

## Gate

No explicit Velero / backup / restore ask → **skip**. Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| List backups / schedules / restores | `velero-inventory` |
| Create / delete / restore gates | `velero-safety` |

## Defaults

1. Never invent backup/schedule name or namespace filter.
2. Read inventory before mutate.
3. Pair with `kubernetes` / `argocd` for cluster state; this plugin owns Velero CRs via MCP.
