# graylog

Agnostic Graylog craft: search logs, streams, and fields via MCP. Prefer Graylog MCP; never invent stream ids; keep secrets out of chat.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `graylog-search` | Search logs via MCP with explicit query + time range |
| `graylog-fluent-bit` | Fluent Bit / shipper → Graylog portable hygiene |
| `graylog-safety` | Do not dump full private payloads or credentials into chat |

## Skills

| Skill | Purpose |
| --- | --- |
| `graylog` | Index / gate |

## Commands

- `/graylog` → Graylog search

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/graylog-workflow.drawio`](docs/graylog-workflow.drawio) — gate → act → evidence
