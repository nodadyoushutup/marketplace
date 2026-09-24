# Lucidchart Standard Import style recipes

Copy these shape / line objects (adjust `id`, `boundingBox`, `text`). They
encode the layout floor from `lucidchart-layout`. Geometry units: prefer
`"documentSettings": { "units": "px" }`.

Bounding box:

```json
{ "x": 780, "y": 160, "w": 380, "h": 110 }
```

## Shared style helpers

Fill + stroke (swap colors per role table in `lucidchart-layout`):

```json
{
  "fill": { "type": "color", "color": "#dae8fc" },
  "stroke": { "color": "#6c8ebf", "width": 1.5, "style": "solid" },
  "rounding": 10
}
```

Dashed stroke: `"style": "dash"`. Soft region: lower opacity on the shape
(`"opacity": 80`) plus dashed stroke.

## Process / phase (spine)

`type`: `process` (flowchart) or `rectangle` (shape library).

```json
{
  "id": "gate",
  "type": "process",
  "boundingBox": { "x": 780, "y": 160, "w": 380, "h": 110 },
  "style": {
    "fill": { "type": "color", "color": "#dae8fc" },
    "stroke": { "color": "#6c8ebf", "width": 1.5, "style": "solid" },
    "rounding": 10
  },
  "text": "gate · tracker work?\nexplicit create / manage / transition"
}
```

Min size: w 360–380; h 90 (2 lines) / 110 (3) / 120+ (4).

## Success / finish

```json
{
  "type": "process",
  "style": {
    "fill": { "type": "color", "color": "#d5e8d4" },
    "stroke": { "color": "#82b366", "width": 1.5, "style": "solid" },
    "rounding": 10
  }
}
```

## Warn

```json
{
  "type": "process",
  "style": {
    "fill": { "type": "color", "color": "#fff2cc" },
    "stroke": { "color": "#d6b656", "width": 1.5, "style": "solid" },
    "rounding": 10
  }
}
```

## Danger / blocked

```json
{
  "type": "process",
  "style": {
    "fill": { "type": "color", "color": "#f8cecc" },
    "stroke": { "color": "#b85450", "width": 1.5, "style": "solid" },
    "rounding": 10
  }
}
```

## Neutral / pause

```json
{
  "type": "process",
  "style": {
    "fill": { "type": "color", "color": "#e0e0e0" },
    "stroke": { "color": "#666666", "width": 1.5, "style": "solid" },
    "rounding": 10
  }
}
```

## Start / end terminator

```json
{
  "id": "start",
  "type": "terminator",
  "boundingBox": { "x": 780, "y": 40, "w": 380, "h": 80 },
  "style": {
    "fill": { "type": "color", "color": "#e0e0e0" },
    "stroke": { "color": "#666666", "width": 1.5, "style": "solid" }
  },
  "text": "START — user ask"
}
```

Height ≥80.

## Side note / legend / chip

Filled `rectangle` (never bare text-only floating labels without a fill).

```json
{
  "id": "chip_yes",
  "type": "rectangle",
  "boundingBox": { "x": 1080, "y": 278, "w": 50, "h": 28 },
  "style": {
    "fill": { "type": "color", "color": "#f5f5f5" },
    "stroke": { "color": "#bbbbbb", "width": 1, "style": "solid" },
    "rounding": 6
  },
  "text": "yes"
}
```

Chips: off spine centerline; off exclusive bus x/y.

Legend / ambient: larger `rectangle` or `note`, left-aligned multi-line text,
placed outside the spine. Ambient may use dashed stroke.

## Region (dashed container)

Empty `roundedRectangleContainer` + title `rectangle` **above** it. Children
inset ≥40px. Fan-out cards east of spine; `× N` note below front card.

```json
{
  "id": "status_region",
  "type": "roundedRectangleContainer",
  "boundingBox": { "x": 1260, "y": 325, "w": 380, "h": 640 },
  "style": {
    "fill": { "type": "color", "color": "#ffe6cc" },
    "stroke": { "color": "#d79b00", "width": 2, "style": "dash" }
  },
  "opacity": 80,
  "magnetize": true,
  "containerTitle": { "text": "" }
}
```

Title shape above the frame (separate id), not only `containerTitle`, when the
title must clear children.

## Elbow line (orthogonal)

```json
{
  "id": "e_gate_intent",
  "lineType": "elbow",
  "endpoint1": {
    "type": "shapeEndpoint",
    "style": "none",
    "shapeId": "gate",
    "position": { "x": 0.5, "y": 1 }
  },
  "endpoint2": {
    "type": "shapeEndpoint",
    "style": "arrow",
    "shapeId": "intent",
    "position": { "x": 0.5, "y": 0 }
  },
  "stroke": { "color": "#000000", "width": 1.5, "style": "solid" },
  "elbowControlPoints": []
}
```

Long-haul bus (west gutter climb example):

```json
{
  "id": "e_create_backlog",
  "lineType": "elbow",
  "endpoint1": {
    "type": "shapeEndpoint",
    "style": "none",
    "shapeId": "create",
    "position": { "x": 1, "y": 0.25 }
  },
  "endpoint2": {
    "type": "shapeEndpoint",
    "style": "arrow",
    "shapeId": "st_backlog",
    "position": { "x": 0, "y": 0.65 }
  },
  "stroke": { "color": "#d6b656", "width": 1.5, "style": "dash" },
  "elbowControlPoints": [
    { "x": 1230, "y": 787 },
    { "x": 1230, "y": 417 }
  ]
}
```

Prefer chips over mid-line `text` on long dashed elbows. If line text remains,
keep it short and `side: "middle"`.

## Minimal document skeleton

```json
{
  "__layoutContract__": "SPINE x=780..1160; LEFT x=400..720; BUSES x=350 skip→END",
  "version": 1,
  "documentSettings": { "units": "px" },
  "pages": [
    {
      "id": "page1",
      "title": "Workflow",
      "shapes": [],
      "lines": []
    }
  ]
}
```

## Forbidden

| Anti-pattern | Why |
|---|---|
| Bare unfilled callouts | Low contrast / invisible |
| Chip on spine centerline | Elbow paints through the chip |
| Chip covering a climb bus x | Same as sitting on a bus |
| East horizontal through a right-column stack | Stabs status children |
| Two purposes sharing one east bus | Stacked arrows |
| Elbow control points inside unrelated AABBs | Line stabs the node |
| Full-height skip drain through legend/ambient | Slices chrome |
| Claiming SI can edit an existing Lucid doc | API creates new docs only |
| Shipping `__layoutContract__` inside the zip | Strip on package |
