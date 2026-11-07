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

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/victoriametrics-workflow.drawio`](docs/victoriametrics-workflow.drawio) — gate → act → evidence
