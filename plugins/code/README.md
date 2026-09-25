# code

Coding standards and coding workflow for Claude Code and Cursor.

Install alongside `nodadyoushutup-global` (folder `global`). This plugin owns file-type conventions, refactor /
debug / verify skills, git worktree / merge-conflict craft, and coding agents. Product planning agents live in
`business-analyst`. GitHub Actions / PR checks live in `github`; Jenkins builds live in `jenkins`.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `code-python` | Python style, typing, Google docstrings, tests |
| `code-javascript` | JS/TS/JSX style, JSDoc, robustness, tests |
| `code-html` | Semantic HTML, a11y, safety |
| `code-yaml` | YAML structure, quoting, multi-doc streams, secrets hygiene |
| `code-kubernetes` | Kubernetes manifests on top of `code-yaml` (shape, labels, probes, images) |
| `code-markdown` | Markdown structure, clarity, safety |
| `code-terraform` | HCL layout, locals SSoT, validation, templates, safety |
| `code-comments` | Sparse, durable source comments only |

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `code-workflow` | Intake → execute → verify |
| `code-investigation` | Evidence-driven codebase investigation |
| `code-systematic-debugging` | Diagnose before fixing |
| `code-verification-before-completion` | Evidence before completion claims |
| `code-deslop` | Dead-path / hygiene cleanup |
| `code-refactor` | Behavior-preserving structure (Python + JS/TS) |
| `code-worktrees` | Isolate under `~/.cursor/worktrees`; remount lanes; default-branch detect; prune on ask |
| `code-resolve-merge-conflicts` | Finish merge/rebase conflicts safely |

## Agents (both)

| Agent | Purpose |
| --- | --- |
| `code-technical-lead` | Approach, risks, sequencing |
| `code-reviewer` | Read-only review of a meaningful diff |
| `code-debugger` | Root-cause + minimal fix |
| `code-quality-assurance` | Tests in the same change for app/library code |

## Commands

Primary slash UX (run the matching skill immediately):

- `/deslop` → `code-deslop`
- `/refactor` → `code-refactor`

Also:

- `code-workflow`
- `code-review`
- `code-debug`
- `code-investigate`
- `code-verify`
- `code-worktree` → `code-worktrees`
- `code-resolve-conflicts` → `code-resolve-merge-conflicts`

## Docs

- [`docs/code-workflow.drawio`](docs/code-workflow.drawio) — visual map of `code-workflow` (tiers, phases, isolation, subagent routing)
