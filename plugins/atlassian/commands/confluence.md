---
name: confluence
description: >-
  Create, update, or shape a Confluence page using the atlassian plugin
  (search-before-create; headed sections; draw.io attach).
---

# Confluence

Short slash UX for Atlassian docs work (`/confluence`).

1. Prefer a ready Confluence / Atlassian MCP when docs work is in play.
2. Load `atlassian` and follow `atlassian-confluence-create` or
   `atlassian-confluence-update` as the intent requires.
3. New pages: write Overview + headed sections per
   `atlassian-confluence-structure`.
4. Prefer section updates over full-body rewrites; preserve macros.
5. Search before create — update a near-duplicate instead of minting another.
6. Diagrams: follow `atlassian-confluence-diagrams` (author with
   `drawio-author`, then attach).
