---
name: freshservice
description: >-
  Agnostic Freshservice ITSM craft: create-only ticket filing with clear
  description shape, status honesty, and no invented workspace ids. Prefer
  Freshservice MCP when ready. Skip when the user did not authorize ITSM work.
---

# Freshservice

## Gate

No explicit Freshservice / ticket / incident / service-request ask and no
named ticket id → **skip**. Prefer a connected Freshservice MCP when ready
(`global-mcp-first`); otherwise use the operator’s configured API path once —
do not invent credentials.

## Load map

| Need | Rule |
| --- | --- |
| May I create? | `freshservice-create` |
| Ticket body shape | `freshservice-ticket` |
| Status / priority / assign | `freshservice-status` |

## Defaults

1. Create-only unless the user adds an explicit implement verb.
2. Never invent workspace, group, requester, or category ids.
3. Keep status honest — do not mark resolved without evidence.
4. Pair with `business-analyst` when shaping vague requests before filing.
