# tul Roadmap

## Current mode

Stage 6 — bounded parallel self-host hardening.

The roadmap is a ready queue and bundle planner. The update-integrated verify gate, compact gate/state output, authoring diagnostics, and archive dry-run guidance have passed release gate and are baseline behavior. The active bounded package is `tul_stage6_handoff_discoverability_bundle_v1`.

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

## Active bundle

### Bundle E — Handoff discoverability bundle

Package: `tul_stage6_handoff_discoverability_bundle_v1`

Scope:

1. Add `docs/llm/post-update-review.md` as the fresh-session review path.
2. Make README, entrypoint, handoff docs, and handoff output agree on read-next priority.
3. Clarify when `tul-vf-latest.md`, `tul state`, and repo zip are each necessary.
4. Keep the bundle docs-first and avoid runtime behavior changes beyond handoff pointers.

Success criteria:

- `docs/llm/post-update-review.md` exists and explains evidence economy.
- Compact handoff points to the post-update review guide.
- README and LLM entrypoint include the post-update review guide.
- Loop checklist includes a handoff discoverability checkpoint.
- Normal `tul update` still produces a release-gate PASS artifact after applying this bundle.

## Ready queue

Ready queue items can be bundled when they share a capability area and have compatible risk.

- Parallel-readiness gate: define how multiple bounded bundles are ordered, checked, and rejected on file conflict.
- Windows parity pass: launcher shim, config paths, inbox roots, native update, verify fresh.
- State cleanup policy expansion: imported/failed cleanup guidance after dry-run behavior has been observed.
- Docs consistency checks: status, roadmap, manifest, strategy, and checklist alignment.

## Bundle candidates

### Bundle F — Parallel-readiness gate bundle

Scope:

- package conflict checklist;
- touched-file overlap rules;
- verify/state/handoff acceptance for multiple small bundles;
- guidance on when to serialize instead of parallelize.

### Bundle G — Windows parity bundle

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
