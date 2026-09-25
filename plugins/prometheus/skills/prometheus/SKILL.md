---
name: prometheus
description: >-
  Agnostic Prometheus craft: discover metrics/labels, PromQL instant/range queries, and targets health via MCP. Prefer Prometheus MCP; discover before guessing. Skip when the user did not authorize this surface.
---

# prometheus

## Gate

No explicit Prometheus / PromQL / metrics / targets ask → **skip**. Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Discover metrics / labels / targets | `prometheus-discover` |
| Instant / range query | `prometheus-query` |

## Defaults

1. Discover before query — do not guess metric names.
2. Prefer live MCP queries over remembered PromQL.
3. Pair with `grafana` for dashboards/Explore UX; this plugin owns Prom API.
4. VictoriaMetrics / other PromQL backends: same discovery discipline.
