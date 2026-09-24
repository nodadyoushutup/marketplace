---
name: framework-docker-ops
description: Designs, changes, validates, and operates Docker images and Compose services for this framework, including API, GUI, worker, beat, RAG, Chroma, and shared MCP runtime containers. Use when editing Dockerfiles, Compose, container entrypoints, mounts, profiles, health checks, dependency installation, image hardening, or MCP service packaging in this repository.
---

# Framework Docker Operations

Operate containers through the repository's runtime and addon model. Keep local
development convenience distinct from immutable production packaging.

## Required preparation

Before editing:

1. Read `AGENTS.md`.
2. Read `framework-runtime-boundaries`,
   `framework-runtime-configuration`, and rules for every affected
   runtime, addon, pack, language, persistence, and documentation boundary.
3. Read `docs/sphinx/source/overview.md`, `runtime.md`,
   `local-development.md` (and related `local-dev-*.md` pages), and `deployment-overview.md`.
4. Read runtime-specific docs and inspect the relevant Dockerfile, entrypoint,
   Compose service, dependencies, mounts, health behavior, and tests.
5. For MCP, RAG, Chroma, secrets, egress, mounts, or supply-chain work, inspect
   the owning implementation, tests, and current primary documentation rather
   than relying on a separate domain playbook.

Use current Docker, Compose Specification, base-image, and dependency-manager
documentation for version-sensitive behavior. Do not apply remembered
`docker-compose` v3 rules to modern `docker compose`.

## 1. Classify the target

Identify both the process role and environment.

### Framework process roles

- **API**: backend discovery, migrations, routes, settings, realtime, and job
  registration.
- **GUI**: browser assets, renderer discovery, and local Vite development.
- **Worker**: asynchronous jobs and queue consumption using
  `applications/worker/Dockerfile.cpu` (default) or `Dockerfile.gpu` (CUDA
  wheels and host GPU). GPU-bound jobs (inference, transcodes) belong on the GPU
  worker, not on API. See `docs/sphinx/source/runtime-worker.md`.
- **Beat**: singleton-style scheduled dispatch using the API image.
- **MCP**: shared FastMCP runtime that discovers selected tool packs.
- **CDN**: thin nginx sidecar (`applications/cdn/Dockerfile`) that serves
  `data/public` and optionally reverse-proxies anonymous S3 GETs.
- **Support service**: Postgres, Redis, Chroma, docs, admin UI, or an approved
  external MCP image.

Do not combine independently scalable roles merely to reduce service count.

### Environment modes

- **Local development**: Compose, source bind mounts, optional profiles, and
  boot-time addon/pack dependency installation are allowed when documented.
- **Production**: use a known addon/pack set, immutable dependencies, deployment
  locks where applicable, platform-managed configuration/secrets, explicit
  resources, and independently observable workloads.

The repository's current API and GUI Dockerfiles are development-oriented. Do
not call them production-ready merely because they build successfully.

See [framework-container-model.md](references/framework-container-model.md).

## 2. Preserve image ownership

- Keep `applications/` images thin packaging and startup hosts.
- Keep shared behavior under `framework/runtimes/`.
- Keep product behavior and dependencies in the owning addon or MCP pack.
- Do not bake one product addon or integration into a generic runtime image.
- Beat shares the API image. Worker uses `applications/worker/Dockerfile.cpu`
  or `Dockerfile.gpu`. The GPU variant adds CUDA PyTorch / ONNX Runtime wheels
  and Compose GPU device access (`worker-gpu` via
  `docker/application/gpu.yaml`). The CPU variant
  adds CPU PyTorch / ONNX Runtime wheels. Do not mount a GPU into API or beat.
  Put CUDA/CPU wheels on the worker runtime requirement files, not addon
  `requirements.txt` (API and beat boot-install that file and will miss
  `/api/ready`). Inference libraries belong in addon `requirements-worker.txt`.
- Keep distinct commands and deployment identities for API, worker, and beat.
- Framework MCP services use `applications/mcp/Dockerfile`; mounted or packaged packs
  define the tool surface.
