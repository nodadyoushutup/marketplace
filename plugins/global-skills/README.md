# global-skills

Portable `global-*` Agent **rules**, **skills**, and **agents** shared by the
Claude Code and Cursor marketplace entries in this repo.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `global-execute-first` | Do the work; scope-grill only when blocked |
| `global-mcp-first` | Prefer ready MCP tools over CLI for the same service |
| `global-host-url` | Never give the user localhost URLs |
| `global-code-comments` | Sparse, durable comments only |
| `global-commit-messages` | Conventional Commits style |
| `global-agentmemory-capture` | Gated durable memory saves |
| `global-agentmemory-recall` | Gated proactive memory recall |
| `global-drawio-editor` | Drawio editor false-alarm triage |
| `global-policy-evolution` | Promote durable guidance into project policy |

Claude Code ignores plugin `rules/`. Use the `global-standing-orders` skill
for the same always-on postures.

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `global-standing-orders` | Always-on postures (Claude + explicit invoke) |
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

## Agents (both)

| Agent | Purpose |
| --- | --- |
| `global-business-analyst` | Shape problem, requirements, and acceptance criteria |
| `global-technical-lead` | Pick approach, risks, and sequencing |
| `global-code-reviewer` | Read-only review of a meaningful diff |

## Layout

```text
rules/<rule-name>.mdc
skills/<skill-name>/SKILL.md
agents/<agent-name>.md
```

Cursor discovers all three. Claude Code discovers `skills/` and `agents/`.
