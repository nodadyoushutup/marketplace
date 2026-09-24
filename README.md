# nodadyoushutup-marketplace

Dual marketplace of portable Agent **rules**, **skills**, and **agents** for
**Claude Code** and **Cursor**.

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace
/plugin install global@nodadyoushutup-marketplace
/plugin install code@nodadyoushutup-marketplace
# optional:
/plugin install agentmemory@nodadyoushutup-marketplace
/plugin install docker@nodadyoushutup-marketplace
/plugin install browser@nodadyoushutup-marketplace
/plugin install git@nodadyoushutup-marketplace
/reload-plugins
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins**.
2. Import: `https://github.com/nodadyoushutup/marketplace`
3. Install **global** + **code**, plus optional plugins as needed.

## Plugins

| Plugin | What it is |
| --- | --- |
| **global** | Standing posture, planning agents, writing/policy craft |
| **code** | Language standards (Python/JS/HTML/YAML/Markdown/Terraform), coding workflow, coding agents |
| **agentmemory** | Gated AgentMemory MCP capture/recall |
| **docker** | Local-vs-deployed compose + Docker ops skill |
| **browser** | Browser QA (Playwright → IDE → CLI) |
| **git** | Worktrees, merge conflicts, CI-from-main |
| **drawio** | Cursor `.drawio` editor false-alarm triage |

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Asset basenames must use the owning plugin’s prefix. See [AGENTS.md](AGENTS.md).
