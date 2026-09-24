# nodadyoushutup-marketplace

Dual marketplace of portable Agent **rules**, **skills**, and **agents** for
**Claude Code** and **Cursor**.

Components live once under `plugins/global/` and are listed from both:

- `.claude-plugin/marketplace.json` — Claude Code (skills + agents)
- `.cursor-plugin/marketplace.json` — Cursor (rules + skills + agents)

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/marketplace
/plugin install global@nodadyoushutup-marketplace
/reload-plugins
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins** (or **Customize → Plugins**).
2. Import from GitHub: `https://github.com/nodadyoushutup/marketplace`
3. Install the **global** plugin.

Team marketplaces can also point at this repo directly.

## What's included

Portable `global-*` craft stolen from framework + homelab (site-specific
assets left behind):

| Kind | Contents |
| --- | --- |
| **Rules** (Cursor) | standing posture, change intensity, language (Python/JS/HTML/YAML), Terraform, Docker local-vs-deployed, CI-from-main, AgentMemory gates, policy evolution |
| **Skills** (both) | standing-orders, action-first, STE, coding workflow, debugging, verification, deslop, refactor (+ Python/JS), Docker, browser automation, worktrees, merge conflicts, skill intake, policy evolution, writing for agents |
| **Agents** (both) | BA, tech-lead, code-reviewer, planner, researcher, debugger, QA |

Claude Code does not load plugin `rules/`; use the `global-standing-orders`
skill for always-on postures. Cursor loads `rules/` as alwaysApply / glob
rules.

See [`plugins/global/README.md`](plugins/global/README.md).

## Repo layout

```text
.claude-plugin/marketplace.json   # Claude Code catalog
.cursor-plugin/marketplace.json   # Cursor catalog
plugins/global/            # Shared plugin
  .claude-plugin/plugin.json
  .cursor-plugin/plugin.json
  rules/global-*.mdc              # Cursor rules
  skills/global-*/SKILL.md
  agents/global-*.md
```

## License

MIT — see [LICENSE](LICENSE). Some individual skills retain upstream MIT
attribution in their `ORIGIN.md` / `LICENSE` files.
