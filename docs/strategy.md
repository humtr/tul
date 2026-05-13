# strategy

## Current strategic focus

Stage 7 is closed by establishing `tul run` as the normal user loop and making the surrounding command surface small, action-oriented, and guarded. The next strategic focus is Stage 8: hardening the gates and test harness around the now-stable user loop without expanding user-facing complexity.

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
| Full loop orchestration | High | keep `run` as the single normal loop |
| Verification evidence | High | keep `verify fresh` as uploadable evidence writer |
| Source/review transport | High | keep `export` file-creation only |
| Status/handoff | High | keep status under `show` |
| Cleanup | Medium-high | keep default plan-only under `clean` |
| Recovery | Medium-high | keep default plan-only under `recover` |
| Setup/context | Medium-high | keep status-only default under `setup` |
| Gate/test harness | Medium | harden in Stage 8 without overfitting to transient docs |
| Cross-repo onboarding | Deferred | wait until the self-host loop remains stable across several packages |

## Normal command model

```bash
tul run
```

`run` handles package-present and package-absent cases.

## Design constraints

- no broad staging;
- no force push;
- no legacy alias layer;
- warning-only export freshness unless explicitly promoted;
- source/review zip artifacts are transport artifacts, not backup authority;
- Stage 8 gate hardening should begin warning-first before promoting new checks to hard failures.
