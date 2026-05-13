# post-update export automation

Post-update export automation was introduced before the final Stage 7 command surface split.

The final user-facing orchestration is:

```bash
tul run
```

`run` owns export and fresh verification after an update, or refreshes artifacts when no package is available.

`update` should remain focused on package application, commit, push, and remote HEAD verification.

Export failures are warning-only unless a later release-gate decision changes that policy.
