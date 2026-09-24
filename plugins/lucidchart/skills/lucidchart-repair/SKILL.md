---
name: lucidchart-repair
description: >-
  Repair messy Lucidchart Standard Import JSON (*.lucid.json): overlapping
  boxes, stacked elbow paths, clipped labels, and edges through nodes. Use when
  an existing Lucid import diagram is hard to read or the user asks to clean up
  layout without changing meaning.
---

# Lucidchart repair

Fix layout and readability defects in an existing `*.lucid.json` while
preserving meaning (ids, labels, colors, connectivity). Follow
`lucidchart-layout` and
`lucidchart-author/references/style-recipes.md`. Prefer surgical fixes over a
full rewrite.

If the user asked for a ground-up redesign, use `lucidchart-author` instead.

**Important:** Lucid Standard Import cannot patch a live board. After repair,
re-package and create a **new** document (`lucidchart-package`).

## Triage first

1. **JSON parse:**

```bash
python3 -c "import json; json.load(open('PATH.lucid.json'))"
```

2. **Classify defects** (can be several):
   - Shape AABB overlaps
   - Line–shape collisions (elbow segments / control points in boxes)
   - Line–chip collisions (spine centerline chips; chips on bus x)
   - Stacked elbows (shared corridors — including two purposes on one east bus)
   - East horizontal through a right-column stack
   - West skip/drain through legend/ambient
   - Missing ports or bad elbow angles (not 90°)
   - Children overflowing containers (inset < 40px)
   - Low-contrast / unfilled notes; cramped labels

## Repair procedure

### 1. Inventory

List every shape (`id`, boundingBox, type, style) and every line (`id`,
endpoints, stroke, elbowControlPoints / joints).

### 2. Restore the layout contract

Keep or rewrite `__layoutContract__` before moving geometry.

### 3. Typography

Filled notes/legend/chips only; font floors; grow height for line count;
region titles above empty containers; children inset ≥40px.

### 4. Untangle shapes

Assign lanes; snap to 10px grid; ≥20px gaps (≥40px between columns); move chips
off spine centerline and buses; narrow legend/ambient so they clear the west
drain.

### 5. Untangle lines

1. Keep source/target / stroke colors unless wrong.
2. Reset long routes to `elbow` + explicit shapeEndpoint positions.
3. Distinct buses ≥40px apart; split shared east buses when purposes differ.
4. Walk every segment (endpoint → control points → endpoint) against solid +
   chip AABBs.
5. Spine → right stack: west gutter climb; enter from the left.
6. Prefer chips over mid-line text on long dashed elbows.

### 6. Verify and re-package

```bash
python3 -c "import json; json.load(open('PATH.lucid.json'))"
python3 plugins/lucidchart/skills/lucidchart-author/scripts/package_lucid.py PATH.lucid.json
```

Acceptance checklist: same geometry bar as `lucidchart-author` verify list;
connectivity unchanged unless fixing clear typos; package succeeds.

## Scope discipline

| Do | Don't |
|---|---|
| Move bounding boxes and elbow points | Rename domain concepts without asking |
| Apply style recipes | Claim in-place Lucid API edits |
| Preserve ids when possible | Silent full rewrite when a corridor fix suffices |
| Report what was fixed briefly | Confuse API 400 with layout craft |

## Escalate to author

Escalate when more than ~half the shapes need new lanes, structure is
unrecoverable, or the user wants a new layout pattern.
