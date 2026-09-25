# Framework Container Model

## Runtime ownership

The application is a composition of generic runtime processes and selected
addons or MCP packs.

| Process | Image/runtime | Owns |
| --- | --- | --- |
| API | `applications/api/Dockerfile` | Backend discovery, persistence, migrations, routes, settings, realtime, job registration |
| Worker | `applications/worker/Dockerfile.cpu` (default) or `Dockerfile.gpu` (API image + CUDA wheels), Celery worker command | Asynchronous job execution for selected queues; GPU variant is the accelerator role |
| Beat | API image, Celery beat command | Singleton scheduled dispatch (one Compose replica; duplicates double-fire jobs) |
| GUI | `applications/gui/Dockerfile` | Browser runtime, renderer discovery, local Vite development |
| MCP | `applications/mcp/Dockerfile` | FastMCP process, shared addon discovery, transports, ingress auth, generic health |
| CDN | `applications/cdn/Dockerfile` | nginx public-attachment sidecar (`data/public` + optional anonymous S3 proxy) |
| Addon MCP | `addons/<name>/mcp/` via shared `CUSTOM_ADDONS` | Integration tools and MCP-specific dependencies |
| Addon | Mounted or packaged under addon roots | Product functionality and runtime-specific dependencies |

Keep these process roles independently deployable. Sharing an image does not
make API, worker, and beat one workload.

## Local development

`docker/application/application.yaml` is the default all-addon local orchestrator.
Addon-owned external services are optional. Configure their endpoints in the
owning addon's block in `docker/.config/env/addons.env`; Compose does not automatically join
external product networks. Optional MCP and administration services run from
their owning stacks when used, not this Compose file.

Expected characteristics:

- source bind mounts replace copied image content
- addon and pack dependencies may install at container startup
- GUI dependencies and generated imports may be refreshed at startup
- optional MCP/admin services may run from separate operator Compose stacks when used; a cold clone does not require them
- named volumes preserve Postgres, Redis, and Node dependency state
- service-name DNS connects containers on the Compose network; RAG clients dial
  a host-published Chroma address when configured
- developer-facing ports may be published to the host

These choices optimize iteration, not immutability or least privilege.

## Production packaging

Production uses the same process boundaries under a production orchestrator,
commonly Kubernetes, with different packaging and policy:

- preinstall a known addon/pack set and dependencies
- disable boot-time requirement installation
- record the selected addon set; optional
  `FRAMEWORK_INFRASTRUCTURE__DEPLOYMENT_LOCK_VERIFY` fails closed on fingerprint
  mismatch when enabled (default off). The lock is release inventory / an
  optional boot gate, not source-integrity proof of every file byte — see
  `docs/sphinx/source/deployment-overview.md`
- avoid application source bind mounts
- inject process configuration and secrets through platform mechanisms
- set resources, replicas, probes, disruption policy, and shutdown grace
- define persistent storage, backup, restore, and migration ownership
- promote verified immutable images

The repository documents both baked and release-tool-controlled addon patterns.
Either pattern must produce a known, auditable runtime input set.

## Current image realities

Treat these as observations, not desired guarantees:

- API installs **runtime** requirements only (`requirements.txt`). Pytest/ruff
  stay on `requirements-dev.txt` for local/CI hosts. Optional
  `FRAMEWORK_BAKE_ADDON_REQUIREMENTS=1` bakes discovered addon Python deps.
  Worker-cpu and worker-gpu derive from that image; CPU adds CPU torch
  wheels and GPU adds CUDA wheels. See `docs/sphinx/source/immutable-images.md`.
- GUI production image bakes framework-addon `dist/` at image build (assemble,
  optional addon npm install, Vite build) and defaults to serve-only start.
  Compose still overrides to Vite dev. Generate-on-start
  (`start:production`) can still install missing mounted-addon specs unless
  `FRAMEWORK_INFRASTRUCTURE__ADDON_GUI_DEPS_INSTALL=false`.
- API and MCP entrypoints support boot-time dependency installation with
  explicit disable flags for immutable deployments.
- Framework-owned API, GUI, and MCP Dockerfiles pin base images by digest.
- Compose contains a mixture of pinned, tagged, and `latest` external images.
- Current framework images do not establish a universal non-root/read-only
  filesystem contract.
- Health coverage is uneven across local services.

Do not encode current development compromises as production policy.

## Configuration ownership

Environment variables configure process startup, connectivity, credentials,
queues, paths, transports, and topology. Persisted application settings affect
runtime behavior only when the owning code reads them.

Keep aligned across API, worker, and beat when applicable:

- database URL
- broker and result backend
- timezone and queue names
- addon roots
- realtime/message queue settings

MCP runtime configuration is separate from persisted pack/addon settings.

## Persistence map

- Postgres volume: framework and addon relational state
- Redis volume: broker/result/realtime development state as configured
- Chroma volume: vector collections
- `data/`: application-managed data and worker caches
- GUI Node volume: local dependency cache
- Playwright output directory: generated browser artifacts

Before changing a mount or volume, identify owner, mutability, backup, restore,
retention, permissions, migration, and deletion behavior.

## Restart and rollout

Restart affected processes when their discovery or startup inputs change:

- API: manifests, models, migrations, routes, settings, jobs, pages, widgets
- Worker: job or dependency code
- Beat: schedule definitions
- GUI: addon entrypoints, renderers, browser dependencies
- MCP: pack manifests, registration, dependencies, mounts, auth, or runtime config

Schema migrations remain API-owned. Worker/beat/MCP rollout must remain compatible
with the migrated application state.
