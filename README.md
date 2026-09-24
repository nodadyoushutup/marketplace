# nodadyoushutup-marketplace

Dual marketplace of portable Agent **rules**, **skills**, and **agents** for
**Claude Code** and **Cursor**.

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace
/plugin install nodadyoushutup-global@nodadyoushutup-marketplace
/plugin install nodadyoushutup-code@nodadyoushutup-marketplace
# optional:
/plugin install nodadyoushutup-business-analyst@nodadyoushutup-marketplace
/plugin install nodadyoushutup-agentmemory@nodadyoushutup-marketplace
/plugin install nodadyoushutup-jira@nodadyoushutup-marketplace
/plugin install nodadyoushutup-framework@nodadyoushutup-marketplace
/plugin install nodadyoushutup-browser@nodadyoushutup-marketplace
/reload-plugins
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins**.
2. Import: `https://github.com/nodadyoushutup/marketplace`
3. Install **nodadyoushutup-global** + **nodadyoushutup-code**, plus optional plugins (`business-analyst`, …) as needed.

## Plugins

Marketplace `name` is `nodadyoushutup-<short>`; folders and asset prefixes stay short (`code-*`, `global-*`, …).

| Marketplace id | Folder | What it is |
| --- | --- | --- |
| **nodadyoushutup-global** | `plugins/global/` | Standing posture, writing/policy craft |
| **nodadyoushutup-code** | `plugins/code/` | Language standards, coding workflow, worktrees/merge/CI craft, coding agents |
| **nodadyoushutup-business-analyst** | `plugins/business-analyst/` | Business analysis, planner, external researcher |
| **nodadyoushutup-agentmemory** | `plugins/agentmemory/` | Gated AgentMemory recall/capture (+ on-demand ops) |
| **nodadyoushutup-jira** | `plugins/jira/` | Agnostic Jira create + Story/Bug/Task/Epic/Sub-task craft |
| **nodadyoushutup-framework** | `plugins/framework/` | Homelab framework monorepo craft + workflow hooks |
| **nodadyoushutup-browser** | `plugins/browser/` | Browser QA (Playwright → IDE → CLI) |
| **nodadyoushutup-drawio** | `plugins/drawio/` | `.drawio` author/repair (clean layout) + editor false-alarm triage |

Plugins may also ship **commands** under `plugins/<short>/commands/` (`/deslop`, `/refactor`, `/business-analyst`, `/jira`, `/framework`, `code-review`, …).

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Asset basenames must use the owning plugin’s prefix. See [AGENTS.md](AGENTS.md).
