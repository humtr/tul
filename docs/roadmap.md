# tul Roadmap

## Current mode

Stage 7 post-update export automation. Stage 6 is closed, Stage 7 planning consolidation is closed, terminology audit is closed, source spec/gates is closed, explicit source export implementation is closed, and export integrity hardening is closed. The next short-term goal is to reduce bridge work by refreshing source/review transport artifacts automatically after a successful update while keeping export failures warning-only.

## Verified baseline

```text
HEAD: 2bd72e4eedbc6753083d12ea7c4eac73e7691ba3
Remote HEAD: 2bd72e4eedbc6753083d12ea7c4eac73e7691ba3
Release gate: PASS
Steps: 25 pass, 0 fail
Fresh clone verify: PASS
Latest package: tul-stage7-export-integrity-hardening-bundle-v1
```

The runtime baseline remains the latest user-provided `tul-vf-latest.md` when it is newer than this document.

## Completed foundations

- Stage 0 through Stage 6 stabilization checkpoint.
- Stage 7 planning consolidation — verified at `79d27fb07ce52666acb603b714dab33a45079e19`.
- Stage 7 terminology audit — verified at `7d7b27a4eb81570482ff4d9eaba1dc7c83429272`.
- Stage 7 source spec and gates — verified at `a3585a7441e320f1ce78f924d293c411854f76ef`.
- Stage 7 explicit source export implementation — verified at `a5db5d01d96277e83913ec17506c22e3284424eb`.
- Stage 7 export integrity hardening — verified at `2bd72e4eedbc6753083d12ea7c4eac73e7691ba3`.

## Stage 7 objective

Use the stable loop to manage manifest, short-term/mid-term/long-term plans, and bounded parallel bundle candidates. Stage 7 allows several candidate workstreams to be planned and compared at once, while actual application remains sequential and release-gated.

## Stage 7 ready queue

1. **Post-update export automation package**: run source/review export automatically after successful commit, push, and fresh verification; failures are warning-only.
2. **Post-automation audit package**: if needed, tighten wording or status output after one verified automation run.
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
| Export integrity hardening | Closed | `lib/tulcore/integrity.py`, CLI, verify snapshots, handoff, docs | Verified baseline is `2bd72e4...` |
| Post-update export automation | Red-light | update pipeline, postexport helper, state, docs | Changes default post-update behavior, but warning-only |
| Archive policy expansion | Red | archive/sweep/state docs and code | Moves runtime evidence; must have separate dry-run proof |
| Stage X target onboarding | Red | templates, config, possibly external repo docs | Cross-repo scope expands risk |

## Short-term plan

- Automate post-update source and review export only after commit/push/fresh-verify succeeds.
- Keep export failures warning-only.
- Record post-update export outcomes in state/report/handoff and latest verify snapshots.
- Preserve `--no-export`, `--no-source-export`, and `--no-review-export` as recovery/debug escape hatches.
- Continue applying packages sequentially even when planning candidates are compared in parallel.

## Medium-term plan

- Observe whether automatic source/review exports remain current and low-noise across several self-host updates.
- Add more docs drift checks only if current/status/roadmap drift recurs.
- Preserve review/source export as transport artifacts, not recovery authority.

## Long-term plan

- Reduce human bridge work by making runtime evidence, review transport, and source context explicit and role-separated.
- Keep user approval, rollback authority, and destructive-action boundaries intact.
- Apply the tul harness to future target repositories only after the self-host loop demonstrates stable low-friction operation.
