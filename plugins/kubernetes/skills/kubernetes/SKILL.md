---
name: kubernetes
description: >-
  Agnostic Kubernetes craft: portable manifest authoring plus pods, events,
  logs, and node summary via MCP. Prefer Kubernetes MCP. Skip when the user
  did not authorize cluster or manifest work. Destructive actions need an
  explicit ask.
---

# Kubernetes

## Gate

No explicit Kubernetes / pod / namespace / cluster / manifest ask → **skip**.
Prefer a connected Kubernetes MCP for live cluster work.

## Load map

| Need | Rule |
| --- | --- |
| Write / review manifests | `kubernetes-manifests` |
| Pod / workload status | `kubernetes-triage` |
| Logs / previous crash | `kubernetes-logs` |
| ExternalSecret / SecretStore | `kubernetes-external-secrets` |
| Load balancer / ingress / Postgres operator / cache | `kubernetes-addons` |
| Delete / scale / exec / apply risk | `kubernetes-safety` |

## Defaults

1. Never invent cluster context, namespace, or pod names — list/resolve.
2. Read-only triage is the default (get/list/log/events).
3. Manifest edits follow `kubernetes-manifests` (YAML floor is in that rule);
   do not encode site GitOps paths or secret-store layout here.
4. Metrics and dashboards are out of scope — this plugin owns k8s API triage
   and portable manifest craft.
5. Site-specific overlays stay in private site repos — keep this plugin
   agnostic.
6. External-secret payloads live in the project's secret provider — never
   commit plaintext Secrets beside ExternalSecrets.
