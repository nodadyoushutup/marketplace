# traefik

Agnostic Traefik craft: routers, services, middlewares, and IngressRoute shape with destructive gates. Prefer MCP when connected; otherwise API/manifests. Never invent router names.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `traefik-routes` | List/craft routers, services, middlewares, IngressRoute CRDs |
| `traefik-safety` | Delete/expose/TLS drop need an explicit verb naming the object |

## Skills

| Skill | Purpose |
| --- | --- |
| `traefik` | Index / gate |

## Commands

- `/traefik` → Traefik routes or gated mutate

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/traefik-workflow.drawio`](docs/traefik-workflow.drawio) — gate → act → evidence
