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
the diff touches auth, sessions, cookies, secrets, crypto, JWT, SQL, a shell,
uploads, redirects, deserialization, outbound fetches, tenant isolation,
dependencies, response headers, or a public network surface.

## Load map

| Need | Rule |
| --- | --- |
| Any code change while this plugin is installed | `security-baseline` |
| Login, session, password, token, permission, rate limit | `security-auth` |
| Query, command, markup, path, upload, outbound URL, redirect | `security-injection` |
| Credentials, env, logs of secrets | `security-secrets` |
| Hashing, encryption, JWT verify, TLS verify | `security-crypto` |
| Listener, cookie flags, CORS, CSRF, headers, HSTS | `security-transport` |
| New dependency, image, or install script | `security-supply-chain` |
| Logs, errors, cache, tenant data | `security-data` |
| Checklist before calling the change done | skill `security-review` |
| Chat paste of a credential | refuse copy; say rotate; continue without the value |
| Secret-store path read/write | out of scope — apply `security-secrets` refuse-leak floor only |
| Plaintext cluster Secret, RBAC, privileged pod | out of scope for product craft — apply `security-baseline` / `security-secrets` |
| CI workflow `permissions:`, OIDC, pin style | out of scope for workflow craft — least privilege + pin non-`latest` here |

## Defaults

1. Prefer the project's existing auth, crypto, and validation libraries.
2. Scope the review to the diff and its direct callers.
3. Cite paths and key names. Do not paste secret values into the reply.
4. Fix must-fix findings in the same change when the user asked to implement.
   Report them when the user asked for a review only.
5. When the diff adds a sink, add or extend a regression test for the control.

## Procedure

1. Name the trust boundary the diff crosses. Who is the attacker, what data
   moves, which check stops them.
   **Done when** you can point at a sink (query, shell, file, network, auth
   check, secret, cookie, redirect, deserialize, or client output) or you have
   skipped this plugin.
2. Read the load-map rule for that sink and `security-baseline`.
   **Done when** the edit matches those rules.
3. When the change is high risk or the user asked for a pass, run
   `security-review` on the diff.
   **Done when** every applicable checklist item is met or listed as a finding.
4. Report findings with file paths. Omit secret values.
   **Done when** a reader can verify each finding from the path alone.
