---
name: security
description: >-
  Apply this plugin's security practices to the current change.
---

# security

1. Load skill `security`.
2. Apply the rule that matches the sink in the diff.
3. When the change crosses a trust boundary, also run `security-review`.
4. Never paste secret values into the reply.
