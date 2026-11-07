---
name: traefik
description: >-
  Agnostic Traefik craft: routers, services, middlewares, and IngressRoute shape
  with destructive gates. Prefer MCP when connected; otherwise API/manifests.
  Skip when the user did not authorize this surface.
---

# traefik

## Gate

No explicit Traefik / IngressRoute / router / middleware ask → **skip**. Other
reverse-proxy products are out of scope — do not absorb them here. Prefer a
connected MCP; else Traefik API or Kubernetes CRDs/file provider with a
resolved entrypoint.

## Load map

| Need | Rule |
| --- | --- |
| List / craft routers, services, middlewares, CRDs | `traefik-routes` |
| Delete / expose / TLS wipe gates | `traefik-safety` |

## Defaults

1. Never invent router, service, or middleware names — list/resolve first.
2. Prefer update-in-place over delete+recreate for host/path changes.
3. This plugin owns Traefik routing craft only.
