# MCP Container Checklist

Use with the owning addon `mcp/` implementation, tests, and runtime documentation.

## Boundary

- [ ] Framework addon contribution versus external standalone image is explicit
- [ ] Shared runtime owns FastMCP, transport, ingress auth, and generic health
- [ ] Addon `mcp/` owns integration tools and MCP-specific behavior
- [ ] Separate services are used for different trust, credentials, egress,
      mutation policy, or scaling requirements (different `CUSTOM_ADDONS` /
      keys — not a second allowlist env var)

## Development service

- [ ] Build uses `applications/mcp/Dockerfile`
- [ ] `MCP_SERVER_NAME` is distinct when multiple MCP services share a host
- [ ] Shared `CUSTOM_ADDONS` + `/app/addons` (and `/app/framework`) mounts
- [ ] No `MCP_PACKS_DIR` / per-pack `/app/mcp/<name>` mounts
- [ ] Data/DB mounts and deps are present when selected addons need them
- [ ] Required Postgres, Chroma, or other dependencies have honest startup conditions
- [ ] Optional service has the appropriate profile
- [ ] Published port and host bind are intentional (prefer loopback when possible)
- [ ] Ingress API key behavior is documented and tested
- [ ] Runtime healthcheck command is configured

## Immutable production image

- [ ] Thin image derives from the generic MCP runtime
- [ ] Selected addons and required dependencies are copied/preinstalled
- [ ] `FRAMEWORK_INFRASTRUCTURE__MCP_REQUIREMENTS_INSTALL=false` when baked
- [ ] No source bind mounts are required
- [ ] Runtime entrypoint and `python -m framework.runtimes.mcp serve` remain intact
- [ ] Image records a known addon set and compatible versions
- [ ] Effective user and writable paths are tested
- [ ] Resource, replica, probe, shutdown, and disruption policy are defined

## Configuration and security

- [ ] Secrets come from approved mechanisms; never baked into the image
- [ ] Non-loopback binds require `MCP_API_KEY` (default Compose binds
      `0.0.0.0` and does **not** set `MCP_ALLOW_UNAUTHENTICATED_NON_LOOPBACK`;
      init fills a blank `MCP_API_KEY` in `infrastructure.env`)
- [ ] Health endpoints do not disclose secrets
- [ ] Egress destinations for selected tools are approved
- [ ] Clients (Cursor) send the same key as `x-api-key`

## Verification

- [ ] `/healthz` lists expected addons
- [ ] Unselected custom addons contribute no tools
- [ ] Authenticated tool listing works when a key is configured
- [ ] One approved read-only tool call succeeds (when deps are up)
