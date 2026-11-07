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

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `kubernetes` — IngressRoute / Middleware CRDs
- `authentik` — forward-auth / SSO
- `nginx-proxy-manager` — sibling reverse-proxy craft (do not mix)
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/traefik-workflow.drawio`](docs/traefik-workflow.drawio) — gate → act → evidence
