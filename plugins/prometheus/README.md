# prometheus

Agnostic Prometheus craft: discover metrics/labels, PromQL instant/range queries, and targets health via MCP. Prefer Prometheus MCP; discover before guessing.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `prometheus-discover` | Discover metric and label names (`label_values`, `series`, `metric_metadata`) before writing complex PromQL |
| `prometheus-query` | Instant and range queries: prefer rate-then-sum; keep cardinality bounded; never invent metric names |

## Skills

| Skill | Purpose |
| --- | --- |
| `prometheus` | Index / gate |

## Commands

- `/prometheus` → Prometheus discover or query

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/prometheus-workflow.drawio`](docs/prometheus-workflow.drawio) — gate → act → evidence
