# tul Roadmap

## Current mode

Stage 6 — bounded parallel stabilization.

The current priority is not another convenience feature. The repo zip export work exposed an artifact-model problem, so the next sequence is a stabilization checkpoint followed by smaller export cleanups.

## Verified baseline

```text
c647c6ebe4dfffc7197185a09da8dca2b064f5e6
Release gate: PASS
```

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
- Stage 6.1a-f — native context through update-integrated verify gate
- Stage 6.2 — compact verify gate and state output
- Stage 6.4 — package authoring diagnostics
- Stage 6.5 — archive cleanup dry-run guidance
- Stage 6.6 — handoff discoverability
- Stage 6.7 — parallel-readiness gate
- Stage 6.8 — import-root latest verify snapshots
- Stage 6.9 — state verify path alignment

## Recent bundle status

### Closed

- Bundle B — compact gate/state: PASS
- Bundle C — authoring diagnostics: PASS
- Bundle D — archive cleanup dry-run: PASS
- Bundle E — handoff discoverability: PASS
- Bundle F — parallel-readiness gate: PASS
- Bundle G — import-root latest snapshot: PASS
- Bundle H — state verify path alignment: PASS

### Not closed

- Bundle I — repo zip export: verify passed, but source export semantics are unresolved.

Reason: state can show a zip path without proving that the current update generated a fresh, wrapper-free source archive matching the verified HEAD. Full source export also drifted toward backup semantics, which is not the intended role.

## Active bundle

### Bundle J1 — Artifact semantics checkpoint

Package: `tul_stage6_artifact_semantics_checkpoint_bundle_v1`

Goal: stop and document the artifact model before further export work.

Scope:

1. Define verify artifact, state, handoff, review bundle, source bundle, and backup separately.
2. Record `tul-main.zip` automatic export as unresolved.
3. Reframe future upload work around `tul-review-latest.zip` and explicit `tul export source`.
4. Preserve verified baseline and avoid runtime behavior changes.

Acceptance:

- Release gate PASS.
- `docs/workflows/artifact-semantics.md` exists.
- `docs/status/current.md` says repo zip export is unresolved.
- `docs/llm/post-update-review.md` no longer treats `tul-main.zip` as automatically trusted evidence.
- Roadmap lists J2/J3/J4 as separate follow-up bundles.

## Next ready queue

### J2 — Remove misleading source zip state

Goal: do not show source zip as successful unless the runtime recorded valid freshness/root-layout/provenance evidence.

Expected files:

- `lib/tulcore/state.py`
- `lib/tulcore/report.py`
- `lib/tulcore/handoff.py`
- docs

### J3 — Review bundle export

Goal: implement `tul export review` for compact diff-oriented review bundles.

Expected latest path:

```text
/sdcard/termux/import/tul/tul-review-latest.zip
```

Expected contents: latest verify, state, handoff, changed-files, diff, and changed-file copies.

### J4 — Explicit source bundle export

Goal: implement `tul export source` for full source context only when needed.

Requirements: no wrapper directory, root-layout checks, size/file count/sha256, and explicit command invocation.

### Later

- Decide whether successful `tul update` should automatically run review export.
- Windows parity bundle.
- State cleanup policy expansion.
- Docs consistency checks.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.
