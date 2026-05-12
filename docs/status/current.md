# Current status

Latest known version: `0.8.16-source-export-state-cleanup`.

Current mode: Stage 6 bounded parallel stabilization. The release gate, compact state, handoff discoverability, parallel-readiness gate, import-root latest verify artifact, and runtime snapshots are baseline behavior. Repo/source zip export is explicitly not closed and is being re-scoped.

## Verified baseline

Latest verified baseline:

```text
HEAD: da00aae271a82473f0958e4e66416a4d6f9d5801
Remote HEAD: da00aae271a82473f0958e4e66416a4d6f9d5801
Release gate: PASS
Working tree: clean
```

The latest canonical review artifact remains:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

## Artifact semantics checkpoint

The Stage 6 repo zip work exposed a design error: verify evidence, handoff evidence, source transfer, review transfer, and backup were being treated as one artifact family. This checkpoint freezes the corrected model before more implementation work.

Current rule:

- `tul-vf-latest.md` is release-gate and runtime snapshot evidence.
- Timestamped verify artifacts under `logs/verify/YYMMDD/` are run history.
- `tul state` is the latest decision view.
- `tul handoff` is fresh-session orientation.
- `tul-main.zip` is not accepted as a closed automatic export capability.
- Zip artifacts are transport artifacts, not backups.
- Git remote, commit hashes, and rollback state are the recovery authority.

See `docs/workflows/artifact-semantics.md`.

## Bundle I/J2 status correction

Bundle I and its fixes proved commit/push/verify, but they did not close source zip export semantics. J2 removes the misleading runtime path display and detaches source zip export from the default update loop until explicit review/source export commands exist.

Corrected status:

```text
Bundle I initial: verify PASS, export incomplete
Bundle I fix v2: verify PASS, path surfaced, export semantics unresolved
Bundle J1: artifact vocabulary checkpoint PASS
Bundle J2: remove misleading source zip state output
```

Do not mark repo/source zip export as closed until a future explicit command records freshness, root layout, and provenance evidence.

## Current next bundle

Package: `tul_stage6_review_bundle_export_bundle_v1`

Scope:

1. Add explicit `tul export review`.
2. Write `/sdcard/termux/import/tul/tul-review-latest.zip`.
3. Include latest verify, state, report, handoff, git facts, changed-files, diff, and changed-file copies.
4. Keep review export separate from `verify` and from the default `update` loop for now.
5. Keep full source export as a separate future command.

## Next implementation queue

1. Verify `tul export review` as an explicit command.
2. Decide later whether successful `tul update` should run review export automatically.
3. Implement `tul export source` for explicit source bundles with wrapper/root-layout checks.

## Verify artifact convention

Canonical latest files live directly under the tul import root:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-vf-latest.json
```

Timestamped run artifacts live in YYMMDD date folders directly under the verify log root. There is no `runs/` layer and no legacy `tul-verify-latest.*` alias.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop reduces rather than multiplies bridge work.
