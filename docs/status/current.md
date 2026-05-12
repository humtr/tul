# Current status

Latest known version: `0.8.5-update-handoff-hotfix`.

Current mode: Stage 6 gate stabilization. Native context is available, package mismatch guidance is available, and update-integrated fresh verification has been installed and hotfixed.

## Current verified loop

The intended normal self-host loop is now:

```bash
tul package latest
tul update
# upload /sdcard/termux/import/tul/logs/verify/tul-vf-latest.md when review evidence is needed
```

`tul update` should print the update report first, including commit, push verification, rollback, changed files, and checks. It should then run a compact post-update `verify fresh` gate, write markdown/json verify artifacts, and print the LLM handoff.

## Current smoke package

`tul_parallel_entry_smoke_v1`

Purpose:

- prove that a normal docs-only package can be applied with one `tul update` command;
- prove that post-update `verify fresh` runs automatically after the commit/push path;
- prove that `tul-vf-latest.md` is updated to the new package commit without requiring a separate manual verify command;
- record the canonical verify artifact layout decision before parallel bundles resume.

## Verify artifact convention

Canonical latest files remain directly under the verify log root:

```text
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.md
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.json
```

Timestamped run artifacts should move to date folders directly under the verify log root:

```text
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-152110-9dae1b4.md
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-152110-9dae1b4.json
```

Do not continue writing both `tul-vf-latest.*` and `tul-verify-latest.*`. `tul-vf-latest.md/json` are the canonical latest artifacts.

## Parallel entry condition

Parallel Stage 6 bundles may start after this smoke package passes with one `tul update` command and the uploaded latest verify artifact points at the smoke commit.

## Next after smoke

First bounded parallel bundle:

`tul_stage6_compact_gate_bundle_v1`

Candidate scope:

- canonical verify log layout implementation;
- release-gate summary polish;
- compact state output;
- docs/status/roadmap/checklist consistency update.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.
