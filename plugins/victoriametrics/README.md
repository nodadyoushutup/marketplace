# victoriametrics

Agnostic VictoriaMetrics craft: discover metrics/labels, MetricsQL/PromQL query and range, TSDB status, and alerts/rules via MCP. Prefer VictoriaMetrics MCP; discover before guessing.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `victoriametrics-discover` | Discover metrics/labels/series and TSDB status before complex MetricsQL |
| `victoriametrics-query` | Instant and range queries: rate-then-sum; bound cardinality |

## Skills

| Skill | Purpose |
| --- | --- |
| `victoriametrics` | Index / gate |

## Commands

- `/victoriametrics` → VictoriaMetrics discover or query

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `prometheus` — Prometheus-server-specific Prom API
- `grafana` — dashboards / Explore UX
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/victoriametrics-workflow.drawio`](docs/victoriametrics-workflow.drawio) — gate → act → evidence
