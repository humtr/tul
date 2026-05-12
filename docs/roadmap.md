# tul Roadmap

## Current mode

Stage 6 — accelerated self-host hardening.

The roadmap is now a ready queue and bundle planner. Short-term tasks are intentionally stocked in advance and extracted from medium-term capability pressure. Lessons from each update can modify the ready queue, strategy, and, when justified, the manifest.

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

## Current smoke

Package: `tul_parallel_entry_smoke_v1`

Goal: confirm the one-command native loop after the update-integrated verify gate hotfix.

Success criteria:

- `tul update` applies this docs-only smoke package.
- Commit and push succeed.
- Post-update `verify fresh` runs automatically.
- `tul-vf-latest.md` is updated to the smoke commit.
- The working tree is clean after update.
- The handoff includes verify artifact pointers.

## Ready queue

Ready queue items can be bundled when they share a capability area and have compatible risk.

- Canonical verify artifact layout: latest files at log root; timestamped run files under date folders; no legacy duplicate `verify` names.
- Verify release gate summary: keep terminal output compact while preserving commit/push/rollback visibility.
- State compact output: latest state, latest published, latest rollbackable, cleanup suggestion.
- Archive recommendations: reduce no-op/imported state clutter.
- Package check diagnostics: clearer failure messages and package authoring guidance.
- Docs consistency checks: status, roadmap, manifest, strategy, and checklist alignment.
- Windows parity pass: launcher shim, config paths, inbox roots, native update, verify fresh.

## Bundle candidates

### Bundle A — Parallel entry smoke

Package: `tul_parallel_entry_smoke_v1`

Scope:

- docs-only update;
- record canonical verify artifact layout decision;
- record bootstrap lessons from update-integrated verify;
- establish pass/fail criteria for parallel entry.

### Bundle B — Compact gate bundle v1

Package: `tul_stage6_compact_gate_bundle_v1`

Initial parallel scope:

1. Canonical verify log layout implementation.
2. Release-gate summary polish.
3. Compact state output.
4. Docs/checklist consistency updates.

This is the first bounded parallel bundle after the smoke pass. It should stay small enough that a failure can still be triaged quickly.

### Bundle C — Authoring and diagnostics bundle

Scope:

- package check diagnostics;
- zip/check workflow polish;
- clearer mismatch and authoring remediation messages.

### Bundle D — Windows parity bundle

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
