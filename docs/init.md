> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# tul init

`tul init <id|repo|path>` registers a repository for the loop.

It may:

- clone a GitHub slug when a local repo does not exist
- register or update a project alias in global config
- create `.tul.yml` when missing
- print an initial-review handoff with `--handoff`

It must not silently delete existing config values.
