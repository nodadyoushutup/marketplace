---
name: velero
description: >-
  Agnostic Velero craft: list backups/schedules/restores and gated create/delete via MCP. Prefer Velero MCP; restores are irreversible without explicit ask. Skip when the user did not authorize this surface.
---

# velero

## Gate

No explicit Velero ask (and no named Velero backup/schedule/restore) → **skip**.
Bare “backup / restore” without Velero is out of scope. Prefer a connected MCP.

## Load map

| Need | Rule |
| --- | --- |
| List backups / schedules / restores | `velero-inventory` |
| Create / delete / restore gates | `velero-safety` |

## Defaults

1. Never invent backup/schedule name or namespace filter.
2. Read inventory before mutate.
3. Cluster API triage and GitOps sync are out of scope — this plugin owns
   Velero CRs via MCP.
4. Non-Velero / filesystem backup products are out of scope — do not absorb
   them here.
