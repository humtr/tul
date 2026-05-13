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
