# code

Coding standards and coding workflow for Claude Code and Cursor.

This plugin owns file-type conventions, refactor / debug / verify skills,
git worktree / merge-conflict craft, and coding agents. It does not define
a tracker application, a git host, product planning, or security practices —
those live in the `security` plugin. Stack rules keep one-line pointers;
`code-workflow` Finish runs `security-review` on trust-boundary diffs when
that plugin is installed.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `code-python` | Python style, typing, Google docstrings, tests |
| `code-javascript` | JavaScript and JSX style, JSDoc, robustness, tests |
| `code-typescript` | TypeScript and TSX types, narrowing, and module boundaries |
| `code-go` | Go formatting, errors, context, and tests |
| `code-rust` | Rust ownership, errors, and tests |
| `code-react` | React components, hooks, effects, lists, tests |
| `code-nextjs` | Next.js App Router / Server vs Client Components |
| `code-flask` | Flask app factory, blueprints, sessions, extensions |
| `code-fastapi` | FastAPI routers, Pydantic, Depends, async |
| `code-html` | Semantic HTML, a11y, safety |
| `code-yaml` | YAML structure, quoting, multi-doc streams, secrets hygiene |
| `code-markdown` | Markdown structure, clarity, safety |
| `code-terraform` | HCL layout, locals SSoT, validation, templates, safety |
| `code-comments` | Sparse, durable source comments only |
| `code-unit-testing` | Lasting unit-test philosophy (core contracts, no AI scratch theater) |
| `code-commit-messages` | Conventional Commits + PR titles (always on) |

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
| `code-execute-issue` | Named tracker issue → worktree → open pull request (no merge, not done) |
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
- `/code-execute-issue <ISSUE-KEY>` → `code-execute-issue` (worktree → pull request; manual merge)
- `code-resolve-conflicts` → `code-resolve-merge-conflicts`

## Docs

- [`docs/code-workflow.drawio`](docs/code-workflow.drawio) — visual map of `code-workflow` (tiers, phases, isolation, subagent routing)
- [`docs/code-workflow.png`](docs/code-workflow.png) — same map, black background
