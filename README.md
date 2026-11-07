<p align="center">
  <img src="docs/assets/github-banner.png" alt="Marketplace" width="100%">
</p>

Agent plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code),
[Cursor](https://cursor.com),
[GitHub Copilot](https://github.com/features/copilot), and
[OpenAI Codex](https://openai.com/codex).

Each plugin is a bundle of rules, skills, agents, and slash commands that change
how the agent behaves—not just a list of files to open. Add this repo as a
marketplace, then install what you actually need.

## Install

Plugin ids are `nodadyoushutup-<short>`. The marketplace name in install
selectors is `nodadyoushutup-marketplace`. Substitute `<plugin>` with any id
from the tables below.

### Claude Code

In a Claude Code session (slash commands):

```text
/plugin marketplace add nodadyoushutup/marketplace
/plugin install <plugin>@nodadyoushutup-marketplace
```

`/plugin install` opens the plugin panel so you can pick a scope. Closing the
panel applies pending changes.

From your shell (no session required):

```shell
claude plugin marketplace add nodadyoushutup/marketplace
claude plugin install <plugin>@nodadyoushutup-marketplace
```

If a session is already running when you install from the shell, apply the
change with `/reload-plugins`. Use `/reload-plugins --force` if Claude warns
that the reload would invalidate the prompt cache.

### Cursor

1. Open **Dashboard → Settings → Plugins**
2. Import `https://github.com/nodadyoushutup/marketplace`
3. Install plugins from the catalog

### OpenAI Codex

From your shell:

```shell
codex plugin marketplace add nodadyoushutup/marketplace
codex plugin add <plugin>@nodadyoushutup-marketplace
```

Or open `/plugins` in Codex CLI, add the marketplace, and install from there.
Start a new Codex session after install so skills and tools load.

### GitHub Copilot

From your shell:

```shell
copilot plugin marketplace add nodadyoushutup/marketplace
copilot plugin install <plugin>@nodadyoushutup-marketplace
```

In an interactive Copilot CLI session the same steps are
`/plugin marketplace add …` and `/plugin install …`.

### Example: `global`

Install the default-posture plugin (`nodadyoushutup-global`):

| Host | Install |
| --- | --- |
| Claude Code (session) | `/plugin install nodadyoushutup-global@nodadyoushutup-marketplace` |
| Claude Code (shell) | `claude plugin install nodadyoushutup-global@nodadyoushutup-marketplace` |
| Cursor | Pick `nodadyoushutup-global` after importing the marketplace |
| OpenAI Codex | `codex plugin add nodadyoushutup-global@nodadyoushutup-marketplace` |
| GitHub Copilot | `copilot plugin install nodadyoushutup-global@nodadyoushutup-marketplace` |

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
| `nodadyoushutup-kubernetes` | Manifest craft, pods, events, logs |
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
