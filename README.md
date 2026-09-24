# nodadyoushutup-market

Dual marketplace of portable Agent Skills for **Claude Code** and **Cursor**.

Skills live once under `plugins/global-skills/skills/` and are listed from both:

- `.claude-plugin/marketplace.json` — Claude Code
- `.cursor-plugin/marketplace.json` — Cursor

## Install — Claude Code

```shell
/plugin marketplace add nodadyoushutup/market
/plugin install global-skills@nodadyoushutup-market
/reload-plugins
```

## Install — Cursor

1. Open **Dashboard → Settings → Plugins** (or **Customize → Plugins**).
2. Import from GitHub: `https://github.com/nodadyoushutup/market`
3. Install the **global-skills** plugin.

Team marketplaces can also point at this repo directly.

## What's included

The `global-skills` plugin ships the portable `global-*` skill pack:

action-first replies, STE rewrite, coding workflow, systematic debugging,
verification-before-completion, deslop, refactor (incl. Python/JS), Docker,
browser automation, git worktrees, merge conflicts, skill intake, policy
evolution, and writing for agents.

See [`plugins/global-skills/README.md`](plugins/global-skills/README.md).

## Repo layout

```text
.claude-plugin/marketplace.json   # Claude Code catalog
.cursor-plugin/marketplace.json   # Cursor catalog
plugins/global-skills/            # Shared plugin
  .claude-plugin/plugin.json
  .cursor-plugin/plugin.json
  skills/global-*/SKILL.md
```

## License

MIT — see [LICENSE](LICENSE). Some individual skills retain upstream MIT
attribution in their `ORIGIN.md` / `LICENSE` files.
