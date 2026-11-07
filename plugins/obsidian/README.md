# obsidian

Agnostic Obsidian vault craft: note inventory, Markdown / wikilink /
frontmatter authoring, and gated delete/move. Prefer MCP when connected;
otherwise the vault filesystem. Never invent note paths; refuse vault dumps.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `obsidian-vault` | Resolve vault root; list/search notes; author Markdown craft |
| `obsidian-safety` | Delete / move / rename / bulk rewrite need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `obsidian` | Index / gate |

## Commands

- `/obsidian` → Obsidian vault inventory or gated note act

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.
- Memory-store export-to-Markdown tools are out of scope here — stay on vault
  note craft.

## Diagrams

- [`docs/obsidian-workflow.drawio`](docs/obsidian-workflow.drawio) — gate → act → evidence
