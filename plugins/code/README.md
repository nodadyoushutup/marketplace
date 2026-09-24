# code

Coding standards and coding workflow for Claude Code and Cursor.

Install alongside `global`. This plugin owns file-type conventions, refactor /
debug / verify skills, and coding agents. Product planning agents stay in
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

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `code-workflow` | Intake → execute → verify |
| `code-investigation` | Evidence-driven codebase investigation |
| `code-systematic-debugging` | Diagnose before fixing |
| `code-verification-before-completion` | Evidence before completion claims |
| `code-deslopify` | Dead-path / hygiene cleanup |
| `code-refactor` | Behavior-preserving structure (Python + JS/TS) |

## Agents (both)

| Agent | Purpose |
| --- | --- |
| `code-technical-lead` | Approach, risks, sequencing |
| `code-reviewer` | Read-only review of a meaningful diff |
| `code-debugger` | Root-cause + minimal fix |
| `code-quality-assurance` | Tests in the same change for L2/L3 code |

## Commands

- `code-debug`
- `code-deslop`
- `code-investigate`
- `code-refactor`
- `code-review`
- `code-verify`
- `code-workflow`
