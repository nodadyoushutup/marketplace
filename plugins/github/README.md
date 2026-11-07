# github

Agnostic GitHub craft for Claude Code and Cursor — PR checks, comments, and
Actions workflow hygiene. Install when the project uses GitHub (GitHub MCP or
equivalent). No product-specific workflows or repo keys hard-coded.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `github-pr-checks` | Wait for / report PR checks; never invent green |
| `github-pr-comments` | Leave or reply to PR/issue comments |
| `github-pr-titles` | Conventional Commits shape for PR titles |
| `github-actions` | Actions workflow YAML: structure, pins, no secrets |
| `github-runners` | Self-hosted runners: labels, registration hygiene, `runs-on` |
| `github-ci-from-main` | Workflow edits may need the tracked default branch |

All rules are **agent-requested** (`alwaysApply: false`) so cold clones without
GitHub work do not load them every turn.

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `github` | Index / gate for Claude + explicit entry |

## Commands

- `/github` → PR checks, comments, or Actions workflow craft

## Defaults

- Prefer a connected GitHub tool. Use the `gh` CLI only when that tool is
  missing or has failed.
- Workflow YAML stays in this plugin: 2-space indent, no secrets in the file.
- This plugin does not implement product code and does not define other CI
  systems.

## Diagrams

- [`docs/github-workflow.drawio`](docs/github-workflow.drawio) — gate → act → evidence
