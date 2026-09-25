# grafana

Grafana observability craft — dashboards, Explore, incidents, alerting.
Install when Grafana MCP is available.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `grafana-dashboards` | Dashboard search / update |
| `grafana-explore` | Loki / Prometheus queries |
| `grafana-incidents` | Incident lifecycle |
| `grafana-alerting` | Alert rules / routing |

## Skills

| Skill | Purpose |
| --- | --- |
| `grafana` | Index / gate |

## Commands

- `/grafana` → observability craft

## Pairing

- `global-mcp-first` — Grafana MCP before raw datasource HTTP
- `kubernetes` — correlate pod symptoms with metrics/logs
