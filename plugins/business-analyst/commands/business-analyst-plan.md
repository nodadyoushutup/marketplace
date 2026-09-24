---
name: business-analyst-plan
description: >-
  Lock an executable plan for L3 or ambiguous multi-step work. Uses
  business-analyst-planner with code-technical-lead when the code plugin is
  installed.
---

# Plan

1. Load `global-change-intensity` — confirm this is L3 / blocked L2 (not L0/L1).
2. Launch `business-analyst-planner` (read-only). Include the user ask and any repo paths already known.
3. If implementation approach is unclear and the `code` plugin is installed, launch `code-technical-lead` in parallel.
4. Launch `business-analyst-researcher` only for true external unknowns (docs/APIs outside this repo).
5. Return the locked plan: goal, in/out scope, acceptance criteria, steps, risks.
6. Do not implement until the plan is locked (or the user says to proceed without locking).
