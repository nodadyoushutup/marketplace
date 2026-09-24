---
name: global-standing-orders
description: >-
  Always-on portable agent postures: execute-first, MCP-first, no-localhost
  URLs, and conventional commits. Use at session start. Claude Code loads this
  as a skill; Cursor also ships matching alwaysApply rules. Coding standards
  live in the sibling `code` plugin; BA/planner agents live in
  `business-analyst`; other optional stacks are sibling plugins too.
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

## Conventional commits

When drafting a commit the user asked for: `type(optional-scope): imperative
summary`. Same form for PR titles. No secrets in commits.

## Sibling plugins

| Plugin | When |
| --- | --- |
| `code` | Language standards, coding workflow (Direct/Standard/Full), worktrees/merge/CI, coding agents |
| `business-analyst` | Business analysis, ambiguous multi-step planning, external research |
| `agentmemory` | AgentMemory MCP connected |
| `jira` | Jira / Atlassian tracker craft |
| `framework` | Homelab framework monorepo (from **marketplace-private**) |
| `homelab` | Homelab infra repo (from **marketplace-private**) |
| `browser` | Browser QA / Playwright |
| `drawio` | `.drawio` author/repair + editor false alarms |
