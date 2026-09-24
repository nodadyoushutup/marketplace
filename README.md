# nodadyoushutup-marketplace

Dual marketplace of portable Agent **rules**, **skills**, and **agents** for
**Claude Code** and **Cursor**.

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace
/plugin install nodadyoushutup-global@nodadyoushutup-marketplace
/plugin install nodadyoushutup-code@nodadyoushutup-marketplace
# optional:
/plugin install nodadyoushutup-agentmemory@nodadyoushutup-marketplace
/plugin install nodadyoushutup-docker@nodadyoushutup-marketplace
/plugin install nodadyoushutup-browser@nodadyoushutup-marketplace
/reload-plugins
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins**.
2. Import: `https://github.com/nodadyoushutup/marketplace`
3. Install **nodadyoushutup-global** + **nodadyoushutup-code**, plus optional plugins as needed.

## Plugins

Marketplace `name` is `nodadyoushutup-<short>`; folders and asset prefixes stay short (`code-*`, `global-*`, …).

| Marketplace id | Folder | What it is |
| --- | --- | --- |
| **nodadyoushutup-global** | `plugins/global/` | Standing posture, planning agents, writing/policy craft |
| **nodadyoushutup-code** | `plugins/code/` | Language standards, coding workflow, worktrees/merge/CI craft, coding agents |
| **nodadyoushutup-agentmemory** | `plugins/agentmemory/` | Gated AgentMemory MCP capture/recall |
| **nodadyoushutup-docker** | `plugins/docker/` | Local-vs-deployed compose + Docker ops skill |
| **nodadyoushutup-browser** | `plugins/browser/` | Browser QA (Playwright → IDE → CLI) |
| **nodadyoushutup-drawio** | `plugins/drawio/` | `.drawio` author/repair (clean layout) + editor false-alarm triage |

Plugins may also ship **commands** under `plugins/<short>/commands/` (`/deslop`, `/refactor`, `code-review`, …).

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Asset basenames must use the owning plugin’s prefix. See [AGENTS.md](AGENTS.md).
