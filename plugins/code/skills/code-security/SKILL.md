---
name: code-security
description: >-
  Agnostic secure-coding checklist for auth, secrets, injection, SSRF, path
  traversal, crypto, and logging. Use when needs_security is true, before
  shipping trust-boundary changes, or when asked for a security pass on a
  diff. Pair with always-on rule code-security.
---

# code-security

## Gate

Skip when the change is typo/rename/comment-only with no behavior or trust
impact. Otherwise load when:

- Execution notes set `needs_security: true`
- The user asks for a security review / hardening pass
- The diff touches auth, secrets, crypto, SQL, shell, uploads, SSRF-prone
  fetches, multi-tenant isolation, or public HTTP surfaces

## Load map

| Need | Asset |
| --- | --- |
| Always-on baseline | rule `code-security` |
| Language/file style | matching `code-python` / `code-javascript` / … |
| Secrets in infra YAML/HCL | `code-yaml`, `code-terraform`, `code-kubernetes` |

## Checklist (diff-scoped)

Work the list against the changed code and its direct callers. Skip items that
cannot apply. Prefer evidence (paths, sinks) over generic advice.

### 1. Secrets

- [ ] No new hardcoded credentials, private keys, or long-lived tokens
- [ ] Logs, traces, and API errors omit secrets and session material
- [ ] Examples and tests use placeholders or fakes — not production values

### 2. Injection

- [ ] SQL / datastore: parameterized or ORM-bound; no user string in query text
- [ ] OS/commands: no unsanitized shell interpolation
- [ ] HTML/JS: untrusted data escaped or passed through the project's sanitizer
- [ ] Template/path engines: no user-controlled template or view names

### 3. AuthN / AuthZ

- [ ] Sensitive routes/actions enforce auth on the server
- [ ] Authorization checks the actor's rights on *this* resource (IDOR-safe)
- [ ] Session/cookie flags follow project standards (HttpOnly / Secure / SameSite
      when applicable)
- [ ] Password reset, invite, and magic-link tokens are single-use, time-bound,
      and high entropy when present in the diff

### 4. Requests and files

- [ ] Server-side HTTP clients do not fetch arbitrary user URLs (allowlist or
      block private/link-local targets)
- [ ] Uploads: size/type limits; stored outside the web root or served safely;
      no executable content trusted as static
- [ ] Path joins cannot escape an allowlisted directory

### 5. Crypto and randomness

- [ ] Passwords hashed with a modern KDF via a maintained library
- [ ] Tokens/IDs use CSPRNG; no predictable sequences for security decisions
- [ ] TLS and certificate verification left on unless the environment truly
      requires otherwise (and that is explicit)

### 6. Multi-tenant / data exposure

- [ ] Queries and caches are scoped by tenant/owner where the product is
      multi-tenant
- [ ] Error and debug payloads do not leak stack traces or internal hosts to
      untrusted clients in production paths

## Phase 9 use

When `code-workflow` selects the security gate:

1. Run this checklist on the diff (Read/Grep; no drive-by refactors).
2. Fix must-fix findings in the same change; re-verify.
3. Optionally launch the host's dedicated security-review subagent for a second
   pass — this skill is the portable floor when that subagent is absent.
4. Hand off to `code-reviewer` for general correctness after security is clear.

## Refuse

- Do not dump real secrets into chat while explaining findings — cite key names
  and file paths only
- Do not expand into a full-product penetration test unless the user asked for
  that scope
