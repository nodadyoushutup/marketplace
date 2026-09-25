---
name: google
description: >-
  Unified Google Workspace craft: Gmail search/draft/send, Drive file ops,
  Calendar events, Docs and Sheets reads/edits. Prefer Google Workspace MCP.
  Skip when the user did not authorize Google/Workspace work.
---

# Google Workspace

## Gate

No explicit Gmail / Drive / Calendar / Docs / Sheets / Google Workspace ask
and no named message, file, event, or doc → **skip**. Prefer a connected
Google Workspace MCP when any surface is in play (`global-mcp-first`).

Route by product:

| Surface | Signals |
| --- | --- |
| Gmail | email, inbox, thread, draft, send, label |
| Drive | Drive, file, folder, share link, upload |
| Calendar | calendar, event, meeting, OOO, free/busy |
| Docs / Sheets | Doc, Spreadsheet, tab, cell range |

## Load map

| Need | Rule |
| --- | --- |
| Mail search / read / draft / send / labels | `google-gmail` |
| Drive search / read / create / share | `google-drive` |
| Calendar list / create / update / freebusy | `google-calendar` |
| Docs or Sheets content | `google-docs` |

## Defaults

1. Never invent user email, file id, event id, or spreadsheet id.
2. Use the MCP-configured Google account; do not ask the operator to paste
   tokens. If the namespace documents a fixed `user_google_email`, use it.
3. Destructive or outbound actions (send mail, share publicly, delete file,
   cancel event) need an explicit user verb this turn.
4. Draft-before-send for new mail unless the user said “send”.
5. No secrets, tokens, or full mailbox dumps in chat.
