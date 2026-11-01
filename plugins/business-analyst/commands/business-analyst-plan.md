---
name: business-analyst-plan
description: >-
  Lock an executable plan for ambiguous multi-step or cross-subsystem work. Uses
  business-analyst-planner. Confirm the approach by reading the repository.
---

# Plan

1. Confirm the ask is ambiguous / multi-step (not trivia or an obvious single fix).
2. Launch `business-analyst-planner` (read-only). Include the user ask and any repo paths already known.
3. If the implementation approach is unclear, read the repository and record the reversible default.
4. Launch `business-analyst-researcher` only for true external unknowns (docs/APIs outside this repo).
5. Return the locked plan: goal, in/out scope, acceptance criteria, steps, risks.
6. Do not implement until the plan is locked (or the user says to proceed without locking).
