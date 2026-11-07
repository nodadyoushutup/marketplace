<p align="center">
  <img src="docs/assets/github-banner.png" alt="Marketplace" width="100%">
</p>

# Marketplace

Agent plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code),
[Cursor](https://cursor.com),
[GitHub Copilot](https://github.com/features/copilot), and
[OpenAI Codex](https://openai.com/codex).

Each plugin is a self-contained package of rules, skills, agents, and slash
commands. Add this repo as a marketplace, then install only what you use.

## Install

Replace `<short>` with a plugin folder name from the tables below
(for example `code`, `github`, or `vault`).

### Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace
/plugin install nodadyoushutup-<short>@nodadyoushutup-marketplace
/reload-plugins
```

### Cursor

1. Open **Dashboard → Settings → Plugins**
2. Import `https://github.com/nodadyoushutup/marketplace`
3. Install the plugins you want

### GitHub Copilot CLI

```shell
copilot plugin marketplace add nodadyoushutup/marketplace
copilot plugin install nodadyoushutup-<short>@nodadyoushutup-marketplace
```

### OpenAI Codex

```shell
codex plugin marketplace add nodadyoushutup/marketplace
```

## Plugins

Marketplace ids are `nodadyoushutup-<short>`. On disk that maps to
`plugins/<short>/`.

### Core

| Install id | Description |
| --- | --- |
| `nodadyoushutup-global` | Default posture, MCP-first workflow, writing |
| `nodadyoushutup-code` | Language standards, refactor/deslop, coding agents |
| `nodadyoushutup-business-analyst` | Briefs, plans, external research |
| `nodadyoushutup-security` | Secrets, auth, injection, crypto, supply chain |
| `nodadyoushutup-github` | PRs, review checks, Actions workflows |
| `nodadyoushutup-atlassian` | Jira and Confluence |
| `nodadyoushutup-drawio` | Author and repair `.drawio` diagrams |

### Optional

| Install id | Description |
| --- | --- |
| `nodadyoushutup-agentmemory` | AgentMemory recall / capture |
| `nodadyoushutup-browser` | Browser QA |
| `nodadyoushutup-jenkins` | Jenkins builds and pipeline craft |
| `nodadyoushutup-lucidchart` | Lucidchart Standard Import |
| `nodadyoushutup-google-workspace` | Gmail, Drive, Calendar, Docs, Sheets |
| `nodadyoushutup-google-cloud` | GCP projects, Compute, GKE, GCS |
| `nodadyoushutup-freshservice` | Freshservice ITSM |
| `nodadyoushutup-vault` | Vault secrets and PKI |
| `nodadyoushutup-grafana` | Dashboards, Explore, incidents, alerting |
| `nodadyoushutup-cloudflare` | DNS records |
| `nodadyoushutup-compose` | Docker Compose |
| `nodadyoushutup-kubernetes` | Pod, event, and log triage |
| `nodadyoushutup-proxmox` | Proxmox VE inventory and gated VM ops |
| `nodadyoushutup-argocd` | Argo CD apps and gated sync |
| `nodadyoushutup-prometheus` | PromQL discover and query |
| `nodadyoushutup-graylog` | Log search |
| `nodadyoushutup-minio` | MinIO / S3 buckets and objects |
| `nodadyoushutup-velero` | Backup and restore |
| `nodadyoushutup-fortigate` | FortiGate inventory and gated policies |
| `nodadyoushutup-yarr` | *arr, Plex, qBittorrent, Seerr |

Many plugins also expose slash commands named after the short key
(`/code`, `/vault`, `/kubernetes`, …). See each plugin’s `README.md` for
details.

## Layout

| Host | Marketplace catalog | Plugin manifest |
| --- | --- | --- |
| Claude Code | `.claude-plugin/marketplace.json` | `.claude-plugin/plugin.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `.cursor-plugin/plugin.json` |
| GitHub Copilot | `.github/plugin/marketplace.json` | `.claude-plugin/plugin.json` |
| OpenAI Codex | `.agents/plugins/marketplace.json` | `.codex-plugin/plugin.json` |

## Development

Rules for prefixes, manifests, and the craft-plugin quality bar live in
[AGENTS.md](AGENTS.md).

Validate before you commit:

```shell
python3 scripts/validate_marketplace.py
```

CI runs the same check on push and pull request.

Scaffold a gate → act workflow diagram:

```shell
python3 scripts/generate_workflow_drawios.py
```

## License

[MIT](LICENSE)
