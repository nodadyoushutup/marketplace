---
name: global-standing-orders
description: >-
  Always-on portable agent postures: execute-first, MCP-first, no-localhost
  URLs, sparse code comments, conventional commits, and gated AgentMemory
  capture/recall. Use at session start and whenever standing guidance might
  conflict with a local habit. Claude Code loads this as a skill; Cursor also
  ships the same text as alwaysApply rules under rules/.
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
machine-reachable `$HOST` (project env → detect → optional AgentMemory) and
build `http://$HOST:<port>`.

## Sparse comments

Default: no new `//` / `#` / block comments. Prefer names, structure, and
tests. Put ephemeral explanation in chat or the commit body.

## Conventional commits

When drafting a commit the user asked for: `type(optional-scope): imperative
summary`. No secrets in commits.

## AgentMemory (gated)

If AgentMemory is not connected, skip memory tools entirely. When it is
connected: recall before re-investigating known areas; save verified durable
insights (usually 0–2 per turn). Do not save routine churn.

## Drawio editor false alarm

If Cursor refuses to open a `.drawio` with an assertion about undefined/null,
parse the XML first. Valid XML means editor bug — open once with Text Editor,
then reopen normally. Do not "repair" the diagram.