- Vendor-managed MCP servers remain separate external images and must not be
  mounted as framework packs.
- MCP **proxy variants** of existing vendor servers (GitHub, Jira, AgentMemory,
  Postgres, Google Workspace) may live in **optional separate operator
  repositories** (for example Compose stacks that wrap vendor images). Use them
  for stdio→HTTP/SSE bridges, secret bridging, or minimal build-time patches; do
  not fold that packaging into the shared FastMCP image. A cold clone of this
  repo does not require those sibling trees.

Use a thin derived image when a process role needs extra native stacks the
generic host must not carry (worker CPU/GPU wheels) or when production must
preinstall a selected addon or pack set. The derived image must retain the
shared runtime entrypoint and must not create a second framework implementation.

## 3. Design the dependency lifecycle

### Local development

- API entrypoint may discover and install addon requirements.
- MCP entrypoint may discover and install pack requirements.
- GUI may install addon browser dependencies before generating renderer imports.
- Bind mounts may replace image content for rapid iteration.

This requires writable dependency locations and network access at startup. It is
not an immutable or least-privilege production model.

### Production

- Resolve and preinstall selected runtime/addon/pack dependencies at build time.
- Set `FRAMEWORK_INFRASTRUCTURE__ADDON_REQUIREMENTS_INSTALL=false`,
  `FRAMEWORK_INFRASTRUCTURE__ADDON_GUI_DEPS_INSTALL=false`, or
  `FRAMEWORK_INFRASTRUCTURE__MCP_REQUIREMENTS_INSTALL=false` as applicable.
  See `docs/sphinx/source/immutable-images.md`.
- Package a known addon/pack set and record its release inputs. Optional
  deployment-lock boot verification
  (`FRAMEWORK_INFRASTRUCTURE__DEPLOYMENT_LOCK_VERIFY`) fails closed when
  enabled and the pinned fingerprint mismatches; default remains off for local
  Compose. See `docs/sphinx/source/deployment-overview.md`. Do not treat the
  lock as source-integrity proof of every file byte.
- Avoid bind-mounted application source.
- Verify builds without relying on undeclared internet access at startup.
- Pin compatible dependencies and preserve reproducible lock inputs.

Do not add integration-only packages to generic runtime requirements.

## 4. Review Dockerfiles in context

- Pin base images by immutable digest for framework-owned images.
- Verify the tag, digest, OS, architecture, Python/Node version, and security
  support window together.
- Prefer the base that matches native dependencies and operational needs.
  Do not prefer Alpine or distroless categorically.
- Copy dependency manifests before frequently changing source when that improves
  cache reuse without producing stale dependency layers.
- Use `npm ci` only when a compatible committed lockfile makes it correct.
- Avoid unbounded package upgrades and network downloads in the final runtime
  startup path.
- Keep secrets out of `ARG`, `ENV`, copied files, image history, and build logs.
- Use multi-stage builds when they materially separate build tools or artifacts;
  do not add stages that provide no size, security, or reproducibility benefit.
- Keep `ENTRYPOINT` for required startup behavior and `CMD` for the overridable
  process role.
- Add init handling when the process tree or external image requires signal and
  child-process reaping support.

Non-root users and read-only filesystems are production goals, not assumptions
about current images. Before enabling them, identify every required write:
dependency installation, `/data`, caches, generated GUI imports, temporary
files, browser output, and application state. Use explicit writable mounts or
tmpfs and prove startup, health, and shutdown behavior.

See [dockerfile-and-hardening.md](references/dockerfile-and-hardening.md).

## 5. Treat Compose as the local orchestrator

- Default stack: `docker/application/application.yaml` (all installed addons; Chroma is
  optional and reached via `FRAMEWORK_SETTING__RAG__CHROMA_HOSTNAME` as
  `host:port` — no external Compose network join) from the repository root.
- Docs site: standalone `docker/application/docs.yaml` (nginx serving
  `docs/sphinx/_build/html` on host port `8099`). Not part of the main stack;
  `python3 scripts/docs/build_docs.py` starts/recreates it after a human-run build.
  Agents must not run that build or recreate the docs service unless asked.
