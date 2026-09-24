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
| `agentmemory` | `nodadyoushutup-agentmemory` | `agentmemory` or `agentmemory-*` |
| `docker` | `nodadyoushutup-docker` | `docker-*` |
| `browser` | `nodadyoushutup-browser` | `browser-*` |
| `git` | `nodadyoushutup-git` | `git-*` |
| `drawio` | `nodadyoushutup-drawio` | `drawio-*` |

### Examples

- `plugins/code/rules/code-python.mdc`
- `plugins/code/skills/code-workflow/SKILL.md` with frontmatter `name: code-workflow`
- `plugins/code/agents/code-reviewer.md` with frontmatter `name: code-reviewer`
- `plugins/docker/skills/docker-ops/SKILL.md` with frontmatter `name: docker-ops`
- `plugins/agentmemory/skills/agentmemory/SKILL.md` with frontmatter `name: agentmemory`
- `plugins/code/commands/deslop.md` with frontmatter `name: deslop` → `/deslop`
- `plugins/code/commands/refactor.md` with frontmatter `name: refactor` → `/refactor`
- `plugins/code/commands/code-review.md` with frontmatter `name: code-review`


### Slash command names

Skills, rules, and agents stay plugin-prefixed (`code-deslop`, `code-refactor`).

**Commands** that are meant to be typed as short slash UX may use the short
name as frontmatter `name:` and filename (for example `deslop`, `refactor` →
`/deslop`, `/refactor`). Those commands must still live under the owning
plugin (`plugins/code/commands/`) and invoke the prefixed skill.

### Hard requirements

1. **Directory / file stem matches frontmatter `name:`** for skills and agents.
2. **Do not leave `global-*` assets inside non-`global` plugins.**
3. **Do not invent a second prefix** inside a plugin (no `code-global-*`, no
   bare `python.mdc` under `plugins/code/rules/`).
4. When moving an asset between plugins, **rename it** and update all
   cross-references in the same change.
5. Cross-plugin references use the **full prefixed name** (for example
   `code-technical-lead`, `browser-automation`, `docker-ops`).

### What goes where

| Short key | Owns |
| --- | --- |
| `global` | Standing posture, SDLC intensity, planning agents, writing/policy craft |
| `code` | Language/file-type standards, coding workflow skills, coding agents |
| `agentmemory` | AgentMemory MCP capture/recall (optional) |
| `docker` | Docker/Compose craft (optional) |
| `browser` | Browser QA skill (optional) |
| `git` | Worktrees, merge conflicts, CI-from-main (optional) |
| `drawio` | Cursor `.drawio` editor triage (optional) |

## Commits

Use Conventional Commits (`global-commit-messages`). For this repo, commit and
push after meaningful changes unless the user says otherwise.

## Validation checklist (before commit)

- [ ] New/renamed skills/rules/agents use the owning plugin’s prefix
- [ ] Commands use the plugin prefix **or** an allowed short slash name that
      invokes the prefixed skill (`deslop` → `code-deslop`, `refactor` →
      `code-refactor`)
- [ ] Skill/agent/command `name:` frontmatter matches the directory or file stem
- [ ] Both marketplace JSON files list the plugin (if new)
- [ ] READMEs for touched plugins list the new names
- [ ] No references to old unprefixed or wrong-plugin names remain
