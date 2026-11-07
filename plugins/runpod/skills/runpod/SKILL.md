---
name: runpod
description: >-
  Agnostic RunPod craft: list pods/endpoints/templates/GPUs and gated
  create/start/stop/delete via MCP. Prefer RunPod MCP; never invent pod or
  endpoint ids; cost-aware defaults. Skip when the user did not authorize this
  surface.
---

# runpod

## Gate

No explicit RunPod / GPU cloud / pod / serverless endpoint ask → **skip**.
Prefer a connected MCP.

## Load map

| Need | Rule |
| --- | --- |
| List pods / endpoints / templates / GPUs | `runpod-inventory` |
| Create / start / stop / delete / cancel gates | `runpod-safety` |

## Defaults

1. Never invent pod, endpoint, template, or job ids — list/resolve first.
2. Read inventory before mutate.
3. Prefer the cheapest GPU that meets the stated need; state cost impact when
   creating or leaving resources running.
4. Never paste API keys, registry passwords, or env secret values into chat.
