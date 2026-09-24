# nodadyoushutup-marketplace

Dual marketplace of portable Agent **rules**, **skills**, and **agents** for
**Claude Code** and **Cursor**.

Plugins live under `plugins/` and are listed from both:

- `.claude-plugin/marketplace.json` — Claude Code
- `.cursor-plugin/marketplace.json` — Cursor

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace
/plugin install global@nodadyoushutup-marketplace
# optional stacks:
/plugin install agentmemory@nodadyoushutup-marketplace
/plugin install docker@nodadyoushutup-marketplace
/plugin install terraform@nodadyoushutup-marketplace
/plugin install browser@nodadyoushutup-marketplace
/plugin install git@nodadyoushutup-marketplace
/reload-plugins
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins** (or **Customize → Plugins**).
2. Import from GitHub: `https://github.com/nodadyoushutup/marketplace`
3. Install **global**, plus any optional plugins you need.

## Plugins

| Plugin | What it is |
| --- | --- |
| **global** | Core posture, languages, coding workflow, writing, agents |
| **agentmemory** | Gated AgentMemory MCP capture/recall |
| **docker** | Local-vs-deployed compose + Docker ops skill |
| **terraform** | Terraform HCL + validation rules |
| **browser** | Browser QA (Playwright MCP → IDE → CLI) |
| **git** | Worktrees, merge conflicts, CI-from-main |
| **drawio** | Cursor `.drawio` editor false-alarm triage |

## Repo layout

```text
.claude-plugin/marketplace.json
.cursor-plugin/marketplace.json
plugins/
  global/
  agentmemory/
  docker/
  terraform/
  browser/
  git/
  drawio/
```

## License

MIT — see [LICENSE](LICENSE). Some individual skills retain upstream MIT
attribution in their `ORIGIN.md` / `LICENSE` files.
