# Drawio style recipes

Copy these `style=` strings verbatim (then add role colors if needed). They
encode the typography / padding floor from `drawio-layout`.

## Process / phase node (spine)

**Do not** add `spacingTop` / `spacingBottom` here. With
`verticalAlign=middle`, those paddings fight centering in Cursor's drawio and
jam multi-line text toward the top (or clip the bottom line). Horizontal
spacing only — grow the box height for vertical room.

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=12;spacingRight=12;fontSize=12;fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#12305B
```

Min size: width 360–380; height 90 (2 lines) / 110 (3 lines) / 120+ (4 lines).

## Side branch node

Same as phase node (same padding). Width often 320–340.

## Success / finish

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=12;spacingRight=12;fontSize=12;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#12401A
```

## Warn / repair

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=12;spacingRight=12;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#6B4E00
```

## Danger / blocked

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=12;spacingRight=12;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;fontColor=#6E1B18
```

## Neutral / pause

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=12;spacingRight=12;fontSize=12;fillColor=#e0e0e0;strokeColor=#666666;fontColor=#222222
```

## Start / end ellipse

```
ellipse;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=13;fontStyle=1;fillColor=#e0e0e0;strokeColor=#666666;fontColor=#222222
```

Height ≥80 so the label is not vertically cramped. Skip `spacingTop/Bottom`
here too when using `verticalAlign=middle`.

## Side note / tier callout / stack caption

**Always a filled box** — never bare `text` on the canvas. Notes may use
`spacingTop/Bottom` because they are left+middle with short copy; keep them
**off exclusive bus x/y** values.

```
rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;spacingLeft=14;spacingRight=14;spacingTop=10;spacingBottom=10;fontSize=11;fillColor=#f5f5f5;strokeColor=#bbbbbb;fontColor=#222222
```

## Meaning chip (branch / bus label)

Use instead of mid-stroke `value=` on long or dashed edges. **Placement:**
east or west of the spine centerline in inter-node gaps; never on the vertical
spine edge x; never covering an exclusive bus x/y.

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=10;spacingRight=10;fontSize=11;fillColor=#f5f5f5;strokeColor=#bbbbbb;fontColor=#222222
```

Typical size: width 50–160; height 28.

## Legend / ambient panel

```
rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=11;fillColor=#f5f5f5;strokeColor=#bbbbbb;fontColor=#222222
```

Ambient (dashed):

```
rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 8;align=left;verticalAlign=top;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=11;fontStyle=1;fillColor=#eeeeee;strokeColor=#999999;strokeWidth=2;fontColor=#333333
```

## Dashed region (fan-out / layer)

Prefer an **empty** dashed frame (`value=""`) plus a **separate title cell
above** it. Putting the title inside the region fights children and clips.

Region frame (empty value):

```
rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 8;fillColor=#e1d5e7;strokeColor=#9673a6;strokeWidth=2;opacity=80
```

Title chip (place ≥10px above the frame):

```
text;html=1;align=left;verticalAlign=middle;fontSize=12;fontStyle=1;fontColor=#4B286D;labelBackgroundColor=#e1d5e7
```

Children: inset ≥40px from region edges. Left-aligned child content needs
`spacingLeft=14` (and **no** `spacingTop/Bottom` when `verticalAlign=middle`).

**Fan-out stack placement (required):**
1. Front worker + opacity stack cards sit **east of the spine** (≥40px clear of
   the spine column’s right edge). The spine may cross the dashed region *fill*
   only — it must miss the cards.
2. The `× N …` note sits **directly below** the front card (same x, ≥20px gap),
   never beside it in a slot that overlaps the card AABB.
3. Uniform stack offsets (e.g. back +20/+20, mid +10/+10) — not random.

Orange enforcement / subagent region: swap fill/stroke to `#ffe6cc` /
`#d79b00`, and title font/`labelBackgroundColor` to `#7A3B00` / `#ffe6cc`.
Subagent children: equal gaps, equal insets, no `spacingTop/Bottom`.

## Edge (orthogonal)

```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;jumpStyle=arc;jumpSize=10
```

Labeled:

```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;jumpStyle=arc;jumpSize=10;labelBackgroundColor=#ffffff;fontSize=11;fontColor=#333333
```

## Forbidden

| Anti-pattern | Why |
|---|---|
| `style="text;…;fontColor=#12305B"` with no fill | Invisible on dark drawio canvas (region *titles* with `labelBackgroundColor` are the exception) |
| `spacingTop`/`spacingBottom` on `verticalAlign=middle` phase boxes | Text sinks / clips in Cursor's drawio |
| `align=left` without `spacingLeft≥12` | Clips first characters |
| `fontSize=10` on phase boxes | Too small in the editor |
| 3-line copy in an 80px-tall box | Cramped / overflow |
| Region title *inside* a dashed frame with children | Title clips under children; use a separate cell above |
| Spine edge through stacked fan-out cards | Looks like the line stabs the stack; put cards east of spine |
| `× N` note beside / overlapping the front fan-out card | Guaranteed AABB overlap; put the note **below** the card |
| Mid-stroke labels on long dashed buses | Stroke slices the label; use a separate chip cell beside the bus |
| Chip on spine centerline between phase boxes | Spine edge paints through the chip; offset east/west |
| Chip AABB covering a climb/drain bus x | Same as sitting on a bus — move the chip or the bus |
| Note / callout sitting on an exclusive bus x | Drain/advisory line cuts the note |
| East horizontal from spine through a right-column stack | y intersects status children; climb the west gutter instead |
| Two different purposes sharing one east bus | Stacked arrows; e.g. create→backlog ≠ progress→blocked |
| Climb that goes vertically through a node above the exit | Exit east/west of the obstructing AABB first, then use a top runway |
| Long-haul edge waypoints inside another box's AABB | Line appears to stab through the node |
| Two loops sharing one collector y above a busy node | Stacked arrows; use two y values ≥30px apart |
| Full-height bus x through legend/ambient panels | Lines slice the chrome; panel right edge ≤ bus_x − 40 |
| Drain bus continuing horizontally through `blocked` | Enter from top/bottom; exit the other side |
