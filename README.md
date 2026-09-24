# nodadyoushutup-marketplace

Dual marketplace of portable Agent **rules**, **skills**, and **agents** for
**Claude Code** and **Cursor**.

Components live once under `plugins/global-skills/` and are listed from both:

- `.claude-plugin/marketplace.json` — Claude Code (skills + agents)
- `.cursor-plugin/marketplace.json` — Cursor (rules + skills + agents)

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/market
/plugin install global-skills@nodadyoushutup-marketplace
/reload-plugins
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins** (or **Customize → Plugins**).
2. Import from GitHub: `https://github.com/nodadyoushutup/market`
3. Install the **global-skills** plugin.

Team marketplaces can also point at this repo directly.

## What's included

The `global-skills` plugin ships the portable `global-*` pack from the
framework repo (framework-specific assets stay behind):

| Kind | Contents |
| --- | --- |
| **Rules** (Cursor) | execute-first, MCP-first, host URLs, comments, commits, AgentMemory gates, drawio triage, policy evolution |
| **Skills** (both) | standing-orders, action-first, STE rewrite, coding workflow, debugging, verification, deslop, refactor (+ Python/JS), Docker, browser automation, worktrees, merge conflicts, skill intake, policy evolution, writing for agents |
| **Agents** (both) | business-analyst, technical-lead, code-reviewer |

Claude Code does not load plugin `rules/`; use the `global-standing-orders`
skill for the same always-on postures. Cursor loads `rules/` as alwaysApply /
glob rules.

See [`plugins/global-skills/README.md`](plugins/global-skills/README.md).

## Repo layout

```text
.claude-plugin/marketplace.json   # Claude Code catalog
.cursor-plugin/marketplace.json   # Cursor catalog
plugins/global-skills/            # Shared plugin
  .claude-plugin/plugin.json
  .cursor-plugin/plugin.json
  rules/global-*.mdc              # Cursor rules
  skills/global-*/SKILL.md
  agents/global-*.md
```

## License

MIT — see [LICENSE](LICENSE). Some individual skills retain upstream MIT
attribution in their `ORIGIN.md` / `LICENSE` files.
