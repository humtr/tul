# Current status

Latest known version: `0.8.24-stage7-planning`.

Current mode: Stage 7 planning consolidation. Stage 6 is closed as the verified stabilization baseline. Stage 7 now organizes short-term, mid-term, and long-term plans plus bounded parallel candidate management.

## Verified baseline

Latest verified baseline from the current `tul-vf-latest.md` artifact:

```text
HEAD: 5086c982ae5d52c586049d4fb21c8e7d4ada006d
Remote HEAD: 5086c982ae5d52c586049d4fb21c8e7d4ada006d
Release gate: PASS
Steps: 25 pass, 0 fail
Working tree: clean
Fresh clone verify: PASS
Latest package: tul-stage6-stabilization-checkpoint-bundle-v1
```

Canonical latest artifact:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

When a newer artifact is provided by the user, treat it as the runtime source of truth over this document.

## Closed checkpoints

- Bundle B — compact gate/state: PASS.
- Bundle C — authoring diagnostics: PASS.
- Bundle D — archive cleanup dry-run: PASS.
- Bundle E — handoff discoverability: PASS.
- Bundle F — parallel-readiness gate: PASS.
- Bundle G — import-root latest snapshot: PASS.
- Bundle H — state verify path alignment: PASS.
- Bundle I — source zip export attempt: verify passed, export semantics not closed.
- Bundle J1 — artifact semantics checkpoint: PASS.
- Bundle J2 — remove misleading source zip state: PASS.
- Bundle J3 — explicit review bundle export: PASS.
- Bundle J4 — review export rewrite/state integration: PASS.
- K1 — archive execution safety: PASS.
- K2 — package inbox ingest policy: PASS.
- K3 — Stage 6 stabilization checkpoint: PASS.

## Current artifact model

- `tul-vf-latest.md` is release-gate evidence with runtime snapshots.
- `tul-review-latest.zip` is explicit review transport from `tul export review`.
- A GitHub-generated `tul-main.zip` can be manual source context when package generation needs full repo contents, but it is not a tul runtime backup or a tul-proven explicit source export.
- Future source export must be explicit and must record root layout, freshness, HEAD provenance, sha256, bytes, and exclusions.
- Git remote, commit hashes, and rollback state remain the recovery authority.

See `docs/workflows/artifact-semantics.md`, `docs/workflows/parallel-readiness.md`, and `docs/workflows/stage7-bounded-parallel-planning.md`.

## Current cleanup model

- `tul archive --noop --dry-run --keep 3` is the inspection path.
- `tul archive --noop --keep 3` is the only accepted actual archive move class at this checkpoint.
- `tul package hygiene` reports shared external invalid archives without moving them.
- `tul package hygiene --ingest` moves valid matching tul packages into the project inbox.
- `tul package hygiene --quarantine` only applies to project-inbox cleanup candidates.

## Stage 7 active package

Recommended package:

```text
tul-stage7-planning-consolidation-bundle-v1
```

Goal:

```text
Commit the Stage 7 planning system in one package: Stage 6 baseline closure, roadmap alignment, manifest cleanup, short/mid/long plan, bundle matrix, conflict matrix, and acceptance gates.
```

Parallel class: Yellow.

Reason: this package touches coordination docs. It may consolidate many plans in one commit, but no competing package should edit `docs/status/current.md`, `docs/roadmap.md`, `docs/manifest.md`, `docs/decisions.md`, or `docs/learning-log.md` until the new baseline is verified.

## Next ready queue

1. Apply the Stage 7 planning consolidation package and close it with `tul-vf-latest.md`.
2. If more planning detail is needed, refine acceptance gate templates without touching runtime code.
3. Specify `tul export source` before implementing it.
4. Implement `tul export source` only if the spec is accepted and source context remains a repeated bridge cost.
5. Consider docs drift checking if planning/status baselines drift again.
6. Run Windows parity smoke only after several self-host packages remain stable.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop reduces rather than multiplies bridge work.
