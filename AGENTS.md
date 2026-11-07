# AGENTS.md — marketplace

Public Claude Code / Cursor / GitHub Copilot / OpenAI Codex plugin marketplace.
Root catalogs:

- `.cursor-plugin/marketplace.json`
- `.claude-plugin/marketplace.json`
- `.github/plugin/marketplace.json` (Copilot)
- `.agents/plugins/marketplace.json` (Codex)

Plugins live under `plugins/<short>/` (for example `plugins/jenkins/`).

Marketplace / `plugin.json` **`name`** is `nodadyoushutup-<short>` (for example
`nodadyoushutup-jenkins`). Claude/Cursor catalog `source` stays the short folder
name; Copilot/Codex catalogs use `./plugins/<short>`.

## Out of scope (permanent)

These plugins are **not** maintained in this public marketplace:

| Short key | Lives in |
| --- | --- |
| `homelab` / `homelab-*` | [`marketplace-private`](https://github.com/nodadyoushutup/marketplace-private) (site overlays) |
| `archentic` / framework agent policy | [`archentic/marketplace`](https://github.com/archentic/marketplace) |

Do not add `plugins/homelab/` or `plugins/archentic/` here.

## Plugin inventory

**Tier:** `core` = useful in most workspaces. `domain` = install when that
surface is in play (MCP/ops craft).

Asset basenames use the **short** plugin key (folder stem), not the full
marketplace id: exact short name, or `short-*`. Commands follow the same rule,
plus the short slash aliases listed under Allowed basenames.

| Short key | Marketplace id | Allowed basenames | Owns | Tier |
| --- | --- | --- | --- | --- |
| `global` | `nodadyoushutup-global` | `global` or `global-*` | Standing posture, host URLs, MCP-first, writing, and policy sync | core |
| `code` | `nodadyoushutup-code` | `code` or `code-*`; commands also `deslop`, `refactor` | Language standards, workflow, and coding agents | core |
| `business-analyst` | `nodadyoushutup-business-analyst` | `business-analyst` or `business-analyst-*` | Briefs, plans, and external research | core |
| `security` | `nodadyoushutup-security` | `security` or `security-*` | Secrets, auth, injection, crypto, transport, supply chain, and data exposure | core |
| `git` | `nodadyoushutup-git` | `git` or `git-*` | Worktrees, merge conflicts, Conventional Commits, and safe local git | core |
| `github` | `nodadyoushutup-github` | `github` or `github-*` | Pull request checks, comments, titles, and Actions workflow craft | core |
| `atlassian` | `nodadyoushutup-atlassian` | `atlassian` or `atlassian-*`; commands also `jira`, `confluence` | Jira and Confluence create gates and page/issue shape | domain |
| `drawio` | `nodadyoushutup-drawio` | `drawio` or `drawio-*` | `.drawio` author and repair | domain |
| `agentmemory` | `nodadyoushutup-agentmemory` | `agentmemory` or `agentmemory-*` | AgentMemory MCP recall/capture + on-demand ops | domain |
| `jenkins` | `nodadyoushutup-jenkins` | `jenkins` or `jenkins-*` | Agnostic Jenkins builds + pipeline CI craft | domain |
| `lucidchart` | `nodadyoushutup-lucidchart` | `lucidchart` or `lucidchart-*` | Lucidchart Standard Import author/repair + `.lucid` packaging | domain |
| `google-workspace` | `nodadyoushutup-google-workspace` | `google-workspace` or `google-workspace-*` | Gmail + Drive + Calendar + Docs/Sheets | domain |
| `google-cloud` | `nodadyoushutup-google-cloud` | `google-cloud` or `google-cloud-*` | GCP projects + Compute/GKE + GCS with safety gates | domain |
| `freshservice` | `nodadyoushutup-freshservice` | `freshservice` or `freshservice-*` | Freshservice ITSM create gates + ticket shape | domain |
| `vault` | `nodadyoushutup-vault` | `vault` or `vault-*` | Vault secrets/PKI + leak refuse | domain |
| `grafana` | `nodadyoushutup-grafana` | `grafana` or `grafana-*` | Dashboards, Explore, incidents, alerting | domain |
| `cloudflare` | `nodadyoushutup-cloudflare` | `cloudflare` or `cloudflare-*` | DNS record craft with destructive gates | domain |
| `compose` | `nodadyoushutup-compose` | `compose` or `compose-*` | Docker Compose layout/ops with destructive gates | domain |
| `kubernetes` | `nodadyoushutup-kubernetes` | `kubernetes` or `kubernetes-*` | Portable manifest craft + pod/event/log triage (site overlays stay in private `homelab`) | domain |
| `proxmox` | `nodadyoushutup-proxmox` | `proxmox` or `proxmox-*` | Proxmox VE inventory + gated VM/LXC ops | domain |
| `argocd` | `nodadyoushutup-argocd` | `argocd` or `argocd-*` | Argo CD app status + gated sync | domain |
| `prometheus` | `nodadyoushutup-prometheus` | `prometheus` or `prometheus-*` | PromQL discover/query via MCP | domain |
| `victoriametrics` | `nodadyoushutup-victoriametrics` | `victoriametrics` or `victoriametrics-*` | MetricsQL/PromQL discover/query via VictoriaMetrics MCP | domain |
| `graylog` | `nodadyoushutup-graylog` | `graylog` or `graylog-*` | Log search via MCP with redaction | domain |
| `minio` | `nodadyoushutup-minio` | `minio` or `minio-*` | MinIO/S3 buckets/objects with delete gates | domain |
| `velero` | `nodadyoushutup-velero` | `velero` or `velero-*` | Velero backup/restore inventory + gated mutate | domain |
| `fortigate` | `nodadyoushutup-fortigate` | `fortigate` or `fortigate-*` | FortiGate inventory + gated policy changes | domain |
| `yarr` | `nodadyoushutup-yarr` | `yarr` or `yarr-*` | *arr / Plex / qBit / Seerr fleet via yarr MCP | domain |
| `runpod` | `nodadyoushutup-runpod` | `runpod` or `runpod-*` | RunPod GPU cloud inventory + gated mutate | domain |
| `uptime-kuma` | `nodadyoushutup-uptime-kuma` | `uptime-kuma` or `uptime-kuma-*` | Uptime Kuma monitors, status pages, and notification channels with gated delete/pause | domain |
| `nginx-proxy-manager` | `nodadyoushutup-nginx-proxy-manager` | `nginx-proxy-manager` or `nginx-proxy-manager-*` | Nginx Proxy Manager hosts, SSL, and access lists with destructive gates | domain |
| `vaultwarden` | `nodadyoushutup-vaultwarden` | `vaultwarden` or `vaultwarden-*` | Vaultwarden admin/ops posture; refuse vault/credential dumps | domain |
| `kopia` | `nodadyoushutup-kopia` | `kopia` or `kopia-*` | Kopia repository/snapshot inventory + gated snapshot/restore/forget | domain |
| `authentik` | `nodadyoushutup-authentik` | `authentik` or `authentik-*` | Authentik IdP apps/providers/flows with destructive gates | domain |
| `traefik` | `nodadyoushutup-traefik` | `traefik` or `traefik-*` | Traefik routers/middlewares/IngressRoute with destructive gates | domain |
| `tailscale` | `nodadyoushutup-tailscale` | `tailscale` or `tailscale-*` | Tailscale devices/ACLs with gated policy and key changes | domain |
| `home-assistant` | `nodadyoushutup-home-assistant` | `home-assistant` or `home-assistant-*` | Home Assistant entities/service calls with destructive gates | domain |
| `immich` | `nodadyoushutup-immich` | `immich` or `immich-*` | Immich library/album/asset inventory with gated delete/share | domain |
| `obsidian` | `nodadyoushutup-obsidian` | `obsidian` or `obsidian-*` | Obsidian vault note inventory/authoring with gated delete/move | domain |
| `portainer` | `nodadyoushutup-portainer` | `portainer` or `portainer-*` | Portainer endpoints/stacks/containers with gated mutate | domain |
| `zot` | `nodadyoushutup-zot` | `zot` or `zot-*` | Zot OCI registry inventory + gated delete/GC | domain |
| `harbor` | `nodadyoushutup-harbor` | `harbor` or `harbor-*` | Harbor projects/artifacts + gated delete/retention/robot | domain |

### Examples

- Rule: `plugins/jenkins/rules/jenkins-ci-from-main.mdc`
- Primary skill: `plugins/jenkins/skills/jenkins/SKILL.md` → `name: jenkins`
- Compound skill: `plugins/code/skills/code-verification-before-completion/SKILL.md` → `name: code-verification-before-completion`
- Plugin command: `plugins/vault/commands/vault.md` → `/vault`
- Alias commands: `plugins/code/commands/deslop.md` → `/deslop`; `plugins/atlassian/commands/jira.md` → `/jira`
- Agent: `plugins/code/agents/code-technical-lead.md` → `name: code-technical-lead`

### Slash command names

Skills, rules, and agents stay plugin-prefixed (`jenkins-ci-from-main`,
`vault-secrets`, `code-technical-lead`). Plugin-named **commands** use the short
key as frontmatter `name:` and filename (`jenkins` → `/jenkins`), live under the
owning plugin, and invoke that plugin's skill. Short aliases (`deslop`,
`refactor`, `jira`, `confluence`) are the only basenames allowed without the
plugin prefix — keep them in sync with `SHORT_COMMANDS` in
`scripts/validate_marketplace.py`.

### Hard requirements

1. **Directory / file stem matches frontmatter `name:`** for skills, agents, and
   commands.
2. **Do not leave another plugin's prefixed assets inside a plugin** (no
   `global-*` files under `plugins/code/`, and no `code-*` files under
   `plugins/global/`).
