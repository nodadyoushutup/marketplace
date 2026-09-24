---
name: drawio-repair
description: >-
  Repair messy .drawio diagrams: overlapping boxes, stacked arrow paths, edges
  through nodes, and broken orthogonal routing. Use when an existing diagram is
  hard to read or the user asks to clean up / fix layout without changing
  meaning.
---

# Drawio repair

Fix layout defects in an existing `.drawio` while preserving meaning (ids,
labels, colors, connectivity). Follow `drawio-layout`. Prefer surgical
repositioning and re-routing over a full rewrite.

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

## Repair procedure

### 1. Inventory

List every `vertex="1"` with `id`, approx `x,y,w,h`, and every `edge="1"` with
`source`, `target`, style, and points. Keep a short table in working notes.

### 2. Establish or restore a layout contract

If a `LAYOUT CONTRACT` comment exists, treat it as the target lanes. If missing,
infer columns from clusters and **write the contract** before moving cells so
later edits stay consistent.

### 3. Untangle vertices

1. Assign each node to a lane (spine / left / right / legend / region).
2. Reposition on the 10px grid; enforce ≥20px gaps (≥40px between columns).
3. Normalize widths within a column when nodes are the same kind.
4. Expand dashed regions so children stay inset ≥30px; move overflow children,
   do not leave them protruding.

Preserve relative top-to-bottom order on a workflow spine unless the user asked
to reorder phases.

### 4. Untangle edges

1. Keep `source` / `target` / labels / stroke colors unless a label is wrong.
2. Reset every repaired edge to orthogonal + ports:
   `edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block` (+
   `jumpStyle=arc;jumpSize=10` when crossings remain).
3. Stagger ports on busy sides (`exitX` 0.25 / 0.5 / 0.75).
4. Assign long-haul routes to **distinct bus x or y** values from the contract.
   Parallel buses ≥20px apart.
5. Replace accidental coincident waypoints: two edges must not share the same
   `(x)` vertical run for overlapping y-ranges unless intentional.
6. Route around regions; do not clip through unrelated boxes.

### 5. Page and legend

Grow `pageWidth` / `pageHeight` if nodes moved outward. Keep or restore a
legend if colors encode meaning.

### 6. Verify

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('PATH.drawio')"
```

Acceptance checklist:

- [ ] No overlapping boxes
- [ ] No two edges sharing the same corridor segment
- [ ] Edges do not cut through unrelated vertices
- [ ] Layout contract matches geometry
- [ ] Connectivity and labels unchanged (unless fixing clear typos)
- [ ] Parse succeeds

## Scope discipline

| Do | Don't |
|---|---|
| Move geometry and waypoints | Rename domain concepts without asking |
| Add buses and ports | Delete nodes "to simplify" unless asked |
| Preserve cell ids when possible | Confuse editor bugs with layout repair |
| Report what was fixed in one short summary | Silent full-file rewrite when a corridor nudge suffices |

## When repair should escalate to author

Escalate to `drawio-author` (full redesign) when:

- More than ~half the vertices need new lanes, or
- There is no recoverable structure (random scatter with no spine/regions), or
- The user explicitly wants a new layout pattern

Say so briefly, then redesign under a fresh layout contract.
