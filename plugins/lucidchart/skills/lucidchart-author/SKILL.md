---
name: lucidchart-author
description: >-
  Create or redesign Lucidchart diagrams as Lucid Standard Import JSON
  (*.lucid.json) with intentional lanes, non-overlapping boxes, dedicated edge
  corridors, and readable labels. Use when writing a new Lucidchart architecture,
  workflow, or system graph, or when the user asks for a clean Lucid diagram.
---

# Lucidchart author

Produce diagrams with the same craft as `drawio-author`, serialized as Lucid
**Standard Import** JSON. Follow `lucidchart-layout` for hard rules; copy shape
and line objects from
[`references/style-recipes.md`](references/style-recipes.md).

## When to use

- New `*.lucid.json` (or package to `.lucid` for import)
- Major redesign where layout should be planned from scratch
- User asks for a Lucidchart / Lucid architecture or workflow diagram

For overlaps / stacked elbows / edge-through-box on existing JSON, use
`lucidchart-repair`. For zip + API/UI import, use `lucidchart-package`.

## Procedure

### 1. Decide the shape

| Need | Pattern |
|---|---|
| Happy path + branches + side layer | Spine + left/right columns + bus lanes |
| Tiered systems | `roundedRectangleContainer` regions with inset children |
| Small (≤6 nodes) flat map | Single grid with ≥40px gaps |

Write `__layoutContract__` first. Do not place shapes until the contract exists.

### 2. Place shapes

1. Snap `boundingBox` to a 10px grid; `documentSettings.units: "px"`.
2. Comparable spine nodes share width (prefer 360–380).
3. Vertical rhythm: consistent gap (~40–70px) between node bottoms and next tops.
4. Size height to line count (see `lucidchart-layout` floors).
5. Apply a style recipe — filled shapes only; role colors from the layout table.
6. Regions: empty container + title shape **above**; children inset ≥40px.
   Fan-out cards **east of the spine**; `× N` note **below** the front card.
7. Legend / ambient / chips outside the spine; chips off centerline and buses.

Suggested sizes: spine `380×90–120`; side `340×90–110`; terminator `380×80`;
chips `50–160×28`.

### 3. Route lines

1. Prefer `lineType: "elbow"` with 90° `elbowControlPoints` on named buses.
2. Explicit `shapeEndpoint` positions; stagger busy sides.
3. Long-haul routes: exclusive bus x/y, ≥40px apart; panel right edge ≤ west
   bus − 40.
4. Never cut through unrelated solid AABBs. Spine → right stack: **west gutter
   climb**, enter from the left — no east horizontal through the stack.
5. Same logical drain may share a bus; different purposes get their own
   (create→backlog ≠ progress→blocked).
6. Prefer chips over mid-line text on long dashed elbows.

### 4. Color with a legend

If more than two role colors, include a filled legend shape naming box and line
meanings.

### 5. Verify and package

```bash
python3 -c "import json; json.load(open('PATH.lucid.json'))"
python3 plugins/lucidchart/skills/lucidchart-author/scripts/package_lucid.py PATH.lucid.json
```

Checklist:

- [ ] No sibling AABB overlaps
- [ ] `__layoutContract__` matches actual x-ranges
- [ ] Elbows on exclusive buses; no segment through unrelated boxes/chips
- [ ] No east horizontal through a right-column stack
- [ ] Fan-out cards east of spine; ×N note below front card
- [ ] Parallel buses ≥40px apart (except one intentional shared drain)
- [ ] Different purposes do not share a bus
- [ ] Chips off spine centerline and off buses
- [ ] Legend/ambient clear the west skip/drain bus by ≥40px
- [ ] Unique ids across pages/shapes/lines
- [ ] Package strips `__layoutContract__`; zip contains `document.json`

Import creates a **new** Lucid document — see `lucidchart-package`.

## Anti-patterns

- Dumping shapes near `(0,0)` with smart lines and no buses
- Chip on spine centerline or covering a climb bus
- East horizontal through a status stack
- Two purposes sharing one east bus
- Elbow control points inside unrelated AABBs
- Skip drain through legend/ambient
- Claiming the API can edit an existing board in place
- Leaving `__layoutContract__` inside the shipped zip
