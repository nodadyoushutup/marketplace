# drawio

Author and repair clean `.drawio` diagrams (intentional lanes, readable padded
labels, dedicated edge corridors), plus Cursor custom-editor false-alarm triage.

Reference graphs in this marketplace:
`plugins/code/docs/code-workflow.drawio`,
`plugins/atlassian/docs/atlassian-jira-workflow.drawio`,
`plugins/business-analyst/docs/business-analyst-workflow.drawio`.

## Contents

### Rules (Cursor)
- `drawio-layout.mdc` — layout, typography, routing, and chip placement for `**/*.drawio`
- `drawio-editor.mdc` — editor open assertion ≠ broken XML

### Skills
- `drawio-author` — create or redesign diagrams under a layout contract
  - `references/style-recipes.md` — copy-paste `style=` strings (padding, chips, contrast)
- `drawio-repair` — fix overlaps, stacked arrows, edge-through-box, clipped labels

## Commands

- `drawio-author`
- `drawio-repair`
- `drawio-triage`

## Diagrams

- [`docs/drawio-workflow.drawio`](docs/drawio-workflow.drawio) — gate → act → evidence
