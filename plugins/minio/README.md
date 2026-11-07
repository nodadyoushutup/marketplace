# minio

Agnostic MinIO / S3 craft: buckets, objects, tags, and gated delete via MCP. Prefer MinIO MCP; never invent bucket names; refuse secret dumps.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `minio-objects` | List buckets/objects, read metadata, and upload/download via MCP after resolving names |
| `minio-safety` | Delete bucket/object and public ACL changes need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `minio` | Index / gate |

## Commands

- `/minio` → MinIO bucket/object craft

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/minio-workflow.drawio`](docs/minio-workflow.drawio) — gate → act → evidence
