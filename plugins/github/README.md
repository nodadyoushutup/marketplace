# github

Agnostic GitHub craft for Claude Code and Cursor — PR checks, comments, and
Actions workflow hygiene. Install when the project uses GitHub (GitHub MCP or
equivalent). No product-specific workflows or repo keys hard-coded.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `github-pr-checks` | Wait for / report PR checks; never invent green |
| `github-pr-comments` | Leave or reply to PR/issue comments |
| `github-actions` | Agnostic Actions workflow YAML (layers on `code-yaml`) |
| `github-ci-from-main` | Workflow edits may need the tracked default branch |

All rules are **agent-requested** (`alwaysApply: false`) so cold clones without
GitHub work do not load them every turn.

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `github` | Index / gate for Claude + explicit entry |

## Commands

- `/github` → PR checks, comments, or Actions workflow craft

## Pairing

- `global-mcp-first` — GitHub MCP before `gh` CLI
- `code-yaml` — YAML style under `.github/workflows/**`
- `code-workflow` — product implementation stays in `code`
- `jenkins` — Jenkins jobs/builds (sibling plugin)

## Diagrams

- [`docs/github-workflow.drawio`](docs/github-workflow.drawio) — gate → act → evidence
