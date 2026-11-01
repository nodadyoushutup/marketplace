---
name: security-review
description: >-
  Run the security checklist on the current diff.
---

# security-review

1. Load skill `security-review`.
2. Scope to the active diff or the named paths. Do not review the whole
   repository unless asked.
3. Report must-fix findings with file paths. Fix them in the tree when the
   user asked to implement.
4. Never paste secret values into the reply.
