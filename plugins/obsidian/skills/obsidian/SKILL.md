---
name: obsidian
description: >-
  Agnostic Obsidian vault craft: note inventory, Markdown/wikilink/frontmatter
  authoring, and gated delete/move. Prefer MCP when connected; otherwise vault
  filesystem. Skip when the user did not authorize this surface.
---

# obsidian

## Gate

No explicit Obsidian / vault / note / wikilink / frontmatter / `.md` vault ask
→ **skip**. Ordinary repo Markdown that is not an Obsidian vault stays ordinary
coding. Prefer a connected MCP; else the vault filesystem with a resolved root.

## Load map

| Need | Rule |
| --- | --- |
| Resolve vault · list/search notes · author Markdown | `obsidian-vault` |
| Delete / move / rename / bulk rewrite gates | `obsidian-safety` |

## Defaults

1. Never invent note paths, folder names, or vault roots — resolve first
   (user path, workspace vault, `.obsidian/` marker, or MCP).
2. Prefer edit-in-place over recreate; preserve existing frontmatter keys the
   user did not ask to change.
3. Use Obsidian wikilinks (`[[Note]]`, `[[Note#Heading]]`, `[[Note|alias]]`)
   and `![[embed]]` when linking inside the vault; use standard Markdown links
   only when the target is outside the vault.
4. Keep YAML frontmatter valid; do not invent community-plugin-only keys unless
   the vault already uses them.
5. Never paste vault secrets, API tokens, or private journal dumps into chat —
   summarize and cite paths.
