---
name: victoriametrics
description: >-
  Agnostic VictoriaMetrics craft: discover metrics/labels, MetricsQL/PromQL
  query and range, TSDB status, and alerts/rules via MCP. Prefer VictoriaMetrics
  MCP; discover before guessing. Skip when the user did not authorize this surface.
---

# victoriametrics

## Gate

No explicit VictoriaMetrics / MetricsQL / VM / vmselect / vmalert ask → **skip**.
Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Discover metrics / labels / series / TSDB | `victoriametrics-discover` |
| Instant / range query | `victoriametrics-query` |

## Defaults

1. Discover before query — do not guess metric names.
2. Prefer live MCP queries over remembered MetricsQL/PromQL.
3. Bound cardinality; prefer rate-then-sum on counters.
4. Pair with `prometheus` when the ask is Prometheus-server-specific; pair with
   `grafana` for dashboards/Explore UX. This plugin owns VictoriaMetrics MCP.
