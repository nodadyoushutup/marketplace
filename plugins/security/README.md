# security

Agnostic security practices for application code, configuration, and reviews.
Install this plugin when a change crosses a trust boundary. It does not define
a language style, a tracker application, a git host, or a product's account
model.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `security-baseline` | Always-on floor: secrets, input, authz, output, crypto |
| `security-auth` | Sessions, tokens, passwords, OAuth, authorization |
| `security-injection` | Query, command, markup, SSRF, path, and upload sinks |
| `security-secrets` | Credential storage, logs, examples, and pasted secrets |
| `security-crypto` | Hashing, encryption, randomness, JWT, TLS verification |
| `security-transport` | Listeners, cookies, CORS, CSRF, and response headers |
| `security-supply-chain` | Dependencies, lockfiles, pins, and install scripts |
| `security-data` | Errors, logs, tenant scope, and sensitive data |

`security-baseline` is always on while this plugin is installed. The other
rules load when the change matches their description.

## Skills

| Skill | Purpose |
| --- | --- |
| `security` | Index: pick the rule, then review when the diff is high risk |
| `security-review` | Diff-scoped checklist before calling a trust-boundary change done |

## Agent

| Agent | Purpose |
| --- | --- |
| `security-reviewer` | Read-only findings on a diff. Does not edit. |

## Commands

- `/security` → choose the matching practice and apply it
- `/security-review` → run the checklist on the active diff

## Workflow

- [`docs/security-workflow.drawio`](docs/security-workflow.drawio) — gate → rule → checklist

## Defaults

- Prefer the project's existing auth, crypto, and validation libraries.
- Scope a review to the diff and its direct callers.
- Cite file paths and key names. Do not paste secret values.
