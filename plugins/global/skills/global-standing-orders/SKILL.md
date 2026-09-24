---
name: global-standing-orders
description: >-
  Always-on portable agent postures: execute-first, change intensity,
  MCP-first, no-localhost URLs, sparse code comments, and conventional
  commits. Use at session start. Claude Code loads this as a skill; Cursor
  also ships matching alwaysApply rules under rules/. Optional stacks
  (AgentMemory, Docker, Terraform, browser, git, drawio) live in sibling
  marketplace plugins.
---

# Standing orders (portable)

Apply these postures for the whole session unless the user overrides them.

## Execute first

Do the work. Do not ask permission to edit, run commands, or verify. Ask at
most one question, and only for irreversible data loss, a missing secret,
incompatible product outcomes with no safe default, or a broad ask with no
success criteria. Tracker create-only asks: file the issue and stop.

See also: `global-action-first`.

## MCP first

When a ready MCP covers the external service, use it. Do not prefer CLI,
curl, or ad-hoc SDKs for the same action. No matching MCP → use the normal
CLI/SDK immediately.

## No localhost for the user

Never put `localhost` or `127.0.0.1` in a URL shown to the user. Resolve a
machine-reachable `$HOST` (project env → detect → optional memory preference)
and build `http://$HOST:<port>`.

## Sparse comments

Default: no new `//` / `#` / block comments. Prefer names, structure, and
tests. Put ephemeral explanation in chat or the commit body.

## Conventional commits

When drafting a commit the user asked for: `type(optional-scope): imperative
summary`. Same form for PR titles. No secrets in commits.

## Change intensity

Classify work as L0–L3 (`global-change-intensity`). Stay light on L0/L1; finish
L2/L3 with verify evidence when shipping is required. Do not spin planner/QA
theater for trivia.

## Optional sibling plugins

Install separately when needed:

| Plugin | When |
| --- | --- |
| `agentmemory` | AgentMemory MCP connected |
| `docker` | Docker/Compose work |
| `terraform` | Terraform/HCL work |
| `browser` | Browser QA / Playwright |
| `git` | Worktrees, merge conflicts, CI-from-main |
| `drawio` | Cursor `.drawio` editor false alarms |
