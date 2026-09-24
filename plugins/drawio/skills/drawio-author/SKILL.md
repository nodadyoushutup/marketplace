---
name: drawio-author
description: >-
  Create or redesign .drawio diagrams with intentional lanes, non-overlapping
  boxes, dedicated edge corridors, and readable padded labels. Use when writing
  a new architecture, workflow, or system graph, or when the user asks for a
  clean draw.io diagram.
---

# Drawio author

Produce diagrams that read like the framework / marketplace reference graphs:
clear columns, no piled boxes, edges on dedicated buses, **labels readable on
a dark canvas**. Follow `drawio-layout` for the hard rules; copy style strings
from [`references/style-recipes.md`](references/style-recipes.md).

## When to use

- New `.drawio` file
- Major redesign where layout should be planned from scratch
- User asks for an architecture, workflow, or dependency graph

For "boxes overlap / arrows are a mess / text is clipped or hard to read" on
an existing file, use `drawio-repair` instead.

## Procedure

### 1. Decide the shape

Pick one primary pattern before placing cells:

| Need | Pattern |
|---|---|
| Happy path + branches + side layer | Spine + left/right columns + bus lanes |
| Tiered systems (clients / runtime / data) | Swimlane regions with inset children |
| Small (<=6 nodes) flat map | Single grid row/column with ≥40px gaps |

Write the **LAYOUT CONTRACT** comment (lanes with x/y ranges) first. Do not
place nodes until the contract exists.

### 2. Place vertices

1. Snap to a 10px grid.
2. Keep comparable nodes the same width in a column (prefer 360–380 for spine).
3. Vertical rhythm on a spine: consistent gap (≈50–70px between node bottoms
   and next tops).
4. Size height to the line count (see `drawio-layout` floors). Prefer growing
   the box over shrinking the font.
5. Apply a **style recipe** from `references/style-recipes.md` — padding and
   contrast are baked in. Do not invent bare `text` callouts. Phase boxes:
   horizontal spacing only (no `spacingTop/Bottom` with `verticalAlign=middle`).
6. Regions: empty dashed frame + **title cell above**; children inset ≥40px.
   Fan-out cards sit **east of the spine**; `× N` note **below** the front card
   (never overlapping). Spine may cross region fill only.
7. Put the legend and ambient panels in filled boxes outside the flow. Keep
   notes off exclusive bus x values. Long dashed buses: use separate chip
   cells for meanings — do not rely on mid-stroke edge labels.

Suggested default sizes:

- Spine / process node: `380 × 90–120`
- Side branch node: `340 × 90–110`
- Ellipse start/end: `380 × 80`
- Side note / tier callout: filled box, not bare text
- Legend / ambient: wide enough for wrapped lines, not overlapping the spine

### 3. Route edges

1. Every edge: `edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block`.
2. Crossing edges: add `jumpStyle=arc;jumpSize=10`.
3. Labeled edges: `labelBackgroundColor=#ffffff;fontColor=#333333;fontSize=11`.
4. Prefer mid-side ports (`exitX=0.5;exitY=1` → `entryX=0.5;entryY=0` for
   downward spine links). Stagger when two edges leave/enter the same side.
5. Long-haul routes use **named exclusive buses** from the contract (fixed x
   for vertical drains, fixed y for collectors). Parallel buses ≥40px apart.
   Do not run a full-height bus through legend/ambient panels or side notes.
6. **Never** let a segment cut through an unrelated solid box. If a climb must
   pass a left-column stack, put the vertical in the gutter **west** of that
   column, then use a collector **above** the obstructing box. If climbing
   past a node above the exit (e.g. START), exit east/west first, then use a
   top runway **above all vertices**.
7. Fan-out: cards east of spine; note below front card; spine through region
   fill only (misses cards).
8. Same logical drain (many → blocked) may share one drain bus; everything else
   gets its own corridor.
9. Enter a sink like `blocked` from one side only (prefer TOP for a vertical
   drain); exit from another side so the drain does not continue through the box.
10. Prefer separate chip cells for long-bus meanings (`cannot proceed`,
    `advisory`) instead of mid-edge `value=` labels that the stroke will slice.

### 4. Color with a legend

Assign fill/stroke by role (see `drawio-layout` tokens). If you use more than
two colors, include a **filled** legend that names box and line meanings.

### 5. Verify before done

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('PATH.drawio')"
```

Checklist:

- [ ] No sibling vertex AABB overlaps (stacked fan-out cards behind a worker are OK)
- [ ] Layout contract matches actual x-ranges
- [ ] Long edges use exclusive bus waypoints; no segment through unrelated boxes
- [ ] Fan-out cards east of spine (≥40px); ×N note below front card; spine through fill only
- [ ] Parallel buses ≥40px apart (except one intentional shared drain)
- [ ] Notes / callouts do not sit on bus x values; long-bus meanings use chip cells
- [ ] Page width/height covers content + margin
- [ ] Phase boxes: no spacingTop/Bottom with verticalAlign=middle; notes/legend keep full spacing
- [ ] Region titles are separate cells above empty frames
- [ ] No bare `text` callouts with colored fonts on transparent fill
- [ ] Multi-line boxes are tall enough; left-aligned boxes have spacingLeft ≥14
- [ ] Cursor open failure on a never-opened file → `drawio-editor`, not rewrite

## Minimal skeleton

```xml
<!-- LAYOUT CONTRACT
     SPINE  x=400..780 — main path top → bottom
     LEFT   x=40..360  — branches
     BUS    x=820      — drain / loop-backs
-->
<mxfile host="app.diagrams.net" agent="cursor" version="24.0.0">
  <diagram id="example" name="Example">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1"
      tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1"
      pageWidth="1200" pageHeight="1600" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- vertices then edges; use style-recipes.md strings -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Anti-patterns

- Dumping all nodes near `(0,0)` and connecting with default edges
- Multiple edges leaving the same `exitX=0.5` without staggered ports or buses
- Routing edges through region interiors instead of around them
- Spine edge through stacked fan-out cards on the spine column
- `× N` note overlapping the front fan-out card (put it below)
- Mid-stroke labels on long dashed buses (use chip cells)
- `spacingTop`/`spacingBottom` on `verticalAlign=middle` phase boxes
- Region title inside a dashed frame that children will clip
- Notes sitting on exclusive bus x values
- Climbing vertically through a node above the exit (step sideways first)
- Skipping the layout contract "because it is a small diagram" when there are
  already crossings or side branches
- Bare `text` notes (especially blue/purple) on a dark drawio canvas
- `align=left` without `spacingLeft` (clipped first characters)
- Cramming three lines into an 80px box
- "Fixing" a Cursor assertion dialog by regenerating valid XML
