---
name: google-workspace
description: >-
  Operate on Gmail, Drive, Calendar, Docs, or Sheets with Google Workspace
  craft (MCP first).
---

# /google-workspace

1. If the user did not authorize Google Workspace work and named no mail,
   file, event, or doc, say so and stop.
2. Otherwise load `google-workspace` and follow the matching rule
   (`google-workspace-gmail`, `google-workspace-drive`,
   `google-workspace-calendar`, `google-workspace-docs`).
3. Prefer Google Workspace MCP. Never invent ids or accounts.
4. Return message/thread ids, file links, event times, or doc URLs with
   evidence — never localhost.
