# Current status

Latest known version: `0.8.21-package-inbox-hygiene`.

Current mode: Stage 6 bounded parallel stabilization, K track. K1 archive execution safety is closed; K2 package inbox hygiene adds dry-run/quarantine handling for duplicate and invalid package archives.

## Verified baseline

Latest verified baseline:

```text
HEAD: b07f4a2f29d7d46857923e847211f4e12b62f96d
Remote HEAD: b07f4a2f29d7d46857923e847211f4e12b62f96d
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
Bundle J2: remove misleading source zip state output PASS
Bundle J3: explicit review bundle export PASS
```

Do not mark repo/source zip export as closed until a future explicit command records freshness, root layout, and provenance evidence.

## Current next bundle

Package: `tul_stage6_review_export_state_integration_bundle_v2`

Scope:

1. Keep `tul export review` as an explicit command.
2. Record review bundle metadata in the latest state.
3. Append review export evidence to the latest report and handoff artifacts.
4. Refresh `tul-vf-latest.md` runtime snapshots after explicit review export.
5. Do not attach review export automatically to `tul update` yet.

## Next implementation queue

1. Verify that `tul export review` leaves `review bundle: ...` evidence in `tul state`.
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


## K1 archive execution safety

K1 narrows actual archive movement while preserving broad dry-run inspection. Actual moves are allowed only for `--noop` selections. Latest and latest rollbackable states are protected by the archive engine and skipped even if a selector would otherwise include them.

Recommended execution path:

```bash
tul archive --noop --dry-run --keep 3
tul archive --noop --keep 3
```

Do not move imported, failed, mixed, or broad `--all` state selections until separate cleanup policies are accepted.
## K2 package inbox hygiene

K2 adds a package hygiene command for inbox-root cleanup:

```bash
tul package hygiene
tul package hygiene --quarantine
```

The dry-run selects invalid archives and older duplicate matching packages. `--quarantine` moves selected files under the platform package-quarantine root. Files are moved, not deleted. Incompatible packages remain visible but are not quarantined by default.