- Optional framework MCP packs, Chroma admin, and Playwright MCP may run from
  separate operator Compose stacks when this checkout uses them — not a second
  framework Compose catalog. A cold clone does not require those stacks.
- Operators configure secrets and settings in `docker/.config/env/infrastructure.env`,
  `docker/.config/env/framework.env`, and `docker/.config/env/addons.env`. Optional gitignored
  `docker/.env` is Compose **client** only. Sticky `COMPOSE_FILE` must lead with
  `compose.yaml` (project-directory anchor under `docker/`; Compose v5+ derives
  the project dir from the first entry), then `application/application.yaml`,
  then optional `application/gpu.yaml` and `services/<name>/` data-plane overlays.
  Optional Postgres / Redis / MinIO / SRS / Nginx Proxy Manager under
  `docker/services/<name>/` are mergeable overlays (see
  `docs/sphinx/source/local-dev-optional-stacks.md`) —
  seed `docker/.config/env/<name>.env` from
  `docs/examples/docker/services/<name>.env` before listing that compose file.
  From merged app containers use Compose DNS (`postgres`, `redis`, `minio`, …),
  not `127.0.0.1`. Compose uses no host `${VAR}` for service config. Do not
  patch the shipped core Compose for day-to-day env changes or when adding a
  custom addon — re-run `python3 scripts/workspace/sync_operator_env.py` so the
  new addon `.env.example` is appended as a block.
- Keep production addon selection deployment-owned; the default development
  allowlist must not broaden a separate deployment's mounts or allowlist.
- Do not add the obsolete top-level `version` field.
- Use service-name DNS on the default Compose network unless isolation or policy
  requires explicit networks.
- Model startup dependencies with honest health conditions where startup order
  matters; `depends_on` is not application-level retry or readiness. For the
  framework API, Compose should probe `GET /api/ready` (not only `/api/health`) and have
  GUI/worker/beat wait on `service_healthy`. `worker-cpu` lives in
  `docker/application/application.yaml`; optional `worker-gpu`
  merges `docker/application/gpu.yaml`. Do not reintroduce base or
  API-scale overlay files.
- Mount local source only where the development loop requires it.
- Mount `framework/` and `addons/` into the MCP service (same layout as API).
  Tool selection is `FRAMEWORK_INFRASTRUCTURE__CUSTOM_ADDONS`, not pack-only
  mounts under `/app/mcp/<name>`.
- Keep persistent state in named volumes or documented host data directories.
- Bind published ports to loopback when host-wide exposure is unnecessary.
- Never copy local `.env`, `.cursor`, data, credentials, or generated output
  into an image; keep `.dockerignore` aligned with the build context.

Environment variables are the runtime's process-configuration interface. Secrets
may arrive as environment variables from an approved secret mechanism; the
problem is hard-coded, committed, logged, or over-broadly exposed values, not the
interface alone.

Treat development defaults such as open host bindings, blank ingress keys, or
admin/admin credentials as local-only risks. Do not carry them into production.

## 6. Build framework MCP containers correctly

Inspect the owning pack implementation and tests for tool contracts. Use this
skill for image, Compose, health, and operational delivery.

For a framework MCP service:

1. use `applications/mcp/Dockerfile` or a thin immutable derivative
2. set a distinct `MCP_SERVER_NAME` when multiple MCP services share a host
3. mount `framework/` + `addons/`; honor shared `CUSTOM_ADDONS` (no
   `MCP_PACKS_DIR` / `MCP_ADDONS`)
4. for DB-backed addon tools, bake or install API deps and mount data /
   document required services honestly (slim image is transport-only by default)
5. configure ingress auth, credentials, and egress through approved config
6. add only required upstream dependencies and health conditions
7. use the runtime healthcheck command (`GET /healthz`)
8. verify expected addons in `/healthz`
9. verify authenticated MCP initialization, tool listing, and one approved
   read-only operation when auth is enabled

