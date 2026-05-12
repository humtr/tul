# Current status

Latest known version: `0.8.11-import-root-latest-snapshot-bundle`.

Current mode: Stage 6 bounded parallel self-host hardening. Native context, package mismatch guidance, update-integrated fresh verification, canonical verify artifact layout, compact state output, package authoring diagnostics, archive dry-run guidance, handoff discoverability, and parallel-readiness gating are baseline behavior. Bundle B, Bundle C, Bundle D, Bundle E, and Bundle F have passed release gate. The active bounded package is the import-root latest snapshot bundle.

## Current verified loop

The intended normal self-host loop is:

```bash
tul package latest
tul update
# upload /sdcard/termux/import/tul/tul-vf-latest.md when review evidence is needed
```

`tul update` should print the update report first, including commit, push verification, rollback, changed files, and checks. It should then run a compact post-update `verify fresh` gate, write markdown/json verify artifacts, and print the LLM handoff. New verify runs use the canonical layout without requiring an extra bootstrap command.

## Current bundle

Package: `tul_stage6_import_root_latest_snapshot_bundle_v1`

Commit message: `Move verify latest to import root`

Scope:

1. Move the stable latest verify markdown/json pair to the tul import root beside `tul-main.zip`.
2. Keep timestamped run artifacts in `logs/verify/YYMMDD/`.
3. Include compact `tul state` and `tul handoff` snapshots in `tul-vf-latest.md`.
4. Rewrite the post-update verify markdown after final handoff-ready state is written.
5. Refresh review, verify, roadmap, checklist, learning log, and decisions docs.

## Verify artifact convention

Canonical latest files live directly under the tul import root so they sit beside `tul-main.zip` for upload:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-vf-latest.json
```

The latest markdown includes the release gate plus compact `tul state` and `tul handoff` snapshots. Timestamped run artifacts live in YYMMDD date folders directly under the verify log root. There is no `runs/` layer:

```text
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-153345-a1dcc39.md
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-153345-a1dcc39.json
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-l-260512-153345-a1dcc39.md
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-l-260512-153345-a1dcc39.json
```

Do not write both `vf` and `verify` naming families. `tul-vf-latest.md/json` are the only canonical latest artifacts and live at the import root. Legacy `tul-verify-latest.*` aliases are no longer generated.

## State output convention

Default `tul state` is a decision view: latest state, latest rollbackable commit, important artifacts, cleanup suggestion, and pointers to full history commands.

Long state output remains available with:

```bash
tul state --all --limit 5
tul state --json
```

## Package authoring convention

Before distribution, a package should pass:

```bash
tul package check /path/to/package.zip --target tul
```

The check should identify missing/nested root manifests, absent or unreferenced payload, generated/cache files, missing apply sources, destination/`commit.files` mismatches, and target mismatches when `--target` is supplied.

## State cleanup convention

State cleanup is intentionally dry-run first. Routine inspection should use:

```bash
tul archive --noop --dry-run --keep 3
```

The dry-run output should show inventory counts, selected state directories, destination archive directories, latest state, and latest rollbackable state before any files are moved. Actual archive moves remain explicit by re-running without `--dry-run` after review.

## Handoff discoverability convention

Fresh LLM sessions should use this review path:

1. `tul-vf-latest.md` for release-gate facts.
2. `tul state` output for state/rollback/cleanup facts when relevant.
3. `docs/llm/entrypoint.md` for repo read order.
4. `docs/llm/post-update-review.md` for evidence economy and next-command selection.
5. `docs/workflows/parallel-readiness.md` before proposing the next bounded bundle.
6. `docs/status/current.md` and `docs/roadmap.md` for current bundle state.

A repo zip is needed for package generation or code-level diagnosis, not for every successful update review.

## Parallel readiness convention

Stage 6 allows bounded parallel planning but still applies packages one at a time. A new package should be generated only after the latest release gate is PASS and a current repo zip matches the verified HEAD. Candidate bundles must declare expected changed files, excluded files, acceptance criteria, and a Green/Yellow/Orange/Red parallel class. Shared runtime files, verify/update/pipeline changes, rollback behavior, archive moves, deletion, or push behavior force serialization.

## Next likely bundles

- Windows parity bundle;
- state cleanup policy expansion for imported/failed states;
- docs consistency checks;
- handoff/runtime prompt polish if fresh-session reviews still miss context.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.
