---
name: drawio-repair
description: >-
  Repair messy .drawio diagrams: overlapping boxes, stacked arrow paths, clipped
  or low-contrast labels, edges through nodes, and broken orthogonal routing.
  Use when an existing diagram is hard to read or the user asks to clean up /
  fix layout without changing meaning.
---

# Drawio repair

Fix layout and readability defects in an existing `.drawio` while preserving
meaning (ids, labels, colors, connectivity). Follow `drawio-layout` and the
style recipes in `drawio-author/references/style-recipes.md`. Prefer surgical
fixes over a full rewrite.

If the user asked for a ground-up redesign, use `drawio-author` instead.

## Triage first

1. **Editor false alarm?** Cursor
   `Unable to open '…drawio' — Assertion Failed` on a file the agent just wrote
   is usually not corruption. Follow `drawio-editor`: parse XML; if valid, open
   once as Text Editor. Do not "repair" valid XML for that dialog.
2. **Parse check:**
   ```bash
   python3 -c "import xml.etree.ElementTree as ET; ET.parse('PATH.drawio')"
   ```
   If parse fails, fix XML well-formedness before layout work.
3. **Classify defects** (can be several):
   - Vertex overlaps (AABB intersection)
   - Edge–vertex collisions (orthogonal segments cross boxes)
   - Stacked edges (shared horizontal/vertical segments)
   - Missing/incorrect ports or waypoints
   - Children overflowing dashed regions
   - Content past `pageWidth` / `pageHeight`
   - **Clipped text** (`align=left` without padding; box too short)
   - **Low-contrast / bare notes** (`style="text;…"` with colored font, no fill)
   - **Cramped labels** (fontSize &lt; 11 on primary nodes; missing spacing*)

## Repair procedure

### 1. Inventory

List every `vertex="1"` with `id`, approx `x,y,w,h`, style flags
(`spacingLeft`, `fontSize`, fill), and every `edge="1"` with `source`,
`target`, style, and points.

### 2. Establish or restore a layout contract

If a `LAYOUT CONTRACT` comment exists, treat it as the target lanes. If missing,
infer columns from clusters and **write the contract** before moving cells so
later edits stay consistent.

### 3. Fix typography first (cheap, high impact)

1. Replace bare `text` callouts with filled note boxes from the style recipes
   (`fillColor=#f5f5f5;fontColor=#222222;spacingLeft=14;…`).
2. On every labeled vertex, ensure
   `spacingLeft/Right≥14`, `spacingTop/Bottom≥12` (or `spacing≥12`), and
   `fontSize≥12` for phase/action nodes (`≥11` for notes/legend).
3. Grow box height to fit line count; do not drop below the font floor.
4. Process nodes: `align=center;verticalAlign=middle`. Left panels:
   `align=left` **with** spacingLeft.
5. Region titles: left + top spacing; children inset ≥40px.

### 4. Untangle vertices

1. Assign each node to a lane (spine / left / right / legend / region).
2. Reposition on the 10px grid; enforce ≥20px gaps (≥40px between columns).
3. Normalize widths within a column when nodes are the same kind (prefer
   360–380 spine width).
4. Expand dashed regions so children stay inset ≥40px; move overflow children,
   do not leave them protruding.

Preserve relative top-to-bottom order on a workflow spine unless the user asked
to reorder phases.

### 5. Untangle edges

1. Keep `source` / `target` / labels / stroke colors unless a label is wrong.
2. Reset every repaired edge to orthogonal + ports:
   `edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block` (+
   `jumpStyle=arc;jumpSize=10` when crossings remain).
3. Stagger ports on busy sides (`exitX` 0.25 / 0.5 / 0.75).
4. Assign long-haul routes to **distinct bus x or y** values from the contract,
   ≥40px apart. Parallel loops that need a horizontal collector above the same
   node get **two y values**, not one.
5. Replace coincident waypoints. Two unrelated edges must not share the same
   vertical x for overlapping y-ranges.
6. Walk every segment: if it intersects an unrelated solid vertex AABB, move the
   bus into a gutter (west of a left column, east of the spine, or a bottom y
   below all nodes).
7. Sinks reached by a drain bus: enter from TOP (or BOTTOM); exit from another
   side so the drain line does not continue through the box interior.
8. Route around regions' solid children; spine→child through a dashed region
   fill is OK.
9. Edge labels: `labelBackgroundColor=#ffffff;fontColor=#333333;fontSize=11`.

### 6. Page and legend

Grow `pageWidth` / `pageHeight` if nodes moved outward. Keep or restore a
**filled** legend if colors encode meaning.

### 7. Verify

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('PATH.drawio')"
```

Acceptance checklist:

- [ ] No overlapping sibling boxes
- [ ] No edge segment through an unrelated solid box
- [ ] No two unrelated edges sharing a corridor segment (shared drain OK)
- [ ] Parallel buses ≥40px apart
- [ ] Layout contract lists every bus x/y
- [ ] No bare canvas text notes; contrast OK on dark editor
- [ ] Padding and font floors satisfied; no clipped first characters
- [ ] Connectivity and labels unchanged (unless fixing clear typos)
- [ ] Parse succeeds

## Scope discipline

| Do | Don't |
|---|---|
| Move geometry and waypoints | Rename domain concepts without asking |
| Apply style recipes / padding | Delete nodes "to simplify" unless asked |
| Preserve cell ids when possible | Confuse editor bugs with layout repair |
| Report what was fixed in one short summary | Silent full-file rewrite when a style nudge suffices |

## When repair should escalate to author

Escalate to `drawio-author` (full redesign) when:

- More than ~half the vertices need new lanes, or
- There is no recoverable structure (random scatter with no spine/regions), or
- The user explicitly wants a new layout pattern

Say so briefly, then redesign under a fresh layout contract.
