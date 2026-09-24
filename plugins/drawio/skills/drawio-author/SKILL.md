---
name: drawio-author
description: >-
  Create or redesign .drawio diagrams with intentional lanes, non-overlapping
  boxes, and dedicated edge corridors. Use when writing a new architecture,
  workflow, or system graph, or when the user asks for a clean draw.io diagram.
---

# Drawio author

Produce diagrams that read like the framework reference graphs: clear columns,
no piled boxes, edges on dedicated buses. Follow `drawio-layout` for the hard
rules; this skill is the procedure.

## When to use

- New `.drawio` file
- Major redesign where layout should be planned from scratch
- User asks for an architecture, workflow, or dependency graph

For "boxes overlap / arrows are a mess" on an existing file, use
`drawio-repair` instead.

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
2. Keep comparable nodes the same width in a column.
3. Vertical rhythm on a spine: consistent gap (≈60–80px between node bottoms
   and next tops).
4. Regions: dashed container first, then children inset ≥30px; region label via
   `verticalAlign=top;align=left` (or right) with spacing.
5. Put the legend outside the flow (corner or below).

Suggested default sizes:

- Spine / process node: `340 × 80–110`
- Side branch node: `320 × 80–90`
- Ellipse start/end: `340 × 70`
- Legend text box: wide enough for wrapped lines, not overlapping the spine

### 3. Route edges

1. Every edge: `edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block`.
2. Crossing edges: add `jumpStyle=arc;jumpSize=10`.
3. Labeled edges: `labelBackgroundColor=#ffffff`.
4. Prefer mid-side ports (`exitX=0.5;exitY=1` → `entryX=0.5;entryY=0` for
   downward spine links).
5. Long-haul or fan-in routes share a **named bus** from the contract
   (fixed x for vertical drains, fixed y for horizontal collectors). Put
   waypoints on that bus only.
6. Never let two edges share the same bus segment in the same direction unless
   they are intentionally the same logical cable (rare — prefer separate
   staggered lanes 20–40px apart).

### 4. Color with a legend

Assign fill/stroke by role (see `drawio-layout` tokens). If you use more than
two colors, include a legend that names box and line meanings.

### 5. Verify before done

```bash
python3 -c "import xml.etree.ElementTree as ET; ET.parse('PATH.drawio')"
```

Mentally (or with a quick geometry pass) confirm:

- [ ] No vertex AABB overlaps
- [ ] Layout contract matches actual x-ranges
- [ ] Long edges use bus waypoints, not diagonal shortcuts through boxes
- [ ] Page width/height covers content + margin
- [ ] Cursor open failure on a never-opened file → `drawio-editor`, not rewrite

## Minimal skeleton

```xml
<!-- LAYOUT CONTRACT
     SPINE  x=400..740 — main path top → bottom
     LEFT   x=40..360  — branches
     BUS    x=780      — drain / loop-backs
-->
<mxfile host="app.diagrams.net" agent="cursor" version="24.0.0">
  <diagram id="example" name="Example">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1"
      tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1"
      pageWidth="1200" pageHeight="1600" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- vertices then edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Anti-patterns

- Dumping all nodes near `(0,0)` and connecting with default edges
- Multiple edges leaving the same `exitX=0.5` without staggered ports or buses
- Routing edges through region interiors instead of around them
- Skipping the layout contract "because it is a small diagram" when there are
  already crossings or side branches
- "Fixing" a Cursor assertion dialog by regenerating valid XML
