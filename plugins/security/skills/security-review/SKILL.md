---
name: security-review
description: >-
  Diff-scoped security checklist for auth, secrets, injection, server-side
  request forgery, path traversal, crypto, transport, dependencies, and data
  exposure. Use before shipping a trust-boundary change, or when asked for a
  security pass on a diff.
---

# Security review

## Gate

Skip a typo, rename, or comment-only diff. Run when the user asks for a
security pass, or the diff touches auth, sessions, cookies, secrets, crypto,
JWT, SQL, a shell, uploads, redirects, deserialization, outbound fetches,
tenant isolation, dependencies, response headers, or a public HTTP surface.

## Load map

| Need | Rule |
| --- | --- |
| Floor for every reviewed diff | `security-baseline` |
| The sink the diff actually touches | the matching `security-*` rule from skill `security` |

## Severity

**Must-fix (block ship):** hardcoded secret; missing server-side object-level
authz; query or shell injection; SSRF; TLS verification off without an
explicit user ask this turn; unsafe deserialization; upload served as active
content; secret in logs or client errors.

**Note (do not block alone):** missing HSTS on an existing site; missing rate
limit; header policy on an existing app; CSP not yet present on a legacy page.

## Procedure

Work the list against the changed code and its direct callers. Skip items
that cannot apply. Prefer a path and a sink over generic advice. When the
diff adds a sink, require a regression test that covers the control.

1. **Secrets.** No new hardcoded credentials, private keys, or long-lived
   tokens. Logs, traces, and client errors omit secrets and session material.
   Examples and tests use placeholders.
   **Done when** each new secret-shaped string is a placeholder or a reference
   to the secret store.
2. **Injection.** Datastore queries are parameterized. Commands are argument
   arrays. HTML and JavaScript encode untrusted data or use the project's
   sanitizer. User input does not choose a template name. Untrusted data is
   not deserialized into an object graph.
   **Done when** each new sink has a bound parameter or an encoder.
3. **Auth.** Sensitive actions enforce auth on the server. The check covers
   this object, not only "is signed in." Cookie sessions set `HttpOnly`,
   `Secure`, and `SameSite` when this diff adds them. Cookie state changes
   have a cross-site request check. Recovery tokens are single-use,
   time-limited, and high entropy.
   **Done when** each new sensitive action has a server-side check.
4. **Requests and files.** Outbound HTTP does not fetch an arbitrary user URL;
   hosts are allowlisted and re-checked after resolve and on redirects.
   Uploads have size and type limits, a generated name outside the web root,
   and are not executed as static content. Path joins cannot leave an
   allowlisted directory. Redirect targets are allowlisted.
   **Done when** each new fetch, upload, path, or redirect has that limit.
5. **Crypto.** Passwords use a modern password hash via a maintained library.
   Tokens use a cryptographic random generator. TLS verification stays on
   unless the user asked to disable it this turn. Token verification checks
   algorithm allowlist, expiry, issuer, and audience, and refuses caller-chosen
   `kid`/`jku`/`x5u`.
   **Done when** no new custom cipher or disabled certificate check remains
   without an explicit user ask this turn.
6. **Data.** Tenant or owner filters cover new queries and cache keys. Client
   errors in production paths omit stack traces and internal hosts.
   **Done when** a second tenant cannot read the new data through the diff.
7. **Supply chain.** A new dependency has a lockfile update. Production images
   pin a non-`latest` tag. Remote `curl|sh` is refused. CI does not print
   secrets.
   **Done when** the manifest change includes the lockfile, or there is no
   dependency change.
8. **Tests.** Each new sink added by the diff has a regression test, or an
   existing test is extended to cover the control.
   **Done when** the test path is named, or the item is listed as a must-fix
   finding.

Fix must-fix findings in the same change when the user asked to implement,
then re-check the failing item. List notes separately. Do not expand into a
full-product penetration test unless the user asked for that scope.

## Refuse

- Do not paste secret values into the reply. Cite key names and file paths.
- Do not report a scanner result you did not run.
