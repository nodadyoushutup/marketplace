# runpod

Agnostic RunPod craft: list pods/endpoints/templates/GPUs and gated create/start/stop/delete via MCP. Prefer RunPod MCP; never invent pod or endpoint ids; cost-aware defaults.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `runpod-inventory` | List pods, endpoints, templates, GPU types, and billing via MCP |
| `runpod-safety` | Create/start/stop/delete need an explicit verb; cost-aware; no secret dumps |

## Skills

| Skill | Purpose |
| --- | --- |
| `runpod` | Index / gate |

## Commands

- `/runpod` → RunPod inventory or gated mutate

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/runpod-workflow.drawio`](docs/runpod-workflow.drawio) — gate → act → evidence
