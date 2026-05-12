# tul Roadmap

## Current mode

Stage 6 — bounded parallel self-host hardening.

The roadmap is a ready queue and bundle planner. The update-integrated verify gate, compact gate/state output, authoring diagnostics, archive dry-run guidance, and handoff discoverability have passed release gate and are baseline behavior. The active bounded package is `tul_stage6_parallel_readiness_gate_bundle_v1`.

## Completed foundations

- Stage 0 — syntax/runtime recovery
- Stage 1 — runtime boundary restructure
- Stage 1.5 — no-op/state cleanup
- Stage 2 — LLM loop contract and README option 2
- Stage 2.1 — launcher/install sync
- Stage 2.1.1 — doctor/no-op output polish
- Stage 2.5 — apply safety audit
- Stage 3 — recovery/debug commands
- Stage 3.1 — recovery state selection
- Stage 4 — init/config onboarding
- Stage 5.1 — verify/fresh clone acceleration
- Stage 5.2 — package discovery polish
- Stage 5.3 — state cleanup UX
- Stage 5.4 — package authoring helper
- Stage 5.5 — package authoring polish
- Stage 6.0 — planning harness insertion
- Stage 6.0.1 — verify artifact logging
- Stage 6.0.2 — short verify artifact names
- Stage 6.1a — active project context
- Stage 6.1b — read-only native context and `tul verify fresh`
- Stage 6.1c — guarded native update/import/rollback
- Stage 6.1d — package manifest mismatch guidance
- Stage 6.1e — update-integrated verify gate and handoff hotfix
- Stage 6.1f — normal update smoke for post-update fresh verification
- Stage 6.2 — compact verify gate and state output
- Stage 6.4 — package authoring diagnostics
- Stage 6.5 — archive cleanup dry-run guidance
- Stage 6.6 — handoff discoverability

## Recently completed bundles

### Bundle B — Compact gate bundle v1

Package: `tul_stage6_compact_gate_bundle_v1`

Result: release gate passed. Canonical verify layout, release-gate summary, compact state output, and docs consistency updates are now baseline behavior.

### Bundle C — Authoring and diagnostics bundle

Package: `tul_stage6_authoring_diagnostics_bundle_v1`

Result: release gate passed. Package check now catches nested roots, missing payload sources, unreferenced payload files, and apply/commit file drift before update.

### Bundle D — Archive cleanup dry-run bundle

Package: `tul_stage6_archive_cleanup_dryrun_bundle_v1`

Result: release gate passed. `tul state` points to dry-run cleanup, and `tul archive --noop --dry-run --keep 3` prints inventory, protected reference states, and source/destination directories without moving files.

### Bundle E — Handoff discoverability bundle

Package: `tul_stage6_handoff_discoverability_bundle_v1`

Result: release gate passed. Fresh sessions now have an explicit post-update review guide, compact handoff read-next pointers, and evidence-economy guidance for deciding when `tul-vf-latest.md`, `tul state`, or repo zip is required.

### Bundle F — Parallel-readiness gate bundle

Package: `tul_stage6_parallel_readiness_gate_bundle_v1`

Result: release gate passed. Fresh sessions now have a bounded-bundle readiness guide, file-overlap rules, and Green/Yellow/Orange/Red classification before package generation.

## Active bundle

### Bundle G — Import-root latest snapshot bundle

Package: `tul_stage6_import_root_latest_snapshot_bundle_v1`

Scope:

1. Move `tul-vf-latest.md/json` to `/sdcard/termux/import/tul/` beside `tul-main.zip`.
2. Keep timestamped run artifacts in `logs/verify/YYMMDD/`.
3. Include compact `tul state` and `tul handoff` snapshots in `tul-vf-latest.md`.
4. Ensure `tul update` rewrites the verify markdown after final state/handoff are available.
5. Update review and verify docs so the user can upload one latest markdown file for normal review.

Success criteria:

- `tul-vf-latest.md/json` are written under the tul import root.
- Timestamped run artifacts remain under `logs/verify/YYMMDD/`.
- Latest markdown contains `## Runtime snapshots`, `### tul state`, and `### tul handoff`.
- `tul state` reports the root latest markdown path after update.
- Normal `tul update` still produces a release-gate PASS artifact after applying this bundle.

## Ready queue

Ready queue items can be bundled when they share a capability area and have compatible risk. Apply the parallel-readiness gate before generating a package.

- Windows parity pass: launcher shim, config paths, inbox roots, native update, verify fresh.
- State cleanup policy expansion: imported/failed cleanup guidance after dry-run behavior has been observed.
- Docs consistency checks: status, roadmap, manifest, strategy, and checklist alignment.

## Bundle candidates

### Bundle H — Windows parity bundle

Scope:

- Windows launcher shim verification;
- Windows inbox/log/config paths;
- `tul update` and post-update verify on Windows;
- PowerShell fallback scripts.

### Bundle I — State cleanup policy expansion

Scope:

- imported/failed dry-run selectors;
- archive review guidance;
- explicit stop rules before actual deletion or pruning.

## Extraction rules

- Pull short-term items from `docs/strategy.md` capability pressure.
- Keep each bundle coherent and bounded.
- After each published package, update `docs/status/current.md` and add lessons to `docs/learning-log.md` when appropriate.
- Escalate repeated capability friction to `docs/strategy.md`.
- Escalate authority/safety/vision changes to `docs/manifest.md` and `docs/decisions.md`.

## Deferred: Stage X

`humtr/ai` onboarding is intentionally deferred. It should resume only after tul's self-host harness, verification, package discovery, state recovery, and native context are stable enough to reduce rather than multiply bridge work.


### Stage 6 Bundle H — state verify path alignment

Goal: align compact `tul state` and embedded runtime snapshots with the import-root latest verify path introduced by Bundle G.

Scope:

1. Normalize stale bootstrap-time `logs/verify/<project>-vf-latest.md` references in compact state output.
2. Keep timestamped run artifacts unchanged under `logs/verify/YYMMDD/`.
3. Keep import-root `tul-vf-latest.md/json` as the canonical latest upload pair.
4. Avoid modifying verify, update, rollback, archive, or push behavior.

Next candidate: export a current `tul-main.zip` automatically after a successful update, with explicit excludes and safe defaults.


### Bundle I — Repo zip export bundle

Status: active package.

Goal: remove the last routine manual repo-zip bridge step by refreshing `/sdcard/termux/import/tul/tul-main.zip` after successful full updates. Keep it as a latest pointer only, exclude generated/transient content, and surface export status in compact state/runtime snapshots.

Acceptance:

1. `tul update` succeeds normally and still closes with release gate PASS.
2. `/sdcard/termux/import/tul/tul-main.zip` exists after a successful full update.
3. The zip excludes `.git`, caches, build outputs, existing zip files, and backup files.
4. `tul-vf-latest.md` runtime `tul state` snapshot shows the repo zip path.
5. Export failure is visible in state but does not corrupt the already-passed release gate.
