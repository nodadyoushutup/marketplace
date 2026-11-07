---
name: traefik
description: >-
  Agnostic Traefik craft: routers, services, middlewares, and IngressRoute shape
  with destructive gates. Prefer MCP when connected; otherwise API/manifests.
  Skip when the user did not authorize this surface.
---

# traefik

## Gate

No explicit Traefik / IngressRoute / router / middleware ask → **skip**. Nginx
Proxy Manager asks belong in `nginx-proxy-manager`; Caddy in its own plugin when
present. Prefer a connected MCP (`global-mcp-first`); else Traefik API or
Kubernetes CRDs/file provider with a resolved entrypoint.

## Load map

| Need | Rule |
| --- | --- |
| List / craft routers, services, middlewares, CRDs | `traefik-routes` |
| Delete / expose / TLS wipe gates | `traefik-safety` |

## Defaults

1. Never invent router, service, or middleware names — list/resolve first.
2. Prefer update-in-place over delete+recreate for host/path changes.
3. Pair with `kubernetes` for IngressRoute/CRDs and `authentik` for forward-auth.
4. This plugin owns Traefik routing craft — not NPM or Caddy.
