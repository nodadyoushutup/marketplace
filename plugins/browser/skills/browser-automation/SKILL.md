---
name: browser-automation
description: >-
  Automate a real browser for GUI checks, forms, screenshots, and web QA.
  Prefer a ready Playwright MCP or Cursor IDE browser MCP when connected;
  fall back to the agent-browser CLI only when no browser MCP is usable.
  Triggers: open a site, fill a form, click, screenshot, scrape, test this
  web app, dogfood, exploratory browser QA.
---

# Browser automation

## Priority (discover every turn you need a browser)

1. **`GetDynamicTools`** for a ready browser MCP:
   - Prefer **Playwright** namespaces when present and `ready`
     (for example `user-mcp_playwright`).
   - Else use **Cursor IDE browser** (`cursor-ide-browser`) when ready.
2. Call `GetDynamicTools` for that namespace, read the tool schema, then
   `CallDynamicTool`. Do not invent a parallel CLI path while MCP works.
3. **Fallback:** if no browser MCP is ready, auth-blocked after a cheap fix
   attempt, or MCP hard-fails for the needed action, use the
   **agent-browser** CLI when installed:

   ```bash
   command -v agent-browser && agent-browser skills get core
   # or: npx agent-browser skills get core
   ```

   Follow the CLI-served workflow for the installed version. Do not prefer
   agent-browser over a working Playwright / IDE browser MCP.

4. Last resort for read-only page fetch: `WebFetch` / `curl`. Not for click
   paths, auth flows, or visual checks.

## Hard refuse

- Do not spawn a private Playwright/Puppeteer process when a ready browser
  MCP already covers the action.
- Do not loop on a broken MCP; fall back once and continue.
- Do not put `localhost` / `127.0.0.1` in URLs shown to the user; resolve
  `$HOST` per host-URL policy when handing them a link.

## Provenance

Fallback CLI patterns inspired by
[vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
(Apache-2.0 / see upstream LICENSE). This skill does **not** vendor the
full agent-browser package; install the CLI only when MCP is unavailable.
