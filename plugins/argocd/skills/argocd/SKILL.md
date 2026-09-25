---
name: argocd
description: >-
  Agnostic Argo CD craft: list/get apps, sync status, and gated sync/action via MCP. Prefer Argo CD MCP; never invent app names. Skip when the user did not authorize this surface.
---

# argocd

## Gate

No explicit Argo / Application / sync ask and no named app → **skip**. Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| List / get / tree / events | `argocd-apps` |
| Sync / refresh / actions | `argocd-sync` |

## Defaults

1. Never invent Application name, namespace, or project.
2. Read status/events before syncing.
3. Pair with `kubernetes` for pod triage; this plugin owns GitOps apps.
4. Site overlays stay in private `homelab` — keep this plugin agnostic.
