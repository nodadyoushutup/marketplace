---
name: authentik
description: >-
  Agnostic Authentik IdP craft: applications, providers, flows, and groups with
  gated destructive changes. Prefer MCP when connected; otherwise API/UI. Skip
  when the user did not authorize this surface.
---

# authentik

## Gate

No explicit Authentik / IdP / OIDC/SAML app / SSO flow ask → **skip**. Authelia
or Keycloak asks belong in their own plugins when present — do not absorb them
here. Prefer a connected MCP (`global-mcp-first`); else API or UI with a resolved
base URL.

## Load map

| Need | Rule |
| --- | --- |
| List / craft apps, providers, flows, groups | `authentik-apps` |
| Delete / disable / broad ACL risk | `authentik-safety` |

## Defaults

1. Never invent application, provider, flow, or group ids — list/resolve first.
2. Resolve the Authentik base URL from config/MCP/env — never hardcode a host.
3. Prefer update-in-place over delete+recreate for provider/client changes.
4. Pair with `nginx-proxy-manager` / `traefik` for edge auth wiring; this plugin
   owns Authentik IdP craft.
