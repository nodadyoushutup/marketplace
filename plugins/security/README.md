# security

Always-on agnostic security floor for application code, configuration, and
reviews. While this plugin is installed, `security-baseline` applies on every
code change. Specialist rules and `/security-review` add depth on trust-boundary
diffs. It does not define a language style, a tracker application, a git host,
or a product's account model.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `security-baseline` | Always-on must-fail floor: secrets, input, authz, cookies, SSRF, uploads, crypto, deps |
| `security-auth` | Sessions, tokens, passwords, OAuth, rate limits, object-level authorization |
| `security-injection` | Query, command, markup, SSRF, path, redirect, and upload sink depth |
| `security-secrets` | Credential storage, logs, examples, chat-paste refuse |
| `security-crypto` | Hashing, encryption, randomness, JWT verify, TLS verification |
| `security-transport` | Listeners, cookies, CORS, CSRF, HSTS, and response headers |
| `security-supply-chain` | Dependencies, lockfiles, pins, install scripts, CI least-privilege floor |
| `security-data` | Errors, logs, tenant scope, and sensitive data |

`security-baseline` is always on while this plugin is installed. The other
rules load when the change matches their description.

## Skills

| Skill | Purpose |
| --- | --- |
| `security` | Index: pick the rule, then review when the diff is high risk |
| `security-review` | Diff-scoped checklist with must-fix vs note severity |

## Agent

| Agent | Purpose |
| --- | --- |
| `security-reviewer` | Read-only findings on a diff. Does not edit. |

## Commands

- `/security` → choose the matching practice and apply it
- `/security-review` → run the checklist on the active diff

## Workflow

- [`docs/security-workflow.drawio`](docs/security-workflow.drawio) — gate → rule → checklist → ship or fix

## Defaults

- Prefer the project's existing auth, crypto, and validation libraries.
- Scope a review to the diff and its direct callers.
- Cite file paths and key names. Do not paste secret values.
- Secret-store product craft, cluster manifest craft, and CI workflow
  authorship are out of scope — apply the floors in this plugin only.
