# graylog

Agnostic Graylog craft: search logs, streams, and fields via MCP. Prefer Graylog MCP; never invent stream ids; keep secrets out of chat.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `graylog-search` | Search logs via MCP with explicit query + time range |
| `graylog-safety` | Do not dump full private payloads or credentials into chat |

## Skills

| Skill | Purpose |
| --- | --- |
| `graylog` | Index / gate |

## Commands

- `/graylog` → Graylog search

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/graylog-workflow.drawio`](docs/graylog-workflow.drawio) — gate → act → evidence