Generic `/healthz` is liveness plus loaded-addon metadata. It does not prove an
upstream system, database, vector store, or tool-specific operation is ready.
Add and document integration readiness separately when required.

See [mcp-container-checklist.md](references/mcp-container-checklist.md).

## 7. Handle stateful addon services as a coordinated profile

Stateful addon work can involve:

- API for workspace/settings/migration ownership
- worker on an addon-owned queue
- Postgres and Redis
- a persistent external data service
- an addon-owned pack using the shared MCP image
- optional administration services

Do not infer that starting one MCP service alone proves the addon workflow is
available. Verify the required API, worker, source, and data-service lifecycle.

Protect vector data and worker-managed repository caches according to their
separate backup, retention, rebuild, and permission semantics. Administration
UIs and default credentials are development-only unless production security,
auth, exposure, and lifecycle are explicitly designed.

## 8. Apply security and operational gates

- Verify image provenance, version/digest policy, vulnerability status, and
  license expectations for the target environment.
- Verify effective user, capabilities, writable paths, mounts, and filesystem
  policy instead of assuming a Dockerfile directive is sufficient.
- Expose only required ports and document host versus container reachability.
- Keep credentials out of Compose source and rendered logs.
- Review bind mounts for sensitive host paths and write access.
- Document outbound systems and verify the target deployment's actual network
  policy. The repository has no canonical outbound-allowlist file.
- Define CPU, memory, ephemeral storage, replica, disruption, and shutdown
  behavior in production deployment configuration.
- Keep health checks cheap, bounded, secret-safe, and accurate about liveness
  versus readiness.
- Verify graceful signal handling and restart behavior for each process role.

Image scanning, SBOMs, signing, registry promotion, and attestations are valuable
production controls only when the repository's actual CI/release platform
supports and enforces them. Do not claim a pipeline exists without evidence.

## 9. Validate from cheapest to broadest

Run from the repository root:

1. inspect changed Dockerfile, entrypoint, dependency, and ignore inputs
2. run `python3 skills/framework-docker-ops/scripts/inspect_compose.py  # from this plugin root`
3. run `docker compose --project-directory docker -f docker/application/application.yaml config`
4. build only affected services
5. start the smallest required profile/service set
6. inspect `ps` and bounded logs
7. verify service-specific liveness/readiness
8. exercise one representative workflow
9. restart the service and recheck state and discovery
10. broaden to related runtimes when mounts, dependencies, or contracts changed

Do not start, stop, rebuild, or remove unrelated user services. Do not use
`down -v`, prune commands, cache deletion, or destructive volume operations
without explicit authorization. When inspecting reclaimable Docker disk space,
do not assume dangling `<none>` images are safe to delete: after Compose
rebuilds, running containers can still reference untagged intermediate image
IDs while newer `:latest` tags sit unused. Cross-check `docker ps -a --no-trunc`
image IDs before pruning.

For build, startup, health, or runtime failures, read and follow the
`code-systematic-debugging` skill before proposing a fix.

The helper scripts are read-only:

- `scripts/inspect_compose.py` validates rendered Compose configuration and
  reports framework-relevant risks without printing secret values.
- `scripts/check_mcp_health.py` verifies generic MCP health metadata and the
  expected loaded pack set.

## 10. Document and review

Update the root `README.md` and hand-authored Sphinx docs when changing:

- image shape, commands, or dependency installation
- service/profile names, ports, mounts, or upstream dependencies
- environment variables, secrets, precedence, or restart requirements
- health/readiness, persistence, backup, migration, or rollback behavior
- tool exposure, auth, egress, or trust boundaries

Use the available code-review workflow for substantive runtime/container
changes. Use the built-in security-review workflow only when the user
explicitly requests a dedicated security review.

Do not consider the work complete until material findings are resolved and the
smallest relevant runtime workflow has been demonstrated.

## Deliverables

For a substantive container change, report:

1. affected process roles and environment mode
2. image, addon/pack, dependency, configuration, and mount boundaries
3. persistence, health, network, security, and secret implications
4. exact validation commands and observed results
5. rollout, restart, migration, and rollback requirements
6. documentation and review status
