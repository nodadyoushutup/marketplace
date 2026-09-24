# code

Coding standards and coding workflow for Claude Code and Cursor.

Install alongside `global`. This plugin owns file-type conventions, refactor /
debug / verify skills, and coding agents. Product planning agents stay in
`global`.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `python` | Python style, typing, Google docstrings, tests |
| `javascript` | JS/JSX style, JSDoc, robustness, tests |
| `html` | Semantic HTML, a11y, safety |
| `yaml` | YAML structure, quoting, secrets hygiene |
| `markdown` | Markdown structure, clarity, safety |
| `terraform` | HCL layout, locals SSoT, safety |
| `terraform-validation` | Variable validation + templatefile conventions |
| `code-comments` | Sparse, durable source comments only |

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `global-coding-workflow` | Intake → execute → verify |
| `global-code-investigation` | Evidence-driven codebase investigation |
| `global-systematic-debugging` | Diagnose before fixing |
| `global-verification-before-completion` | Evidence before completion claims |
| `global-deslopify` | Dead-path / hygiene cleanup |
| `global-refactor` | Cross-language refactor dispatcher |
| `global-python-refactor` | Behavior-preserving Python refactor |
| `global-javascript-refactor` | Behavior-preserving JS/TS refactor |

## Agents (both)

| Agent | Purpose |
| --- | --- |
| `global-technical-lead` | Approach, risks, sequencing |
| `global-code-reviewer` | Read-only review of a meaningful diff |
| `global-debugger` | Root-cause + minimal fix |
| `global-quality-assurance` | Tests in the same change for L2/L3 code |
