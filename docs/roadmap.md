# tul Roadmap

## Current mode

Stage 6 stabilization checkpoint. The runtime loop is stable enough to prepare Stage 6 exit review and Stage 7 bounded parallel planning.

## Verified baseline

```text
d81989449b813256a4dcbbdd0be60b04180d6dd8
Release gate: PASS
Fresh clone verify: PASS
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

## Stage 6 closure status

Closed:

- J1 artifact semantics checkpoint.
- J2 misleading source zip state removal.
- J3 explicit review bundle export.
- J4 review export rewrite/state integration.
- K1 archive execution safety.
- K2 package inbox ingest policy.

Not closed as automatic behavior:

- Source zip export. `tul-main.zip` is not a canonical backup or automatic source evidence.
- Automatic post-update export. Review export remains explicit until a separate acceptance gate approves automation.

## Stage 7 candidate: planning and bounded parallel operations

Goal: use the now-stable loop to manage manifest, short-term/mid-term/long-term plans, and bounded parallel bundle candidates.

Initial bundle candidates:

1. Planning ledger checkpoint: sync manifest, strategy, roadmap, status, decisions, and learning log around Stage 7 objectives.
2. Bundle candidate matrix: record touched files, gate type, conflict class, and serialization requirement.
3. Acceptance-gate templates: standardize per-bundle success criteria before package generation.
4. Optional source export: implement only if review bundle plus latest verify is insufficient for code generation.

## Cleanup follow-up candidates

- Expand archive policy beyond no-op states only after separate dry-run evidence.
- Add package hygiene reporting to state or review bundle if inbox noise returns.
- Keep deletion out of default cleanup; prefer move/quarantine and explicit operator review.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.
