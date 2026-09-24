---
name: confluence
description: >-
  Agnostic Confluence craft: create-only page filing by default, Overview +
  headed section bodies, safe section updates, and draw.io diagram attach
  pairing. Use when creating, updating, searching, or commenting on Confluence
  pages. Skip when the user did not authorize docs work.
---

# Confluence

## Gate

No explicit create/update/search/comment ask and no named page id or
title+space → **skip** — stay pageless. Prefer a connected Confluence /
Atlassian MCP when docs work is in play.

## Load map

| Need | Rule / action |
| --- | --- |
| May I create? | `confluence-create` |
| Page body shape | `confluence-structure` + `confluence-page` |
| Edit existing | `confluence-update` |
| Architecture / workflow figure | `confluence-diagrams` (+ `drawio-author`) |

## Defaults

1. Create-only / update-only unless the user adds an explicit implement verb.
2. Never invent space key, parent page, or template id.
3. Search before create — do not mint a near-duplicate title in the same space.
4. Prefer `confluence_update_page_section` over full-body rewrites.
5. Diagrams: author with `drawio-author`, then attach — do not paste raw XML
   into the page body.
