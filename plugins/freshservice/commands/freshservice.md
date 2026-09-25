---
name: freshservice
description: >-
  File or manage Freshservice tickets with create-only gates and honest status.
---

# /freshservice

1. If the user did not authorize Freshservice/ticket work and named no ticket,
   say so and stop.
2. Otherwise load `freshservice` and follow `freshservice-create`,
   `freshservice-ticket`, or `freshservice-status`.
3. Prefer Freshservice MCP. Never invent workspace or ticket ids.
4. Return ticket id / URL with evidence.
