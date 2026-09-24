---
name: drawio-triage
description: >-
  Triage a Cursor .drawio open failure before assuming the diagram XML is broken.
---

# Drawio triage

1. Follow `drawio-editor`: parse the XML first.
2. If XML is valid, treat it as the Cursor custom-editor false alarm — open once with Text Editor, then reopen normally.
3. Do not "repair" valid diagram XML in response to the assertion dialog.
