# code

Coding standards and coding workflow for Claude Code and Cursor.

Install alongside `nodadyoushutup-global` (folder `global`). This plugin owns file-type conventions, refactor /
debug / verify skills, git worktree / merge-conflict craft, and coding agents. Product planning agents stay in
`global`.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `code-python` | Python style, typing, Google docstrings, tests |
| `code-javascript` | JS/JSX style, JSDoc, robustness, tests |
| `code-html` | Semantic HTML, a11y, safety |
| `code-yaml` | YAML structure, quoting, secrets hygiene |
| `code-markdown` | Markdown structure, clarity, safety |
| `code-terraform` | HCL layout, locals SSoT, validation, templates, safety |
| `code-comments` | Sparse, durable source comments only |
| `code-ci-from-main` | CI workflow edits must land on the tracked branch |

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `code-workflow` | Intake → execute → verify |
| `code-investigation` | Evidence-driven codebase investigation |
| `code-systematic-debugging` | Diagnose before fixing |
| `code-verification-before-completion` | Evidence before completion claims |
| `code-deslop` | Dead-path / hygiene cleanup |
| `code-refactor` | Behavior-preserving structure (Python + JS/TS) |
| `code-worktrees` | Isolate work under `~/.cursor/worktrees` |
| `code-resolve-merge-conflicts` | Finish merge/rebase conflicts safely |

## Agents (both)

| Agent | Purpose |
| --- | --- |
| `code-technical-lead` | Approach, risks, sequencing |
| `code-reviewer` | Read-only review of a meaningful diff |
| `code-debugger` | Root-cause + minimal fix |
| `code-quality-assurance` | Tests in the same change for L2/L3 code |

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
