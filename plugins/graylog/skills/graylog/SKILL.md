---
name: graylog
description: >-
  Agnostic Graylog craft: search logs, streams, and fields via MCP. Prefer Graylog MCP; never invent stream ids; keep secrets out of chat. Skip when the user did not authorize this surface.
---

# graylog

## Gate

No explicit Graylog / log search ask → **skip**. Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Search / context / aggregate | `graylog-search` |
| Redaction / dump refuse | `graylog-safety` |

## Defaults

1. Never invent stream id or index set — list/resolve.
2. Bound time ranges; start narrow.
3. Pair with `grafana` Loki Explore when that path is preferred; this plugin owns Graylog.
