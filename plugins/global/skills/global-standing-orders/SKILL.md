---
name: global-standing-orders
description: >-
  Always-on portable agent postures: execute-first, MCP-first, and no-localhost
  URLs. Use at session start. Claude Code loads this as a skill; Cursor also
  ships matching alwaysApply rules. This plugin does not include language
  rules, planning, or a product's issue tracker.
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

## Scope

These orders apply on their own. Do not assume another plugin is installed.
Language style, planning, a tracker application, a git host, and diagrams
are separate concerns and are not defined here.
