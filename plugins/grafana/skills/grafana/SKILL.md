---
name: grafana
description: >-
  Grafana craft: search dashboards, Explore logs/metrics, manage incidents and
  alert rules via MCP. Prefer Grafana MCP. Skip when the user did not
  authorize observability work.
---

# Grafana

## Gate

No explicit Grafana / Loki / Prometheus / alert / incident / dashboard ask →
**skip**. Prefer a connected Grafana MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Dashboards / folders / panels | `grafana-dashboards` |
| Explore logs / metrics / traces | `grafana-explore` |
| Incidents | `grafana-incidents` |
| Alert rules / routing | `grafana-alerting` |

## Defaults

1. Never invent dashboard UID, datasource UID, or folder id.
2. Discover metric/label names before complex PromQL/LogQL.
3. Prefer live MCP queries over guessing from memory.
4. Operator replies: short findings + deep link when MCP can generate one
   (`global-host-url` — no localhost).
