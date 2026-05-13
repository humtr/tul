# export integrity hardening

Status: implemented and folded into `tul show exports`.

Export integrity is a warning-only inspection surface. It reports source/review artifact states such as current, stale, missing, invalid, and unrecorded.

Canonical command:

```bash
tul show exports
```

Machine-readable form:

```bash
tul show exports --json
```

`export` itself is reserved for file creation:

```bash
tul export
tul export source
tul export review
```

Export freshness warnings do not change release-gate PASS/FAIL. Release-gate judgment remains the responsibility of `tul verify` and especially `tul verify fresh`.
