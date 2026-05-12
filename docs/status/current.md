# Current status

Latest known version: `0.8.29-stage7-post-export`.

Current mode: Stage 7 post-update export automation. Stage 6 is closed. Stage 7 planning consolidation, terminology audit, source spec/gates, explicit source export implementation, and export integrity hardening are closed. The current task is to automate source/review export after successful updates while keeping export failures warning-only and separate from commit/push/rollback facts.

## Verified baseline

Latest verified baseline from the current `tul-vf-latest.md` artifact:

```text
HEAD: 2bd72e4eedbc6753083d12ea7c4eac73e7691ba3
Remote HEAD: 2bd72e4eedbc6753083d12ea7c4eac73e7691ba3
Release gate: PASS
Steps: 25 pass, 0 fail
Working tree: clean
Fresh clone verify: PASS
Latest package: tul-stage7-export-integrity-hardening-bundle-v1
Export status: warning-only diagnostics available
```

Canonical latest artifacts:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-source-latest.zip
/sdcard/termux/import/tul/tul-review-latest.zip
```

When a newer `tul-vf-latest.md` is provided by the user, treat it as the runtime source of truth over this document.

## Closed checkpoints

- Stage 6 stabilization checkpoint — PASS at `5086c982ae5d52c586049d4fb21c8e7d4ada006d`.
- Stage 7 planning consolidation — PASS at `79d27fb07ce52666acb603b714dab33a45079e19`.
- Stage 7 terminology audit — PASS at `7d7b27a4eb81570482ff4d9eaba1dc7c83429272`.
- Stage 7 source spec and gates — PASS at `a3585a7441e320f1ce78f924d293c411854f76ef`.
- Stage 7 explicit source export implementation — PASS at `a5db5d01d96277e83913ec17506c22e3284424eb`.
- Stage 7 export integrity hardening — PASS at `2bd72e4eedbc6753083d12ea7c4eac73e7691ba3`.

## Current artifact vocabulary

- Runtime baseline: the latest `tul-vf-latest.md` evidence for HEAD, Remote HEAD, release gate, working tree, and fresh clone status.
- Source bundle: implemented source-context artifact from `tul export source`, normally written as `tul-source-latest.zip`.
- Review bundle: implemented changed-files transport artifact from `tul export review`, normally written as `tul-review-latest.zip`.
- Export status: warning-only inspection from `tul export status`; it detects stale, missing, invalid, or unrecorded export artifacts and docs drift.
- Post-update exports: an automatic phase after successful commit/push/fresh-verify that refreshes source/review artifacts but records failures as warnings only.
- Backup/recovery authority: Git remote, commit hashes, and tul rollback state. Zip artifacts are not backup authority.

See `docs/workflows/artifact-semantics.md`, `docs/workflows/source-context-and-export.md`, `docs/workflows/source-export-spec.md`, `docs/workflows/export-integrity-hardening.md`, `docs/workflows/post-update-export-automation.md`, `docs/checklists/stage7-package-gates.md`, and `docs/workflows/stage7-bounded-parallel-planning.md`.

## Stage 7 active package

Recommended package:

```text
tul-stage7-post-update-export-automation-bundle-v1
```

Goal:

```text
Run source/review export automatically after successful commit, push, and fresh verification. Keep export failures warning-only and record them in state/report/handoff/latest verify snapshots.
```

Parallel class: Red-light.

Reason: this package changes default post-update behavior, but the change is bounded to post-success artifact generation and must not alter commit, push, rollback, or release-gate semantics.

## Next ready queue

1. Apply `tul-stage7-post-update-export-automation-bundle-v1` and close it with `tul-vf-latest.md`.
2. Verify that `tul export status` reports current source/review bundles after a normal update.
3. Consider a small follow-up audit package only if automatic exports produce noisy warnings.
4. Consider promoting selected docs drift checks to a release gate only after repeated warning-only runs prove low false positives.
5. Run Windows parity smoke only after several self-host packages remain stable.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop reduces rather than multiplies bridge work.
