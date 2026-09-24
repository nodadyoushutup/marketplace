---
name: confluence
description: >-
  Create, update, or shape a Confluence page with agnostic structure and
  draw.io diagram attach craft.
---

# /confluence

1. If the user did not authorize create/update/search/comment and named no
   page, say so and stop — do not invent a page.
2. Otherwise load `confluence` and follow `confluence-create` or
   `confluence-update` as the intent requires.
3. New pages: write Overview + headed sections per `confluence-structure`.
4. Prefer Confluence MCP tools. Never invent space/parent/template.
5. Create-only or update-only unless the user explicitly asked to implement
   product code too.
6. Diagrams: follow `confluence-diagrams` (author with `drawio-author`, then
   upload/attach).
7. Return the page title, id, and browse URL when known.
