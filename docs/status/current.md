# Current status

Latest known version: `0.8.15-artifact-semantics-checkpoint`.

Current mode: Stage 6 bounded parallel stabilization. The release gate, compact state, handoff discoverability, parallel-readiness gate, import-root latest verify artifact, and runtime snapshots are baseline behavior. Repo/source zip export is explicitly not closed and is being re-scoped.

## Verified baseline

Latest verified baseline:

```text
HEAD: c647c6ebe4dfffc7197185a09da8dca2b064f5e6
Remote HEAD: c647c6ebe4dfffc7197185a09da8dca2b064f5e6
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

## Bundle I status correction

Bundle I and its fixes proved commit/push/verify, but they did not close source zip export semantics.

Corrected status:

```text
Bundle I initial: verify PASS, export incomplete
Bundle I fix v2: verify PASS, path surfaced, export semantics unresolved
```

Do not mark repo/source zip export as closed until the runtime records freshness, root layout, and provenance evidence.

## Current next bundle

Package: `tul_stage6_artifact_semantics_checkpoint_bundle_v1`

Scope:

1. Document artifact roles and corrected ownership.
2. Stop treating `tul-main.zip` as canonical backup or proven source evidence.
3. Split future work into review bundle export and explicit source bundle export.
4. Record Bundle I as unresolved rather than completed.
5. Preserve the verified baseline and keep runtime behavior changes out of this checkpoint.

## Next implementation queue

1. Remove misleading source zip state output.
2. Implement `tul export review` for compact diff-oriented upload bundles.
3. Implement `tul export source` for explicit source bundles with wrapper/root-layout checks.
4. Decide later whether `tul update` should automatically run review export.

## Verify artifact convention

Canonical latest files live directly under the tul import root:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-vf-latest.json
```

Timestamped run artifacts live in YYMMDD date folders directly under the verify log root. There is no `runs/` layer and no legacy `tul-verify-latest.*` alias.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop reduces rather than multiplies bridge work.