3. **Do not invent a second prefix** inside a plugin (no `jenkins-global-*`, no
   bare `builds.mdc` under `plugins/jenkins/rules/`).
4. When moving an asset **within** a plugin (or renaming it), update all
   **intra-plugin** cross-references and the catalog/inventory rows in the same
   change. Do not add pointers into other plugins.
5. **Plugins are self-contained.** Skills, rules, commands, agents, and workflow
   diagrams must not cite another plugin’s asset names (`global-mcp-first`,
   `code-yaml`, `code-technical-lead`, …). Do not tell the agent to load, follow,
   pair with, or hand off to another marketplace plugin. Inline the floor you
   need, or mark the surface **out of scope** with a local sentence. Standing
   posture that lives in `global` (for example MCP-first) applies when that
   plugin is installed via its own always-on rules — other plugins must not
   cite those rule names.
6. **Vendor lock-in is the plugin name only.** Inside a plugin body, prefer
   generic capability language (`LoadBalancer`, ingress controller, secret
   store, issue tracker, reverse proxy, metrics backend). Own-product names
   stay. Do not assume a sibling product (MetalLB, a specific Ingress
   controller, Vault as the only secret backend, …) as the default path.

## Plugin quality bar

Enforced by `python3 scripts/validate_marketplace.py` unless noted.

