<p align="center">
  <img src="docs/assets/github-banner.png" alt="Marketplace" width="100%">
</p>

# Marketplace

Agent plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code),
[Cursor](https://cursor.com),
[GitHub Copilot](https://github.com/features/copilot), and
[OpenAI Codex](https://openai.com/codex).

Each plugin is a bundle of rules, skills, agents, and slash commands that change
how the agent behaves—not just a list of files to open. Add this repo as a
marketplace, then install what you actually need.

## Install

Examples below install `global` (`nodadyoushutup-global`). Swap the short name
for any plugin in the tables.

### Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace
/plugin install nodadyoushutup-global@nodadyoushutup-marketplace
/reload-plugins
```

### Cursor

1. Open **Dashboard → Settings → Plugins**
2. Import `https://github.com/nodadyoushutup/marketplace`
3. Install `nodadyoushutup-global` (or whatever else you want)

### GitHub Copilot CLI

```shell
copilot plugin marketplace add nodadyoushutup/marketplace
copilot plugin install nodadyoushutup-global@nodadyoushutup-marketplace
```

### OpenAI Codex

```shell
codex plugin marketplace add nodadyoushutup/marketplace
```

Then install `nodadyoushutup-global` from the marketplace UI or CLI for your
Codex build.

## Plugins

Marketplace ids are `nodadyoushutup-<short>`. On disk that is `plugins/<short>/`.

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
(`/global`, `/vault`, `/kubernetes`, …). See each plugin’s `README.md` for
details.

## License

[MIT](LICENSE)
