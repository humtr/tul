# tul Roadmap

## Current mode

Stage 7 export integrity hardening. Stage 6 is closed, Stage 7 planning consolidation is closed, terminology audit is closed, source spec/gates is closed, and explicit source export implementation is closed. The next short-term risk is automating export too early, so the current package adds warning-only integrity diagnostics first.

## Verified baseline

```text
HEAD: a5db5d01d96277e83913ec17506c22e3284424eb
Remote HEAD: a5db5d01d96277e83913ec17506c22e3284424eb
Release gate: PASS
Steps: 25 pass, 0 fail
Fresh clone verify: PASS
Latest package: tul-stage7-source-export-implementation-bundle-v1
Source bundle: generated and verified
```

The runtime baseline remains the latest user-provided `tul-vf-latest.md` when it is newer than this document.

## Completed foundations

- Stage 0 through Stage 6 stabilization checkpoint.
- Stage 7 planning consolidation — verified at `79d27fb07ce52666acb603b714dab33a45079e19`.
- Stage 7 terminology audit — verified at `7d7b27a4eb81570482ff4d9eaba1dc7c83429272`.
- Stage 7 source spec and gates — verified at `a3585a7441e320f1ce78f924d293c411854f76ef`.
- Stage 7 explicit source export implementation — verified at `a5db5d01d96277e83913ec17506c22e3284424eb`.

## Stage 7 objective

Use the stable loop to manage manifest, short-term/mid-term/long-term plans, and bounded parallel bundle candidates.

Stage 7 does not mean unrestricted parallel implementation. It means several candidate workstreams may be planned and compared at once, while actual application remains sequential and release-gated.

## Stage 7 ready queue

1. **Export integrity hardening package**: add warning-only `tul export status`, source bundle freshness warnings, and docs drift warnings.
2. **Post-update export automation package**: after warning-only integrity output proves stable, optionally automate review/source export after successful updates.
3. **Docs drift gate candidate**: promote selected drift checks from warning to gate only after false positives are understood.
4. **Duplicate package guidance package**: refine duplicate package name/hash guidance only if package clutter returns.
5. **Windows parity smoke package**: verify PowerShell apply/install/update behavior once self-host planning has stabilized.

## Stage 7 candidate matrix

| Candidate | Class | Likely files | Serialize because |
|---|---|---|---|
| Planning consolidation | Closed | README, manifest, strategy, roadmap, status, checklists, decisions, learning log, workflow docs | Verified baseline is `79d27fb...` |
| Terminology audit | Closed | README, status, roadmap, decisions, workflow docs, CLI help/docstrings | Verified baseline is `7d7b27...` |
| Source export spec and gates | Closed | source-export spec, artifact semantics, gate checklist, roadmap/status | Verified baseline is `a3585a7...` |
| Explicit source export implementation | Closed | `lib/tulcore/source.py`, `lib/tulcore/cli.py`, `lib/tulcore/state.py`, docs | Verified baseline is `a5db5d0...` |
| Export integrity hardening | Orange | `lib/tulcore/integrity.py`, CLI, verify snapshots, handoff, docs | Warning-only but touches runtime inspection output |
| Post-update export automation | Red | update pipeline, review/source, state, verify docs | Changes default post-update behavior |
| Archive policy expansion | Red | archive/sweep/state docs and code | Moves runtime evidence; must have separate dry-run proof |
| Stage X target onboarding | Red | templates, config, possibly external repo docs | Cross-repo scope expands risk |

## Short-term plan

- Close export integrity hardening before any automatic post-update export.
- Keep export integrity warning-only at first.
- Treat stale source bundles as actionable warnings: run `tul export source` after a successful update when a fresh source baseline is needed.
- Treat unrecorded or stale review bundles as review-transport warnings, not backup/recovery failures.
- Continue applying packages sequentially even when planning candidates are compared in parallel.

## Medium-term plan

- Implement config-gated post-update export automation only after warning-only export status has stabilized.
- Decide whether source export, review export, or both should be automatic by default.
- Add more docs drift checks only if current/status/roadmap drift recurs.
- Preserve review/source export as transport artifacts, not recovery authority.

## Long-term plan

- Reduce human bridge work by making runtime evidence, review transport, and source context explicit and role-separated.
- Keep user approval, rollback authority, and destructive-action boundaries intact.
- Apply the tul harness to future target repositories only after the self-host loop demonstrates stable low-friction operation.
