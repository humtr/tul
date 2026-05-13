# strategy

## Current strategic focus

Stage 7 focuses on reducing user bridge work while preserving user control over approval, risk, rollback, and source attribution.

The command surface is intentionally small:

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

## Capability map

| Area | Maturity | Current direction |
|---|---|---|
| Package application | High | keep `update` focused on apply/check/commit/push/remote-head |
| Full loop orchestration | Medium-high | make `run` the single normal loop |
| Verification evidence | High | keep `verify fresh` as uploadable evidence writer |
| Source/review transport | High | keep `export` file-creation only |
| Status/handoff | Medium-high | keep status under `show` |
| Cleanup | Medium | keep default plan-only under `clean` |
| Recovery | Medium | keep default plan-only under `recover` |
| Setup/context | Medium | consolidate under `setup` |
| Cross-repo onboarding | Deferred | wait until self-host loop is stable |

## Normal command model

```bash
tul run
```

`run` handles package-present and package-absent cases.

## Design constraints

- no broad staging;
- no force push;
- no legacy alias layer;
- warning-only export freshness until explicitly promoted;
- source/review zip artifacts are transport artifacts, not backup authority.
