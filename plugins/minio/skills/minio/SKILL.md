---
name: minio
description: >-
  Agnostic MinIO / S3 craft: buckets, objects, tags, and gated delete via MCP. Prefer MinIO MCP; never invent bucket names; refuse secret dumps. Skip when the user did not authorize this surface.
---

# minio

## Gate

No explicit MinIO / S3 / bucket / object ask → **skip**. Prefer a connected MCP (`global-mcp-first`).

## Load map

| Need | Rule |
| --- | --- |
| Buckets / objects / tags | `minio-objects` |
| Delete / ACL risk | `minio-safety` |

## Defaults

1. Never invent bucket or object keys — list/resolve.
2. Prefer MinIO MCP(s) when ready (`global-mcp-first`).
3. Pair with `vault` for credential storage — not chat.
