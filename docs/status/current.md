# Current status

Latest known version: `0.8.28-stage7-export-integrity`.

Current mode: Stage 7 export integrity hardening. Stage 6 is closed. Stage 7 planning consolidation, terminology audit, source spec/gates, and explicit source export implementation are closed. The current task is to add warning-only export freshness and docs drift checks before any post-update automatic export.

## Verified baseline

Latest verified baseline from the current `tul-vf-latest.md` artifact:

```text
HEAD: a5db5d01d96277e83913ec17506c22e3284424eb
Remote HEAD: a5db5d01d96277e83913ec17506c22e3284424eb
Release gate: PASS
Steps: 25 pass, 0 fail
Working tree: clean
Fresh clone verify: PASS
Latest package: tul-stage7-source-export-implementation-bundle-v1
Source bundle: generated and verified
```

Canonical latest artifacts:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-source-latest.zip
```

When a newer `tul-vf-latest.md` is provided by the user, treat it as the runtime source of truth over this document.

## Closed checkpoints

- Stage 6 stabilization checkpoint — PASS at `5086c982ae5d52c586049d4fb21c8e7d4ada006d`.
- Stage 7 planning consolidation — PASS at `79d27fb07ce52666acb603b714dab33a45079e19`.
- Stage 7 terminology audit — PASS at `7d7b27a4eb81570482ff4d9eaba1dc7c83429272`.
- Stage 7 source spec and gates — PASS at `a3585a7441e320f1ce78f924d293c411854f76ef`.
- Stage 7 explicit source export implementation — PASS at `a5db5d01d96277e83913ec17506c22e3284424eb`.

## Current artifact vocabulary

- Runtime baseline: the latest `tul-vf-latest.md` evidence for HEAD, Remote HEAD, release gate, working tree, and fresh clone status.
- Source bundle: currently implemented explicit source-context artifact from `tul export source`, normally written as `tul-source-latest.zip`.
- Review bundle: currently implemented explicit changed-files transport artifact from `tul export review`, normally written as `tul-review-latest.zip`.
- Export status: warning-only inspection from `tul export status`; it detects stale, missing, invalid, or unrecorded export artifacts and docs drift.
- Backup/recovery authority: Git remote, commit hashes, and tul rollback state. Zip artifacts are not backup authority.

See `docs/workflows/artifact-semantics.md`, `docs/workflows/source-context-and-export.md`, `docs/workflows/source-export-spec.md`, `docs/workflows/export-integrity-hardening.md`, `docs/checklists/stage7-package-gates.md`, and `docs/workflows/stage7-bounded-parallel-planning.md`.

## Stage 7 active package

Recommended package:

```text
tul-stage7-export-integrity-hardening-bundle-v1
```

Goal:

```text
Combine export consistency hardening, source bundle freshness warning, and docs drift checking as warning-only runtime diagnostics.
```

Parallel class: Orange.

Reason: this package touches CLI/runtime inspection output, verify runtime snapshots, handoff wording, docs, and version metadata. It must not automate post-update export.

## Next ready queue

1. Apply `tul-stage7-export-integrity-hardening-bundle-v1` and close it with `tul-vf-latest.md`.
2. If warning-only export status is stable, implement post-update export automation as a separate Red-class package.
3. Consider promoting selected docs drift checks to a release gate only after repeated warning-only runs prove low false positives.
4. Refine duplicate package name/hash guidance only if inbox clutter returns.
5. Run Windows parity smoke only after several self-host packages remain stable.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop reduces rather than multiplies bridge work.
