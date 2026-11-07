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
Prefer a connected Kubernetes MCP (`global-mcp-first`) for live cluster work.

## Load map

| Need | Rule |
| --- | --- |
| Write / review manifests | `kubernetes-manifests` (+ `code-yaml`) |
| Pod / workload status | `kubernetes-triage` |
| Logs / previous crash | `kubernetes-logs` |
| ExternalSecret / SecretStore (ESO) | `kubernetes-external-secrets` (+ `vault-external-secrets`) |
| MetalLB / ingress-nginx / CNPG / Redis | `kubernetes-addons` |
| Delete / scale / exec / apply risk | `kubernetes-safety` |

## Defaults

1. Never invent cluster context, namespace, or pod names — list/resolve.
2. Read-only triage is the default (get/list/log/events).
3. Manifest edits follow `code-yaml` then `kubernetes-manifests`; do not
   encode site GitOps paths or secret-store layout here.
4. Pair with `grafana` for metrics; this plugin owns k8s API triage and
   portable manifest craft.
5. Site-specific overlays stay in private `homelab` — keep this plugin
   agnostic.
6. ESO payloads live in Vault — pair `kubernetes-external-secrets` with
   `vault`; never commit plaintext Secrets beside ExternalSecrets.
