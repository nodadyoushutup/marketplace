---
name: business-analyst-plan
description: >-
  Lock a product-sequence plan for ambiguous multi-step or cross-subsystem
  work. Uses business-analyst-planner. Technical approach belongs to
  code-technical-lead.
---

# Plan

1. If `business-analyst-when` stay-out matches, implement immediately — do
   not lock a plan.
2. Launch / follow `business-analyst-planner` (read-only). Include the user
   ask and any repo paths already known.
3. Launch `business-analyst-researcher` only for true external unknowns
   (docs/APIs outside this repo).
4. Return the locked plan: goal, in/out scope, assumptions, acceptance
   criteria, product sequence, risks.
5. Name technical approach as a later pass when the build path is
   unclear. Do not pick libraries or file touch points in this command.
6. If the user asked to proceed without locking, or stay-out now matches,
   implement. Otherwise stop at the lock until the parent continues.
