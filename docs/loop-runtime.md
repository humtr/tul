> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# loop runtime

The normal full-loop command is:

```bash
tul run
```

`run` applies a compatible package when one is available. If no package is available, it refreshes current verification and transport artifacts.

Stepwise diagnostics:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```
