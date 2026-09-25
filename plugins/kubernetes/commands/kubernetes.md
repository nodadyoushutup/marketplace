---
name: kubernetes
description: >-
  Triage Kubernetes pods, events, and logs with read-first craft (MCP first).
---

# /kubernetes

1. If the user did not authorize cluster work and named no workload, say so
   and stop.
2. Load `kubernetes` and follow `kubernetes-triage` / `kubernetes-logs` /
   `kubernetes-safety`.
3. Prefer Kubernetes MCP. Never invent namespaces or pod names.
4. Return status + short log/event evidence.
