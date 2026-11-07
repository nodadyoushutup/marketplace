---
name: nginx-proxy-manager
description: >-
  Agnostic Nginx Proxy Manager craft: proxy hosts, SSL certificates, and access
  lists with destructive gates. Prefer MCP when connected; otherwise API/UI.
  Skip when the user did not authorize this surface.
---

# nginx-proxy-manager

## Gate

No explicit Nginx Proxy Manager / NPM / proxy host / SSL cert ask → **skip**.
Prefer a connected MCP (`global-mcp-first`); else API or browser UI with resolved
base URL. Traefik/Caddy asks belong in their own plugins when present — do not
absorb them here.

## Load map

| Need | Rule |
| --- | --- |
| List / create / update proxy hosts, SSL, access lists | `nginx-proxy-manager-hosts` |
| Delete / disable / cert wipe gates | `nginx-proxy-manager-safety` |

## Defaults

1. Never invent proxy-host, certificate, or access-list ids — list/resolve first.
2. Resolve the NPM base URL from config/MCP/env — never hardcode a host.
3. Prefer update-in-place over delete+recreate for domain or upstream changes.
4. Pair with `cloudflare` for public DNS; this plugin owns NPM proxy/SSL craft.
