---
name: argocd
description: >-
  Agnostic Argo CD craft: list/get apps, sync status, and gated sync/action via MCP. Prefer Argo CD MCP; never invent app names. Skip when the user did not authorize this surface.
---

# argocd

## Gate

No explicit Argo CD / Application / sync ask and no named Argo CD app →
**skip**. Bare “GitOps” without Argo CD is out of scope. Prefer a connected
MCP.

## Load map

| Need | Rule |
| --- | --- |
| List / get / tree / events | `argocd-apps` |
| Sync / refresh / actions | `argocd-sync` |

## Defaults

1. Never invent Application name, namespace, or project.
2. Read status/events before syncing.
3. Pod triage is out of scope — this plugin owns Argo CD Applications.
4. Site overlays stay in private site repos — keep this plugin agnostic.
