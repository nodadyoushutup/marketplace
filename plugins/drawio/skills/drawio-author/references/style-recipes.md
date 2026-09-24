# Drawio style recipes

Copy these `style=` strings verbatim (then add role colors if needed). They
encode the typography / padding floor from `drawio-layout`.

## Process / phase node (spine)

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=12;fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#12305B
```

Min size: width 360–380; height 90 (2 lines) / 110 (3 lines) / 120+ (4 lines).

## Side branch node

Same as phase node (same padding). Width often 320–340.

## Success / finish

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=12;fillColor=#d5e8d4;strokeColor=#82b366;fontColor=#12401A
```

## Warn / repair

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=12;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#6B4E00
```

## Danger / blocked

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=12;fillColor=#f8cecc;strokeColor=#b85450;fontColor=#6E1B18
```

## Neutral / pause

```
rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=12;fillColor=#e0e0e0;strokeColor=#666666;fontColor=#222222
```

## Start / end ellipse

```
ellipse;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacing=12;fontSize=13;fontStyle=1;fillColor=#e0e0e0;strokeColor=#666666;fontColor=#222222
```

Height ≥80 so the label is not vertically cramped.

## Side note / tier callout / stack caption

**Always a filled box** — never bare `text` on the canvas:

```
rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=11;fillColor=#f5f5f5;strokeColor=#bbbbbb;fontColor=#222222
```

## Legend / ambient panel

```
rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=11;fillColor=#f5f5f5;strokeColor=#bbbbbb;fontColor=#222222
```

Ambient (dashed):

```
rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 8;align=left;verticalAlign=top;spacingLeft=14;spacingRight=14;spacingTop=12;spacingBottom=12;fontSize=11;fontStyle=1;fillColor=#eeeeee;strokeColor=#999999;strokeWidth=2;fontColor=#333333
```

## Dashed region (fan-out / layer)

```
rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 8;align=left;verticalAlign=top;spacingLeft=16;spacingTop=12;spacingRight=16;fontSize=12;fontStyle=1;fillColor=#e1d5e7;strokeColor=#9673a6;strokeWidth=2;fontColor=#4B286D
```

Children: inset ≥40px from region edges. Left-aligned child content needs
`spacingLeft=14` (same as process nodes).

Orange enforcement / subagent region: swap fill/stroke/font to
`#ffe6cc` / `#d79b00` / `#7A3B00`.

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
| `style="text;…;fontColor=#12305B"` with no fill | Invisible on dark drawio canvas |
| `align=left` without `spacingLeft≥12` | Clips first characters |
| `fontSize=10` on phase boxes | Too small in the editor |
| 3-line copy in an 80px-tall box | Cramped / overflow |
| Region `align=right` + cramped children | Title fights content; prefer left title + inset children |
| Long-haul edge waypoints inside another box's AABB | Line appears to stab through the node |
| Two loops sharing one collector y above a busy node | Stacked arrows; use two y values ≥30px apart |
| Full-height bus x through legend/ambient panels | Lines slice the chrome |
| Drain bus continuing horizontally through `blocked` | Enter from top/bottom; exit the other side |