**Every plugin** under `plugins/` must ship:

1. **`README.md`** listing rules, skills, commands, agents (if any), and the
   workflow diagram when present.
2. **≥1 skill** at `skills/*/SKILL.md`.
3. **Manifests:** `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json`,
   `.codex-plugin/plugin.json`, and matching entries in all four root catalogs.

**Workflow diagram** (`docs/<short>-workflow.drawio`, or
`<short>-*-workflow.drawio` for multi-surface plugins): required for every
plugin except `global` (standing posture only; see `WORKFLOW_EXEMPT` in the
validator).

**Primary skill shape** (convention; not fully linted by the validator):

- **Gated domain craft** (MCP/ops with a gate → act → end path): Gate + Load map
  + Defaults. Skip the skill body when the gate says the turn is unauthorized
  for that surface.
- **Posture / authoring** (`global`, `code`, `drawio`, `lucidchart`): their own
  shapes (standing orders, tier workflow, When to use + Procedure).
- **`agentmemory`:** Gate + Scope + Session defaults (recall/capture always-on
  lean path; ops on demand).

## Adding a plugin

1. Create `plugins/<short>/` with manifests, README, ≥1 skill, and workflow
   drawio (unless `global`).
2. Add the plugin to all four root marketplace catalogs.
3. Add a row to the inventory table above (basenames, owns, tier).
4. Run `python3 scripts/validate_marketplace.py`.

