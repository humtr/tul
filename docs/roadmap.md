# tul Roadmap

## Current mode

Stage 7 Green/Yellow hardening after terminology audit. Stage 6 is closed, Stage 7 planning consolidation is closed, and terminology audit is closed. The next short-term risk is implementing source export before the command contract and per-bundle gates are explicit enough.

## Verified baseline

```text
HEAD: 7d7b27a4eb81570482ff4d9eaba1dc7c83429272
Remote HEAD: 7d7b27a4eb81570482ff4d9eaba1dc7c83429272
Release gate: PASS
Steps: 25 pass, 0 fail
Fresh clone verify: PASS
Latest package: tul-stage7-terminology-audit-bundle-v1
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
- Stage 7 terminology audit — verified at `7d7b27a4eb81570482ff4d9eaba1dc7c83429272`

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

Use the stable loop to manage manifest, short-term/mid-term/long-term plans, and bounded parallel bundle candidates.

Stage 7 does not mean unrestricted parallel implementation. It means several candidate workstreams may be planned and compared at once, while actual application remains sequential and release-gated.

## Stage 7 ready queue

1. **Source export spec and gates package**: accept the source-export command/artifact contract and make Green/Yellow package gate templates copy-ready before implementation.
2. **Explicit source export implementation package**: implement `tul export source` only after the spec is accepted and source context remains a repeated bridge cost.
3. **Docs drift checker package**: check that docs/status/current.md and roadmap baseline do not contradict the latest release facts.
4. **Duplicate package guidance package**: refine duplicate package name/hash guidance only if package clutter returns.
5. **Windows parity smoke package**: verify PowerShell apply/install/update behavior once self-host planning has stabilized.

## Stage 7 candidate matrix

| Candidate | Class | Likely files | Serialize because |
|---|---|---|---|
| Planning consolidation | Closed | README, manifest, strategy, roadmap, status, checklists, decisions, learning log, workflow docs | Verified baseline is `79d27fb...` |
| Terminology audit | Closed | README, status, roadmap, decisions, workflow docs, CLI help/docstrings | Verified baseline is `7d7b27...` |
| Source export spec and gates | Yellow | source-export spec, artifact semantics, gate checklist, roadmap/status | Owns the pre-implementation contract and coordination docs |
| Explicit `tul export source` implementation | Orange | `lib/tulcore/repozip.py`, `lib/tulcore/cli.py`, docs | Runtime/export behavior must serialize after spec acceptance |
| Docs drift checker | Orange | checks or verify-related modules, docs | May affect release gate semantics |
| Review export automation | Red | update pipeline, review, state, verify docs | Changes default post-update behavior |
| Archive policy expansion | Red | archive/sweep/state docs and code | Moves runtime evidence; must have separate dry-run proof |
| Stage X target onboarding | Red | templates, config, possibly external repo docs | Cross-repo scope expands risk |

## Short-term plan

- Close the source export spec and gates package before any runtime implementation.
- Treat the new commit as the Stage 7 source-spec baseline only after release gate PASS and fresh clone PASS.
- Generate subsequent packages one at a time from the new verified runtime baseline plus matching source context.
- Prefer docs/spec packages before runtime packages when a command name or artifact role can be misread.
- Keep `tul export source` non-runnable until an implementation package explicitly wires the command and proves the accepted gate.

## Medium-term plan

- Implement `tul export source` only if the accepted spec remains valuable after more self-host cycles.
- Add docs drift checking if current status or roadmap repeatedly lags behind latest verify facts.
- Preserve review export as explicit until automatic post-update export has a separate Red-class decision and acceptance gate.
- Strengthen duplicate package diagnostics if package inbox noise returns.

## Long-term plan

- Reduce human bridge work by making runtime evidence, review transport, and source context explicit and role-separated.
- Keep user approval, rollback authority, and destructive-action boundaries intact.
- Apply the tul harness to future target repositories only after the self-host loop demonstrates stable low-friction operation.
