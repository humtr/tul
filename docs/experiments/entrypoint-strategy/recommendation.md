> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# Entrypoint strategy recommendation

Result: **Adopt Option 2 — README brief + dedicated handoff**.

The user-verified test commit showed:

- Option 1: 74 lines, required-term score 6/7, missing `roadmap`.
- Option 2: 66 lines, required-term score 7/7, missing none.
- Option 3: 106 lines, required-term score 7/7, missing none.

Option 2 is the production strategy because it keeps README small enough for first contact while preserving durable status, roadmap, checklist, command grammar, and project instructions in dedicated repo documents.

Production adoption adds an explicit newest-package command form:

```bash
tul update <project> --latest
# or
tul update <project> -l
```

This scans configured inbox roots and selects the newest matching package by manifest target.
