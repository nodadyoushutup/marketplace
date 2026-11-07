---
name: portainer
description: >-
  Agnostic Portainer craft: endpoint/stack/container inventory and gated
  stack/container mutations. Prefer MCP when connected; otherwise API/UI. Skip
  when the user did not authorize this surface.
---

# portainer

## Gate

No explicit Portainer / Docker UI stack / endpoint ask → **skip**. Raw Compose
MCP; else Portainer API/UI with a resolved base URL.

## Load map

| Need | Rule |
| --- | --- |
| List endpoints / stacks / containers | `portainer-inventory` |
| Deploy / stop / delete / prune gates | `portainer-safety` |

## Defaults

1. Never invent endpoint, stack, or container ids — list/resolve first.
2. Resolve the Portainer base URL from config/MCP/env — never hardcode a host.
3. Prefer compose for checked-in Compose authorship; this plugin owns Portainer
   UI/API ops against live endpoints.
4. Never paste API tokens or env secret values into chat.
