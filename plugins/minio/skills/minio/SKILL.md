---
name: minio
description: >-
  Agnostic MinIO / S3 craft: buckets, objects, tags, and gated delete via MCP. Prefer MinIO MCP; never invent bucket names; refuse secret dumps. Skip when the user did not authorize this surface.
---

# minio

## Gate

No explicit MinIO ask (or MinIO MCP/instance in play for S3-compatible
buckets/objects) → **skip**. Bare “S3 / bucket” for another object store is
out of scope. Prefer a connected MCP.

## Load map

| Need | Rule |
| --- | --- |
| Buckets / objects / tags | `minio-objects` |
| Delete / ACL risk | `minio-safety` |

## Defaults

1. Never invent bucket or object keys — list/resolve.
2. Prefer MinIO MCP(s) when ready.
3. Credentials belong in a secret store or env — not chat.
