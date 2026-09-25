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

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/minio-workflow.drawio`](docs/minio-workflow.drawio) — gate → act → evidence
