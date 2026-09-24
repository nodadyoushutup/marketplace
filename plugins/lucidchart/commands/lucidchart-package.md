---
name: lucidchart-package
description: >-
  Package *.lucid.json into a .lucid zip and create a new Lucidchart document
  via API or UI import.
---

# Lucidchart package

1. Follow `lucidchart-package`: validate JSON, run
   `lucidchart-author/scripts/package_lucid.py`.
2. Create a **new** Lucidchart document (API or UI). Do not claim in-place edits.
3. Prefer a ready Lucid MCP when connected (`global-mcp-first`); else curl form
   upload per the package rule.
4. On API 400/415, triage schema / content-type — do not “repair layout” blindly.
