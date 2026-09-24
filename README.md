# nodadyoushutup-marketplace-public

Public dual marketplace of portable Agent **rules**, **skills**, and **agents**
for **Claude Code** and **Cursor**.

Homelab **framework** craft lives in the private sibling
[`marketplace-private`](https://github.com/nodadyoushutup/marketplace-private).

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace-public
/plugin install nodadyoushutup-global@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-code@nodadyoushutup-marketplace-public
# optional:
/plugin install nodadyoushutup-business-analyst@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-agentmemory@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-jira@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-browser@nodadyoushutup-marketplace-public
/plugin install nodadyoushutup-drawio@nodadyoushutup-marketplace-public
/reload-plugins
```

Framework (private marketplace):

```shell
/plugin marketplace add nodadyoushutup/marketplace-private
/plugin install nodadyoushutup-framework@nodadyoushutup-marketplace-private
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins**.
2. Import: `https://github.com/nodadyoushutup/marketplace-public`
3. Install **nodadyoushutup-global** + **nodadyoushutup-code**, plus optional
   plugins (`business-analyst`, …) as needed.
4. For framework: also import
   `https://github.com/nodadyoushutup/marketplace-private` and install
   **nodadyoushutup-framework**.

## Plugins

Marketplace `name` is `nodadyoushutup-<short>`; folders and asset prefixes stay
short (`code-*`, `global-*`, …).

| Marketplace id | Folder | What it is |
| --- | --- | --- |
| **nodadyoushutup-global** | `plugins/global/` | Standing posture, writing/policy craft |
| **nodadyoushutup-code** | `plugins/code/` | Language standards, coding workflow, worktrees/merge/CI craft, coding agents |
| **nodadyoushutup-business-analyst** | `plugins/business-analyst/` | Business analysis, planner, external researcher |
| **nodadyoushutup-agentmemory** | `plugins/agentmemory/` | Gated AgentMemory recall/capture (+ on-demand ops) |
| **nodadyoushutup-jira** | `plugins/jira/` | Agnostic Jira create + Story/Bug/Task/Epic/Sub-task craft |
| **nodadyoushutup-browser** | `plugins/browser/` | Browser QA (Playwright → IDE → CLI) |
| **nodadyoushutup-drawio** | `plugins/drawio/` | `.drawio` author/repair (clean layout) + editor false-alarm triage |

Plugins may also ship **commands** under `plugins/<short>/commands/` (`/deslop`,
`/refactor`, `/business-analyst`, `/jira`, `code-review`, …).

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Asset basenames must use the owning plugin’s prefix. See [AGENTS.md](AGENTS.md).
