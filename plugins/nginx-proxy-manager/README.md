# nginx-proxy-manager

Agnostic Nginx Proxy Manager craft: proxy hosts, SSL certificates, and access lists with destructive gates. Prefer MCP when connected; otherwise API/UI. Never invent host ids.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `nginx-proxy-manager-hosts` | List/create/update proxy hosts, SSL certs, and access lists |
| `nginx-proxy-manager-safety` | Delete/disable/cert wipe need an explicit verb naming the object |

## Skills

| Skill | Purpose |
| --- | --- |
| `nginx-proxy-manager` | Index / gate |

## Commands

- `/nginx-proxy-manager` → NPM hosts or gated mutate

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/nginx-proxy-manager-workflow.drawio`](docs/nginx-proxy-manager-workflow.drawio) — gate → act → evidence
