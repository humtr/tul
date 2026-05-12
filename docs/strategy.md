# tul Strategy

This document is the medium-term capability map for `tul`. The roadmap extracts short-term ready-queue work from this strategy. The learning log can push pressure back into this strategy when execution reveals repeated friction.

## Current mode

Stage 7 — planning consolidation and bounded parallel operations.

Stage 6 closed the self-host stabilization baseline. Stage 7 should not rush into runtime behavior changes. Its first job is to make the planning ledger strong enough that several candidate workstreams can be designed in parallel while applied packages remain sequential, reviewable, and rollbackable.

The operating rule is:

```text
parallel planning, sequential gated update
```

## Capability map

| Capability | Current maturity | Recent progress | Next pressure points |
|---|---:|---|---|
| A. Update runtime | High | full-loop update, push, remote verify, rollback, handoff, integrated verify artifact | preserve invariants; avoid unnecessary pipeline churn |
| B. Package discovery | High | latest matching package selection, incompatible/invalid diagnostics, hygiene ingest/quarantine split | duplicate clutter policy only if inbox noise returns |
| C. Package authoring | High | scaffold/add/summary/zip/check, nested-root and payload diagnostics | acceptance-gate templates and package boundary discipline |
| D. Verification / release gate | High | stable latest markdown/json, timestamped run logs, fresh clone verify, runtime snapshots | optional docs-drift checks; keep terminal output compact |
| E. State / recovery | Medium-high | compact state, latest rollbackable state, archive dry-run and noop move safety | broader cleanup only after separate policy gates |
| F. Handoff / LLM loop | High | compact read-next, latest artifact includes handoff snapshot | keep handoff concise; improve Stage 7 package boundary guidance |
| G. Launcher / install | Medium-high | install sync, doctor launcher diagnostics | Windows shim parity after planning consolidation |
| H. Cross-platform parity | Medium | package format and apply scripts remain cross-platform | repeated Windows smoke tests, PowerShell path behavior |
| I. Planning harness | Medium-high | manifest/strategy/roadmap/status/learning/decisions exist and are used | conflict matrix, bundle matrix, short/mid/long plan alignment |
| J. Native project context | High for self-host loop | `tul use`, `tul current`, guarded no-arg commands, `tul verify fresh` | keep context guards visible in docs and checks |
| K. Artifact semantics | Medium-high | `tul-vf-latest.md` and `tul export review` roles are separated | explicit source export only when needed; no backup semantics for zip artifacts |
| L. Portable project harness | Deferred | templates exist | Stage X target onboarding after more self-host cycles |

## Strategy rules

1. Short-term work should come from the capability map, not only from ad-hoc bug discovery.
2. If several candidate bundles can be prepared at once, classify them first and apply them one at a time.
3. If one capability receives many quick fixes, check whether it needs a medium-term redesign.
4. If a lesson changes user authority, safety, artifact semantics, or the long-term purpose, escalate it to the manifest and decisions log.
5. If a lesson is merely execution friction, keep it in the learning log and ready queue.
6. Stage X target onboarding remains deferred until self-host loop friction is substantially lower.

## Near-term capability pressure

The next pressure cluster is **Stage 7 planning control**:

- close Stage 6 as a verified stabilization baseline;
- align manifest, strategy, roadmap, status, checklists, learning log, and decisions;
- maintain a bundle candidate matrix with Green/Yellow/Orange/Red classes;
- define touched-file and acceptance-gate conflict rules;
- separate planning work from runtime implementation work;
- preserve the source/review/backup artifact distinctions.

After this planning consolidation, implementation work can proceed in smaller packages: explicit source export, docs drift checks, review/source provenance hardening, Windows parity, or cleanup expansion.
