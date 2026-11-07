---
name: home-assistant
description: >-
  Agnostic Home Assistant craft: entity/state inventory, service calls, and
  automation hygiene with gated destructive actions. Prefer MCP when connected;
  otherwise API/UI. Skip when the user did not authorize this surface.
---

# home-assistant

## Gate

No explicit Home Assistant / entity / automation / service-call ask → **skip**.
Prefer a connected MCP (`global-mcp-first`); else HA REST/WebSocket API or UI
with a resolved base URL.

## Load map

| Need | Rule |
| --- | --- |
| List entities / states / areas | `home-assistant-entities` |
| Service calls / automation mutate gates | `home-assistant-safety` |

## Defaults

1. Never invent entity_id — list/resolve first (`light.`, `switch.`, `sensor.`…).
2. Resolve the HA base URL from config/MCP/env — never hardcode a host.
3. Prefer targeted service calls over restarting Home Assistant.
4. Never paste long-lived access tokens into chat.
