# nodadyoushutup-marketplace-public

Public dual marketplace of portable Agent **rules**, **skills**, and **agents**
for **Claude Code** and **Cursor**.

Homelab **framework** and **homelab** infra craft live in the private sibling
[`marketplace-private`](https://github.com/nodadyoushutup/marketplace-private).

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace-public
/plugin install nodadyoushutup-global@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-code@nodadyoushutup-marketplace-public
# optional:
/plugin install nodadyoushutup-business-analyst@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-agentmemory@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-atlassian@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-github@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-jenkins@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-browser@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-drawio@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-lucidchart@nodadyoushutup-marketplace-public
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
   plugins (`business-analyst`, …) as needed.
4. For framework/homelab: also import
   `https://github.com/nodadyoushutup/marketplace-private` and install
   **nodadyoushutup-framework** and/or **nodadyoushutup-homelab**.

## Plugins

Marketplace `name` is `nodadyoushutup-<short>`; folders and asset prefixes stay
short (`code-*`, `global-*`, …).

| Marketplace id | Folder | What it is |
| --- | --- | --- |
| **nodadyoushutup-global** | `plugins/global/` | Standing posture, writing/policy craft |
| **nodadyoushutup-code** | `plugins/code/` | Language standards (incl. YAML/K8s), coding workflow, worktrees/merge craft, coding agents |
| **nodadyoushutup-business-analyst** | `plugins/business-analyst/` | Business analysis, planner, external researcher |
| **nodadyoushutup-agentmemory** | `plugins/agentmemory/` | Gated AgentMemory recall/capture (+ on-demand ops) |
| **nodadyoushutup-atlassian** | `plugins/atlassian/` | Unified Jira + Confluence craft (create gates, issue types, pages, draw.io attach) |
| **nodadyoushutup-github** | `plugins/github/` | Agnostic GitHub PR checks/comments + Actions CI craft |
| **nodadyoushutup-jenkins** | `plugins/jenkins/` | Agnostic Jenkins builds + pipeline CI craft |
| **nodadyoushutup-browser** | `plugins/browser/` | Browser QA (Playwright → IDE → CLI) |
| **nodadyoushutup-drawio** | `plugins/drawio/` | `.drawio` author/repair (clean layout) + editor false-alarm triage |
| **nodadyoushutup-lucidchart** | `plugins/lucidchart/` | Lucidchart Standard Import author/repair + `.lucid` packaging |

Plugins may also ship **commands** under `plugins/<short>/commands/` (`/deslop`,
`/refactor`, `/business-analyst`, `/atlassian`, `/jira`, `/confluence`,
`/github`, `/jenkins`, `code-review`, `lucidchart-author`, …).

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Asset basenames must use the owning plugin’s prefix. See [AGENTS.md](AGENTS.md).
