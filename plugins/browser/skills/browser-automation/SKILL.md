---
name: browser-automation
description: >-
  Automate a real browser for GUI checks, forms, screenshots, and web QA.
  Prefer a ready Playwright MCP or Cursor IDE browser MCP when connected;
  fall back to an agent-browser CLI only when no browser MCP is usable.
  Triggers: open a site, fill a form, click, screenshot, scrape, test this
  web app, dogfood, exploratory browser QA.
---

# Browser automation

Drive a real browser for GUI QA. Prefer a connected browser MCP; only drop to
a CLI when MCP cannot do the job.

## Priority (every turn you need a browser)

1. **`GetDynamicTools`** for a ready browser MCP:
   - Prefer **Playwright** namespaces when present and `ready`
     (for example `user-mcp_playwright`).
   - Else use **Cursor IDE browser** (`cursor-ide-browser`) when ready.
2. Inspect that namespace’s tool schemas, then `CallDynamicTool`. Do not invent
   a parallel CLI path while MCP works.
3. **Fallback:** if no browser MCP is ready, auth stays blocked after a cheap
   fix, or MCP hard-fails for the needed action, use an installed
   **agent-browser**-compatible CLI:

   ```bash
   command -v agent-browser && agent-browser skills get core
   # or: npx agent-browser skills get core
   ```

   Follow the CLI’s own workflow for that version. Never prefer CLI over a
   working Playwright / IDE browser MCP.

4. Last resort for read-only page fetch: `WebFetch` / `curl`. Not for clicks,
   auth flows, or visual checks.

## Hard refuse

- Do not spawn a private Playwright/Puppeteer process when a ready browser MCP
  already covers the action.
- Do not loop on a broken MCP; fall back once and continue.
- Do not put `localhost` / `127.0.0.1` in URLs shown to the user; resolve
  `$HOST` per `global-host-url` when handing them a link.
