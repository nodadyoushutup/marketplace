# nodadyoushutup-marketplace-public

Public marketplace of portable Agent **rules**, **skills**, and **agents** for
**Claude Code**, **Cursor**, **GitHub Copilot**, and **OpenAI Codex**.

Homelab **framework** and **homelab** infra craft live in the private sibling
[`marketplace-private`](https://github.com/nodadyoushutup/marketplace-private).

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace-public
/plugin install nodadyoushutup-global@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-code@nodadyoushutup-marketplace-public
# optional plugins use the same @nodadyoushutup-marketplace-public form
/reload-plugins
```

Private marketplace (framework + homelab):

```shell
/plugin marketplace add nodadyoushutup/marketplace-private
/plugin install nodadyoushutup-framework@nodadyoushutup-marketplace-private
/plugin install nodadyoushutup-homelab@nodadyoushutup-marketplace-private
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins**.
2. Import: `https://github.com/nodadyoushutup/marketplace-public`
3. Install **nodadyoushutup-global** + **nodadyoushutup-code**, plus optional
   plugins as needed.
4. For framework/homelab: also import
   `https://github.com/nodadyoushutup/marketplace-private`.

## Install — GitHub Copilot CLI

```shell
copilot plugin marketplace add nodadyoushutup/marketplace-public
copilot plugin install nodadyoushutup-global@nodadyoushutup-marketplace-public
copilot plugin install nodadyoushutup-code@nodadyoushutup-marketplace-public
# optional plugins use the same @nodadyoushutup-marketplace-public form
```

## Install — OpenAI Codex

```shell
codex plugin marketplace add nodadyoushutup/marketplace-public
```

## Plugins

Marketplace `name` is `nodadyoushutup-<short>`; folders and asset prefixes stay
short (`code-*`, `global-*`, …).

| Marketplace id | Folder | What it is |
| --- | --- | --- |
| **nodadyoushutup-global** | `plugins/global/` | Standing posture, writing/policy craft |
| **nodadyoushutup-code** | `plugins/code/` | Language standards (incl. YAML/K8s), coding workflow, worktrees/merge craft, coding agents |
| **nodadyoushutup-business-analyst** | `plugins/business-analyst/` | Business analysis, planner, external researcher |
| **nodadyoushutup-agentmemory** | `plugins/agentmemory/` | Gated AgentMemory recall/capture (+ on-demand ops) |
| **nodadyoushutup-atlassian** | `plugins/atlassian/` | Unified Jira + Confluence craft |
| **nodadyoushutup-github** | `plugins/github/` | Agnostic GitHub PR checks/comments + Actions CI craft |
| **nodadyoushutup-jenkins** | `plugins/jenkins/` | Agnostic Jenkins builds + pipeline CI craft |
| **nodadyoushutup-browser** | `plugins/browser/` | Browser QA (IDE browser → CLI) |
| **nodadyoushutup-drawio** | `plugins/drawio/` | `.drawio` author/repair + editor triage |
| **nodadyoushutup-lucidchart** | `plugins/lucidchart/` | Lucidchart Standard Import author/repair |
| **nodadyoushutup-google** | `plugins/google/` | Gmail + Drive + Calendar + Docs/Sheets |
| **nodadyoushutup-freshservice** | `plugins/freshservice/` | Freshservice ITSM create gates + ticket shape |
| **nodadyoushutup-vault** | `plugins/vault/` | Vault secrets/PKI + leak refuse |
| **nodadyoushutup-grafana** | `plugins/grafana/` | Dashboards, Explore, incidents, alerting |
| **nodadyoushutup-cloudflare** | `plugins/cloudflare/` | DNS record craft with destructive gates |
| **nodadyoushutup-kubernetes** | `plugins/kubernetes/` | Agnostic pod/event/log triage |

Plugins may also ship **commands** under `plugins/<short>/commands/` (`/deslop`,
`/refactor`, `/business-analyst`, `/atlassian`, `/jira`, `/confluence`,
`/github`, `/jenkins`, `/google`, `/freshservice`, `/vault`, `/grafana`,
`/cloudflare`, `/kubernetes`, …).

## Catalog paths

| Host | Marketplace catalog | Per-plugin manifest |
| --- | --- | --- |
| Claude Code | `.claude-plugin/marketplace.json` | `.claude-plugin/plugin.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `.cursor-plugin/plugin.json` |
| GitHub Copilot | `.github/plugin/marketplace.json` | `.claude-plugin/plugin.json` (Copilot also accepts this path) |
| OpenAI Codex | `.agents/plugins/marketplace.json` | `.codex-plugin/plugin.json` |

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Asset basenames must use the owning plugin’s prefix. See [AGENTS.md](AGENTS.md).
