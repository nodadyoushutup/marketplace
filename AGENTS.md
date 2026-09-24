# AGENTS.md — marketplace

Dual Claude Code / Cursor plugin marketplace. Root catalogs:

- `.cursor-plugin/marketplace.json`
- `.claude-plugin/marketplace.json`

Plugins live under `plugins/<name>/`.

## Plugin prefix rule (required)

Every rule, skill, agent, and command basename **must be prefixed with the plugin
name** that owns it (kebab-case), or — for a single primary skill — use the
exact plugin name.

| Plugin | Allowed basenames |
| --- | --- |
| `global` | `global-*` |
| `code` | `code-*` |
| `agentmemory` | `agentmemory` or `agentmemory-*` |
| `docker` | `docker-*` |
| `browser` | `browser-*` |
| `git` | `git-*` |
| `drawio` | `drawio-*` |

### Examples

- `plugins/code/rules/code-python.mdc`
- `plugins/code/skills/code-workflow/SKILL.md` with frontmatter `name: code-workflow`
- `plugins/code/agents/code-reviewer.md` with frontmatter `name: code-reviewer`
- `plugins/docker/skills/docker-ops/SKILL.md` with frontmatter `name: docker-ops`
- `plugins/agentmemory/skills/agentmemory/SKILL.md` with frontmatter `name: agentmemory`
- `plugins/code/commands/code-review.md` with frontmatter `name: code-review`

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

| Plugin | Owns |
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

- [ ] New/renamed assets (rules, skills, agents, commands) use the owning plugin’s prefix
- [ ] Skill/agent `name:` frontmatter matches the directory or file stem
- [ ] Both marketplace JSON files list the plugin (if new)
- [ ] READMEs for touched plugins list the new names
- [ ] No references to old unprefixed or wrong-plugin names remain