## Commits

Use Conventional Commits (`git-commit-messages` in the `git` plugin).

**Repo policy (this marketplace):** after every change, commit and push to
`origin` on the current branch. Do not wait to be asked. This overrides
ask-first personal commit defaults while working in this repo. Skip only when
the operator explicitly says not to commit or push.

## Version bumps (required for client upgrades)

Harnesses that install from this GitHub marketplace (Claude Code, Copilot,
Codex; Cursor when it re-resolves) treat the plugin **`version`** string as the
update key. An unchanged version means `plugin update` / marketplace refresh
reports “already latest” and leaves the cached install on the old commit even
though `main` moved.

**Before every commit that changes shipped plugin content** under
`plugins/<short>/` (rules, skills, commands, agents, manifests, workflow
diagrams, or plugin README that installers read):

1. Bump that plugin’s semver in **all three** host manifests
   (`.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json`,
   `.codex-plugin/plugin.json`) **and** the matching entry in **all four** root
   catalogs.
2. Default level is **patch** (`0.10.0` → `0.10.1`). Use **minor** when adding
   a user-visible surface (new skill/rule/command/agent) or changing ownership
   contracts; **major** only for install-id / breaking renames.
3. Prefer the one refresh script (auto-bumps plugins that still need it,
   then updates harness marketplaces + installed plugins):

```shell
python3 scripts/refresh_marketplaces.py
# Cursor personal pin stuck? add --force
# Explicit named / non-patch bump only:
#   python3 scripts/bump_plugin_versions.py security --level minor
```

4. Skip the bump only for pure repo chrome that does not change any
   `plugins/<short>/` install payload (for example root `README.md` copy alone,
   or `scripts/` / `AGENTS.md` with no plugin file edits). New plugins start at
   `0.1.0` (or the next free line) and still need catalog rows in sync.
5. After push, re-run `python3 scripts/refresh_marketplaces.py` so clients
   pick up the new versions (Cursor may still need `--force` when a personal
   import is pinned to the first-import commit).

`python3 scripts/validate_marketplace.py` fails when the three manifests or any
catalog entry disagree on version for a plugin.

## Validation checklist (before commit)

- [ ] New/renamed skills/rules/agents/commands use the owning plugin’s prefix
      (or an allowed short alias)
- [ ] Skill/agent/command `name:` frontmatter matches the directory or file stem
- [ ] Inventory table + all four marketplace JSON files list the plugin (if new)
- [ ] Quality bar met (README + skill + manifests; workflow drawio unless exempt)
- [ ] Touched plugins had a version bump (manifests + all four catalogs) when
      shipped content changed — `python3 scripts/refresh_marketplaces.py`
      auto-bumps, or bump explicitly for minor/major
- [ ] `python3 scripts/validate_marketplace.py` passes
- [ ] READMEs for touched plugins list the new names
- [ ] No references to old unprefixed or wrong-plugin names remain
- [ ] No cross-plugin asset citations in skills/rules/commands/agents/diagrams
- [ ] Vendor language inside plugins stays capability-generic (lock-in at plugin name)
- [ ] Homelab / archentic private assets are not introduced under this public
      marketplace
