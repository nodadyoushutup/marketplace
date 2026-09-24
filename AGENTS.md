# AGENTS.md — marketplace-public

Public dual Claude Code / Cursor plugin marketplace. Root catalogs:

- `.cursor-plugin/marketplace.json`
- `.claude-plugin/marketplace.json`

Plugins live under `plugins/<short>/` (for example `plugins/code/`).

Marketplace / `plugin.json` **`name`** is `nodadyoushutup-<short>` (for example
`nodadyoushutup-code`). Catalog `source` stays the short folder name.

Homelab **framework** and **homelab** infra craft ship from the sibling
[`marketplace-private`](https://github.com/nodadyoushutup/marketplace-private)
repo — do not re-add `plugins/framework/` or `plugins/homelab/` here.

## Plugin prefix rule (required)

Asset basenames use the **short** plugin key (folder stem), not the full
marketplace id. Every rule, skill, and agent basename **must** use that short
prefix (kebab-case), or — for a single primary skill — the exact short name.
Commands follow the same rule **except** short slash UX names documented below
(`/deslop`, `/refactor`, `/jira`, `/confluence`).

| Short key (folder) | Marketplace id | Allowed basenames |
| --- | --- | --- |
| `global` | `nodadyoushutup-global` | `global-*` |
| `code` | `nodadyoushutup-code` | `code-*` |
| `business-analyst` | `nodadyoushutup-business-analyst` | `business-analyst` or `business-analyst-*` |
| `agentmemory` | `nodadyoushutup-agentmemory` | `agentmemory` or `agentmemory-*` |
| `atlassian` | `nodadyoushutup-atlassian` | `atlassian` or `atlassian-*` |
| `github` | `nodadyoushutup-github` | `github` or `github-*` |
| `jenkins` | `nodadyoushutup-jenkins` | `jenkins` or `jenkins-*` |
| `browser` | `nodadyoushutup-browser` | `browser-*` |
| `drawio` | `nodadyoushutup-drawio` | `drawio-*` |
| `lucidchart` | `nodadyoushutup-lucidchart` | `lucidchart-*` |

Framework (`framework` / `framework-*`) and homelab (`homelab` / `homelab-*`)
live only in **marketplace-private**.

### Examples

- `plugins/code/rules/code-python.mdc`
- `plugins/code/skills/code-workflow/SKILL.md` with frontmatter `name: code-workflow`
- `plugins/code/agents/code-reviewer.md` with frontmatter `name: code-reviewer`
- `plugins/agentmemory/skills/agentmemory/SKILL.md` with frontmatter `name: agentmemory`
- `plugins/atlassian/skills/atlassian/SKILL.md` with frontmatter `name: atlassian`
- `plugins/atlassian/commands/atlassian.md` with frontmatter `name: atlassian` → `/atlassian`
- `plugins/atlassian/commands/jira.md` with frontmatter `name: jira` → `/jira`
- `plugins/atlassian/commands/confluence.md` with frontmatter `name: confluence` → `/confluence`
- `plugins/github/skills/github/SKILL.md` with frontmatter `name: github`
- `plugins/github/commands/github.md` with frontmatter `name: github` → `/github`
- `plugins/jenkins/skills/jenkins/SKILL.md` with frontmatter `name: jenkins`
- `plugins/jenkins/commands/jenkins.md` with frontmatter `name: jenkins` → `/jenkins`
- `plugins/code/commands/deslop.md` with frontmatter `name: deslop` → `/deslop`
- `plugins/code/commands/refactor.md` with frontmatter `name: refactor` → `/refactor`
- `plugins/business-analyst/commands/business-analyst.md` with frontmatter `name: business-analyst` → `/business-analyst`
- `plugins/code/commands/code-review.md` with frontmatter `name: code-review`


### Slash command names

Skills, rules, and agents stay plugin-prefixed (`code-deslop`, `code-refactor`).

**Commands** that are meant to be typed as short slash UX may use the short
name as frontmatter `name:` and filename (for example `deslop`, `refactor` →
`/deslop`, `/refactor`; `jira`, `confluence` under `plugins/atlassian/` →
`/jira`, `/confluence`). Those commands must still live under the owning
plugin and invoke the prefixed skill (`atlassian` / `atlassian-jira-*` /
`atlassian-confluence-*`). Plugin-named commands (for example
`business-analyst` → `/business-analyst`) follow the same stem/`name:` match
rule.

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
| `code` | Language/file-type standards, coding workflow (Direct/Standard/Full), worktrees/merge craft, coding agents |
| `business-analyst` | Business analysis, multi-step planner, external researcher (optional) |
| `agentmemory` | AgentMemory MCP recall/capture (always) + on-demand ops (optional) |
| `atlassian` | Unified Jira + Confluence craft (optional) |
| `github` | Agnostic GitHub PR checks/comments + Actions CI craft (optional) |
| `jenkins` | Agnostic Jenkins builds + pipeline CI craft (optional) |
| `browser` | Browser QA skill (optional) |
| `drawio` | `.drawio` author/repair craft + editor triage (optional) |
| `lucidchart` | Lucidchart Standard Import author/repair + `.lucid` packaging (optional) |

## Commits

Use Conventional Commits (`global-commit-messages`).

**Expectation for this repo:** after every change, commit and push to `origin`
on the current branch. Do not wait for the user to ask. Skip only when the user
explicitly says not to commit or push.

## Validation checklist (before commit)

- [ ] New/renamed skills/rules/agents use the owning plugin’s prefix
- [ ] Commands use the plugin prefix **or** an allowed short slash name that
      invokes the prefixed skill (`deslop` → `code-deslop`, `refactor` →
      `code-refactor`, `jira` / `confluence` → `atlassian`, `github` /
      `jenkins` → matching plugin skill)
- [ ] Skill/agent/command `name:` frontmatter matches the directory or file stem
- [ ] Both marketplace JSON files list the plugin (if new)
- [ ] READMEs for touched plugins list the new names
- [ ] No references to old unprefixed or wrong-plugin names remain
- [ ] Framework / homelab private assets are not reintroduced under this public
      marketplace
