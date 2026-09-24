# global-skills

Portable `global-*` Agent Skills shared by the Claude Code and Cursor marketplace entries in this repo.

## Skills

| Skill | Purpose |
| --- | --- |
| `global-action-first` | Lead with the result; shape replies for action |
| `global-asd-ste100` | Rewrite English so agents cannot misread it |
| `global-browser-automation` | Browser QA via MCP, with CLI fallback |
| `global-code-investigation` | Evidence-driven codebase investigation |
| `global-coding-workflow` | Intake → execute → verify coding workflow |
| `global-deslopify` | Dead-path / hygiene cleanup audit |
| `global-docker` | Docker / Compose ops from the host CLI |
| `global-git-worktrees` | Isolate work with git worktrees |
| `global-javascript-refactor` | Behavior-preserving JS/TS refactor |
| `global-policy-evolution` | Promote durable guidance into project policy |
| `global-python-refactor` | Behavior-preserving Python refactor |
| `global-refactor` | Cross-language refactor audit dispatcher |
| `global-resolve-merge-conflicts` | Finish merge/rebase conflicts safely |
| `global-skill-intake` | Audit third-party skills before install |
| `global-systematic-debugging` | Diagnose before fixing |
| `global-verification-before-completion` | Evidence before completion claims |
| `global-writing-for-agents` | Author skills and agent guidance docs |

## Layout

```text
skills/<skill-name>/SKILL.md
```

Both Claude Code and Cursor discover skills from this directory when the plugin is installed.
