---
name: kubernetes
description: >-
  Agnostic Kubernetes triage: pods, events, logs, and node summary via MCP.
  Prefer Kubernetes MCP. Skip when the user did not authorize cluster work.
  Destructive actions need an explicit ask.
---

# Kubernetes

## Gate

No explicit Kubernetes / pod / namespace / cluster ask and no named workload →
**skip**. Prefer a connected Kubernetes MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Pod / workload status | `kubernetes-triage` |
| Logs / previous crash | `kubernetes-logs` |
| Delete / scale / exec risk | `kubernetes-safety` |

## Defaults

1. Never invent cluster context, namespace, or pod names — list/resolve.
2. Read-only triage is the default (get/list/log/events).
3. Pair with `grafana` for metrics; this plugin owns k8s API triage.
4. Site-specific overlays stay in private `homelab` — keep this plugin
   agnostic.
