# grafana

Grafana observability craft — dashboards, Explore, incidents, alerting.
Install when Grafana MCP is available.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `grafana-dashboards` | Dashboard search / update |
| `grafana-explore` | Explore logs / metrics / traces datasources |
| `grafana-incidents` | Incident lifecycle |
| `grafana-alerting` | Alert rules / routing |

## Skills

| Skill | Purpose |
| --- | --- |
| `grafana` | Index / gate |

## Commands

- `/grafana` → observability craft

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/grafana-workflow.drawio`](docs/grafana-workflow.drawio) — gate → act → evidence
