# Current status

Latest verified stage: **Stage 5.3 — state cleanup UX**.

The current focus is `tul` development acceleration, not `/ai` onboarding. `/ai` remains **Stage X — future target onboarding**.

Recent completed stages:

- Stage 5.1: `tul verify tul` and `tul verify tul --fresh-clone`.
- Stage 5.2: package discovery polish with `tul package list/latest/inspect` and `tul update -l --dry-run`.
- Stage 5.3: state cleanup commands for no-op/imported state clutter.

Preferred update command:

```bash
tul update tul -l
```

Use `--package PATH` only when deliberately selecting an exact package.
