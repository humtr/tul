# Current status

Latest known version: `0.8.23-stabilization-checkpoint`.

Current mode: Stage 6 bounded parallel stabilization checkpoint. The J artifact-semantics track and K cleanup track are closed enough to prepare Stage 6 exit review.

## Verified baseline

Latest verified baseline:

```text
HEAD: d81989449b813256a4dcbbdd0be60b04180d6dd8
Remote HEAD: d81989449b813256a4dcbbdd0be60b04180d6dd8
Release gate: PASS
Steps: 25 pass, 0 fail
Working tree: clean
Fresh clone verify: PASS
```

Canonical latest artifact:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

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

## Current artifact model

- `tul-vf-latest.md` is release-gate evidence with runtime snapshots.
- `tul-review-latest.zip` is explicit review transport from `tul export review`.
- Source export is not automatic and is not a backup.
- Git remote, commit hashes, and rollback state remain the recovery authority.

See `docs/workflows/artifact-semantics.md` and `docs/workflows/stage6-stabilization-checkpoint.md`.

## Current cleanup model

- `tul archive --noop --dry-run --keep 3` is the inspection path.
- `tul archive --noop --keep 3` is the only accepted actual archive move class at this checkpoint.
- `tul package hygiene` reports shared external invalid archives without moving them.
- `tul package hygiene --ingest` moves valid matching tul packages into the project inbox.
- `tul package hygiene --quarantine` only applies to project-inbox cleanup candidates.

## Next ready queue

1. Stage 6 exit review / stabilization checkpoint package.
2. Stage 7 planning harness expansion for manifest, short-term/mid-term/long-term plans, and bounded parallel candidate management.
3. Explicit source export, only if a future task needs full source transfer and root-layout checks.
4. Windows parity, after the self-host loop remains stable across additional packages.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop reduces rather than multiplies bridge work.
