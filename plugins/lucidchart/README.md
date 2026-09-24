# lucidchart

Author and repair clean **Lucidchart** diagrams using the same layout craft as
`drawio`, expressed as **Lucid Standard Import** JSON.

## Contents

### Rules (Cursor)
- `lucidchart-layout.mdc` — layout, typography, and routing for `**/*.lucid.json`
- `lucidchart-package.mdc` — package `.lucid.json` → `.lucid` zip; API import notes

### Skills
- `lucidchart-author` — create or redesign under a layout contract
  - `references/style-recipes.md` — Standard Import shape/line recipes
  - `scripts/package_lucid.py` — zip `document.json` into `.lucid`
- `lucidchart-repair` — fix overlaps, stacked lines, edge-through-box in SI JSON

## Commands

- `lucidchart-author`
- `lucidchart-repair`
- `lucidchart-package`

## Format note

Lucid’s native editor format is not agent-writable. The source of truth in git
is `*.lucid.json` (Standard Import). Package to `.lucid` and create a **new**
document via Lucid’s Create Document API (or UI import). SI cannot patch an
existing Lucid document in place — re-import after repair.
