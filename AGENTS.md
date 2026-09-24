# AGENTS.md — marketplace

Dual Claude Code / Cursor plugin marketplace. Root catalogs:

- `.cursor-plugin/marketplace.json`
- `.claude-plugin/marketplace.json`

Plugins live under `plugins/<short>/` (for example `plugins/code/`).

Marketplace / `plugin.json` **`name`** is `nodadyoushutup-<short>` (for example
`nodadyoushutup-code`). Catalog `source` stays the short folder name.

## Plugin prefix rule (required)

Asset basenames use the **short** plugin key (folder stem), not the full
marketplace id. Every rule, skill, and agent basename **must** use that short
prefix (kebab-case), or — for a single primary skill — the exact short name.
Commands follow the same rule **except** short slash UX names documented below
(`/deslop`, `/refactor`).

| Short key (folder) | Marketplace id | Allowed basenames |
| --- | --- | --- |
| `global` | `nodadyoushutup-global` | `global-*` |
| `code` | `nodadyoushutup-code` | `code-*` |
| `business-analyst` | `nodadyoushutup-business-analyst` | `business-analyst` or `business-analyst-*` |
| `agentmemory` | `nodadyoushutup-agentmemory` | `agentmemory` or `agentmemory-*` |
| `browser` | `nodadyoushutup-browser` | `browser-*` |
| `drawio` | `nodadyoushutup-drawio` | `drawio-*` |

### Examples

- `plugins/code/rules/code-python.mdc`
- `plugins/code/skills/code-workflow/SKILL.md` with frontmatter `name: code-workflow`
- `plugins/code/agents/code-reviewer.md` with frontmatter `name: code-reviewer`
- `plugins/agentmemory/skills/agentmemory/SKILL.md` with frontmatter `name: agentmemory`
- `plugins/code/commands/deslop.md` with frontmatter `name: deslop` → `/deslop`
- `plugins/code/commands/refactor.md` with frontmatter `name: refactor` → `/refactor`
- `plugins/business-analyst/commands/business-analyst.md` with frontmatter `name: business-analyst` → `/business-analyst`
- `plugins/code/commands/code-review.md` with frontmatter `name: code-review`


### Slash command names

Skills, rules, and agents stay plugin-prefixed (`code-deslop`, `code-refactor`).

**Commands** that are meant to be typed as short slash UX may use the short
name as frontmatter `name:` and filename (for example `deslop`, `refactor` →
`/deslop`, `/refactor`). Those commands must still live under the owning
plugin (`plugins/code/commands/`) and invoke the prefixed skill. Plugin-named
commands (for example `business-analyst` → `/business-analyst`) follow the
same stem/`name:` match rule.

### Hard requirements

1. **Directory / file stem matches frontmatter `name:`** for skills and agents.
2. **Do not leave `global-*` assets inside non-`global` plugins.**
3. **Do not invent a second prefix** inside a plugin (no `code-global-*`, no
   bare `python.mdc` under `plugins/code/rules/`).
4. When moving an asset between plugins, **rename it** and update all
   cross-references in the same change.
5. Cross-plugin references use the **full prefixed name** (for example
   `code-technical-lead`, `business-analyst-planner`, `browser-automation`).

### What goes where

| Short key | Owns |
| --- | --- |
| `global` | Standing posture, writing/policy craft (not SDLC tiers) |
| `code` | Language/file-type standards, coding workflow (Direct/Standard/Full), worktrees/merge/CI craft, coding agents |
| `business-analyst` | Business analysis, multi-step planner, external researcher (optional) |
| `agentmemory` | AgentMemory MCP recall/capture (always) + on-demand ops (optional) |
| `browser` | Browser QA skill (optional) |
| `drawio` | `.drawio` author/repair craft + editor triage (optional) |

## Commits

Use Conventional Commits (`global-commit-messages`).

**Expectation for this repo:** after every change, commit and push to `origin`
on the current branch. Do not wait for the user to ask. Skip only when the user
explicitly says not to commit or push.

## Validation checklist (before commit)

- [ ] New/renamed skills/rules/agents use the owning plugin’s prefix
- [ ] Commands use the plugin prefix **or** an allowed short slash name that
      invokes the prefixed skill (`deslop` → `code-deslop`, `refactor` →
      `code-refactor`)
- [ ] Skill/agent/command `name:` frontmatter matches the directory or file stem
- [ ] Both marketplace JSON files list the plugin (if new)
- [ ] READMEs for touched plugins list the new names
- [ ] No references to old unprefixed or wrong-plugin names remain
