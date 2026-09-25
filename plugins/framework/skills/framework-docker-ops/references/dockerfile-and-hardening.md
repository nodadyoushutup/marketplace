# Dockerfile and Hardening Review

## Build inputs

- Confirm the intended build context and Dockerfile path.
- Inspect `.dockerignore`; exclude local data, virtual environments, dependency
  trees, caches, editor metadata, logs, secrets, and generated artifacts.
- Copy only files required by the target runtime.
- Keep dependency manifests in cache-friendly layers.
- Do not rely on a bind mount to conceal a broken image during production review.

## Base images

- Prefer official or explicitly approved sources.
- Pin framework-owned production inputs by digest.
- Record tag and digest: the tag explains lineage; the digest provides immutability.
- Verify supported architecture, libc, native library, Python/Node, and TLS needs.
- Rebuild regularly to consume approved security fixes; digest pinning does not
  update itself.
- Do not use `latest` for a controlled deployment.

Alpine, slim, and distroless are trade-offs:

- Alpine can increase native-wheel and libc compatibility work.
- Slim images may be larger but align better with Python binary dependencies.
- Distroless reduces runtime utilities but complicates boot installers,
  diagnostics, shells, and dynamic extension models.

Choose from measured compatibility and operational requirements.

## Package installation

- Pin or constrain application dependencies with tested compatibility.
- Avoid unconstrained upgrades during image build or startup.
- Use package-manager cache controls without hiding useful failure evidence.
- Remove OS package metadata in the same layer when appropriate.
- Keep compilers and build-only headers out of the final stage when a multi-stage
  build materially helps.
- Never pass package registry credentials through persistent build arguments.

## Entrypoint and command

- Entrypoint performs mandatory setup, then `exec`s the target process.
- Command identifies the overridable process role.
- Setup must be bounded, idempotent where necessary, and fail visibly.
- Do not run migrations or dependency installation from every process role unless
  that ownership is explicit.
- Verify PID 1 signal handling, child reaping, graceful shutdown, and exit codes.

## User and filesystem

For a non-root/read-only production target:

1. inventory writes during build, entrypoint, startup, health, and normal operation
2. preinstall dependencies and disable boot-time installers
3. create an explicit runtime user and ownership during build
4. provide writable `/data`, cache, temp, or output mounts only where required
5. remove unnecessary Linux capabilities and privileged access
6. test startup, jobs, health, logs, shutdown, and restart under final policy

Do not add `USER` or `read_only` mechanically when startup still writes to
site-packages, generated imports, or mounted application paths.

## Secrets

Secrets must not appear in:

- Dockerfile literals
- image `ENV`
- persistent `ARG`/history
- copied `.env` or credential files
- Compose defaults
- command lines visible through process inspection
- health output or logs

Production secret systems may inject environment variables. Review scope,
rotation, redaction, and which services receive each value.

## Health

Use separate semantics:

- **liveness**: the process can serve its basic endpoint or loop
- **readiness**: dependencies and required operations are available
- **startup**: slow initialization has completed

Keep checks bounded and inexpensive. Do not perform destructive operations,
install dependencies, or leak configuration in a health check.

Compose health conditions improve local startup ordering but do not replace
application retry handling or production probes.

## Network and ports

- Use container ports for service-to-service traffic.
- Publish only ports needed from the host.
- Bind local-only tools and automation to `127.0.0.1`.
- Treat `0.0.0.0` host publishing as exposure, even on a developer machine.
- Document external egress and verify effective deployment policy.
- Use separate services/networks when trust, credentials, or policy differ.

## Supply chain

When supported by the actual release platform:

- scan OS and application dependencies
- generate and retain an SBOM
- record provenance and build inputs
- sign promoted images
- enforce registry and deployment admission policy

Report missing enforcement as a gap. Do not add fictional CI commands or claim
compliance from a local scan alone.
