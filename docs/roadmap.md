# tul Roadmap

## Current mode

Stage 6 — bounded parallel self-host hardening.

The roadmap is a ready queue and bundle planner. The update-integrated verify gate has passed smoke and is now the normal loop baseline. The compact gate and authoring diagnostics bounded packages have passed. The active bounded package is `tul_stage6_archive_cleanup_dryrun_bundle_v1`.

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

## Recently completed bundles

### Bundle B — Compact gate bundle v1

Package: `tul_stage6_compact_gate_bundle_v1`

Result: release gate passed. Canonical verify layout, release-gate summary, compact state output, and docs consistency updates are now baseline behavior.

### Bundle C — Authoring and diagnostics bundle

Package: `tul_stage6_authoring_diagnostics_bundle_v1`

Result: release gate passed. Package check now catches nested roots, missing payload sources, unreferenced payload files, and apply/commit file drift before update.

## Active bundle

### Bundle D — Archive cleanup dry-run bundle

Package: `tul_stage6_archive_cleanup_dryrun_bundle_v1`

Scope:

1. Make `tul state` recommend `tul archive --noop --dry-run --keep 3` before cleanup.
2. Let `tul archive` use the same guarded native context pattern as other mutating commands when target is omitted.
3. Improve archive dry-run output with inventory counts, selector, keep count, source/destination directories, and protected reference states.
4. Refresh state cleanup workflow and runtime checklist docs.

Success criteria:

- `tul archive --noop --dry-run --keep 3` works from the active/current tul repo without a repeated project argument.
- Dry-run output states that no files were moved.
- Output identifies latest state and latest rollbackable state as protected reference states.
- `tul state` cleanup guidance points to dry-run first.
- Normal `tul update` still produces a release-gate PASS artifact after applying this bundle.

## Ready queue

Ready queue items can be bundled when they share a capability area and have compatible risk.

- Handoff discoverability: make repo-resident state easier for a fresh LLM to find.
- Package check diagnostics: clearer failure messages and package authoring guidance.
- Docs consistency checks: status, roadmap, manifest, strategy, and checklist alignment.
- Windows parity pass: launcher shim, config paths, inbox roots, native update, verify fresh.
- State cleanup polish: better archive defaults and clearer stale failure detection.

## Bundle candidates

### Bundle E — Handoff discoverability bundle

Scope:

- repo-visible handoff and current-state discovery;
- LLM entrypoint improvements for post-update review;
- checklist pointers for next-command selection.

### Bundle F — Windows parity bundle

Scope:

- Windows launcher shim verification;
- Windows inbox/log/config paths;
- `tul update` and post-update verify on Windows;
- PowerShell fallback scripts.

## Extraction rules

- Pull short-term items from `docs/strategy.md` capability pressure.
- Keep each bundle coherent and bounded.
- After each published package, update `docs/status/current.md` and add lessons to `docs/learning-log.md` when appropriate.
- Escalate repeated capability friction to `docs/strategy.md`.
- Escalate authority/safety/vision changes to `docs/manifest.md` and `docs/decisions.md`.

## Deferred: Stage X

`humtr/ai` onboarding is intentionally deferred. It should resume only after tul's self-host harness, verification, package discovery, state recovery, and native context are stable enough to reduce rather than multiply bridge work.
