# tul Roadmap

## Current mode

Stage 7 terminology hardening after planning consolidation. Stage 6 is closed, and the first Stage 7 planning package is applied and verified. The next short-term risk is vocabulary drift: docs and help text must not make a proposed source-export command look implemented.

## Verified baseline

```text
HEAD: 79d27fb07ce52666acb603b714dab33a45079e19
Remote HEAD: 79d27fb07ce52666acb603b714dab33a45079e19
Release gate: PASS
Steps: 25 pass, 0 fail
Fresh clone verify: PASS
Latest package: tul-stage7-planning-consolidation-bundle-v1
```

The runtime baseline remains the latest user-provided `tul-vf-latest.md` when it is newer than this document.

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
- Stage 6 J track — artifact semantics and explicit review export
- Stage 6 K track — archive execution safety and package inbox hygiene
- Stage 6 stabilization checkpoint — verified baseline closure
- Stage 7 planning consolidation — verified at `79d27fb07ce52666acb603b714dab33a45079e19`

## Stage 6 closure status

Closed:

- J1 artifact semantics checkpoint.
- J2 misleading source zip state removal.
- J3 explicit review bundle export.
- J4 review export rewrite/state integration.
- K1 archive execution safety.
- K2 package inbox ingest policy.
- K3 Stage 6 stabilization checkpoint.

Intentionally not closed as automatic behavior:

- Source zip export. A GitHub-generated `tul-main.zip` can be manual source context, but it is not a tul-proven backup or explicit source export.
- Automatic post-update export. Review export remains explicit until a separate acceptance gate approves automation.

## Stage 7 objective

Use the now-stable loop to manage manifest, short-term/mid-term/long-term plans, and bounded parallel bundle candidates.

Stage 7 does not mean unrestricted parallel implementation. It means several candidate workstreams may be planned and compared at once, while actual application remains sequential and release-gated.

## Stage 7 ready queue

1. **Terminology audit package**: clarify runtime baseline, review bundle, source context, proposed source export, GitHub-generated source archive, and backup/recovery authority across docs and help/docstrings.
2. **Explicit source export spec package**: define exact root layout, freshness, HEAD provenance, sha256, bytes, and file-exclusion rules before implementation.
3. **Explicit source export implementation package**: implement `tul export source` only after the spec is accepted.
4. **Docs drift checker package**: check that docs/status/current.md and roadmap baseline do not contradict the latest release facts.
5. **Acceptance gate template refinement package**: make per-bundle gate declarations more copy-ready if later packages need it.
6. **Windows parity smoke package**: verify PowerShell apply/install/update behavior once self-host planning has stabilized.

## Stage 7 candidate matrix

| Candidate | Class | Likely files | Serialize because |
|---|---|---|---|
| Planning consolidation | Closed | README, manifest, strategy, roadmap, status, checklists, decisions, learning log, workflow docs | Verified baseline is `79d27fb...` |
| Terminology audit | Yellow | README, status, roadmap, decisions, workflow docs, CLI help/docstrings | Owns artifact vocabulary and current status |
| Acceptance gate template refinement | Green/Yellow | checklists, templates, post-update review guide | Yellow if it touches current status or roadmap |
| Source export spec-only | Green/Yellow | artifact semantics, source-context workflow doc, roadmap | Yellow if it revises current queue/status |
| Explicit `tul export source` implementation | Orange | `lib/tulcore/repozip.py`, `lib/tulcore/cli.py`, docs | Runtime/export behavior must serialize after spec acceptance |
| Docs drift checker | Orange | checks or verify-related modules, docs | May affect release gate semantics |
| Review export automation | Red | update pipeline, review, state, verify docs | Changes default post-update behavior |
| Archive policy expansion | Red | archive/sweep/state docs and code | Moves runtime evidence; must have separate dry-run proof |
| Stage X target onboarding | Red | templates, config, possibly external repo docs | Cross-repo scope expands risk |

## Short-term plan

- Land one terminology audit package before any source-export implementation.
- Treat the new commit as the Stage 7 terminology baseline only after release gate PASS and fresh clone PASS.
- Generate subsequent packages one at a time from the new verified runtime baseline plus matching source context.
- Prefer docs/spec packages before runtime implementation packages.

## Mid-term plan

- Add explicit source export only if package-generation sessions repeatedly need full source context beyond review bundles.
- Add docs-drift checks if roadmap/status drift recurs after Stage 7 terminology hardening.
- Improve Windows parity after self-host behavior stays stable across several packages.

## Long-term plan

- Use the planning harness to reduce human bridge work across additional repositories.
- Keep Stage X target onboarding deferred until tul can move another project through package/update/verify/handoff without multiplying manual state transfer.
- Preserve user authority over goals, execution, rollback, cleanup, and artifact trust.

## Cleanup follow-up candidates

- Expand archive policy beyond no-op states only after separate dry-run evidence.
- Add package hygiene reporting to state or review bundle if inbox noise returns.
- Keep deletion out of default cleanup; prefer move/quarantine and explicit operator review.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.
