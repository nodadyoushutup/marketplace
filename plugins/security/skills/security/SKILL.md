---
name: security
description: >-
  Agnostic security practices for secrets, authentication, authorization,
  injection, cryptography, transport, dependencies, and data exposure. Use
  when writing or reviewing trust-boundary code, or when asked for a security
  pass. Skip for a typo or comment-only edit.
---

# Security

## Gate

Skip when the change is a typo, a rename, or a comment with no behavior and
no trust impact. Load this skill when the user asks for a security review or
the diff touches auth, secrets, crypto, queries, a shell, uploads, outbound
fetches, tenant isolation, or a public network surface.

## Load map

| Need | Rule |
| --- | --- |
| Any code change while this plugin is installed | `security-baseline` |
| Login, session, password, token, permission | `security-auth` |
| Query, command, markup, path, upload, outbound URL | `security-injection` |
| Credentials, env, logs of secrets | `security-secrets` |
| Hashing, encryption, JWT, TLS verify | `security-crypto` |
| Listener, cookie, CORS, CSRF, headers | `security-transport` |
| New dependency, image, or install script | `security-supply-chain` |
| Logs, errors, cache, tenant data | `security-data` |
| Checklist before calling the change done | skill `security-review` |

## Defaults

1. Prefer the project's existing auth, crypto, and validation libraries.
2. Scope the review to the diff and its direct callers.
3. Cite paths and key names. Do not paste secret values into the reply.
4. Fix must-fix findings in the same change when the user asked to implement.
   Report them when the user asked for a review only.

## Procedure

1. Name the trust boundary the diff crosses.
   **Done when** you can point at a sink (query, shell, file, network, auth
   check, secret, or client output) or you have skipped this plugin.
2. Read the load-map rule for that sink and `security-baseline`.
   **Done when** the edit matches those rules.
3. When the change is high risk or the user asked for a pass, run
   `security-review` on the diff.
   **Done when** every applicable checklist item is met or listed as a finding.
4. Report findings with file paths. Omit secret values.
   **Done when** a reader can verify each finding from the path alone.
