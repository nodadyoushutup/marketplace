---
name: authentik
description: >-
  Agnostic Authentik IdP craft: applications, providers, flows, and groups with
  gated destructive changes. Prefer MCP when connected; otherwise API/UI. Skip
  when the user did not authorize this surface.
---

# authentik

## Gate

No explicit Authentik ask → **skip**. Other IdP / OIDC/SAML products are out
of scope — do not absorb them here. Prefer a connected MCP; else API or UI
with a resolved base URL.

## Load map

| Need | Rule |
| --- | --- |
| List / craft apps, providers, flows, groups | `authentik-apps` |
| Delete / disable / broad ACL risk | `authentik-safety` |

## Defaults

1. Never invent application, provider, flow, or group ids — list/resolve first.
2. Resolve the Authentik base URL from config/MCP/env — never hardcode a host.
3. Prefer update-in-place over delete+recreate for provider/client changes.
4. Edge reverse-proxy wiring is out of scope — this plugin owns Authentik IdP
   craft.
