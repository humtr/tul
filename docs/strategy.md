# tul Strategy

This document is the medium-term capability map for `tul`. The roadmap extracts short-term ready-queue work from this strategy. The learning log can push pressure back into this strategy when execution reveals repeated friction.

## Current mode

Stage 6 — accelerated self-host hardening.

The project is moving from sequential micro-patches into bundled, capability-oriented improvement. Bundle size should remain bounded: normally 3–5 coherent changes per package.

## Capability map

| Capability | Current maturity | Recent progress | Next pressure points |
|---|---:|---|---|
| A. Update runtime | High | full-loop update, push, remote verify, rollback, handoff | preserve invariants while adding native defaults |
| B. Package discovery | Medium-high | `package latest/list/inspect`, `update -l`, dry-run | incompatible package explanation, duplicate name/hash guidance |
| C. Package authoring | Medium-high | scaffold/add/summary/zip/check | better diagnostics, zip `--check`, multi-file authoring polish |
| D. Verification / release gate | Medium-high | `verify`, `verify --fresh-clone` | concise release gate summary, docs consistency checks |
| E. State / recovery | Medium | state/archive/rollback/import/resume guidance | compact state, cleanup recommendations, failed-state guidance |
| F. Handoff / LLM loop | Medium-high | compact/full/instructions handoff | next package boundary suggestions, clearer mode distinctions |
| G. Launcher / install | Medium-high | install sync, doctor launcher diagnostics | Windows shim verification and docs |
| H. Cross-platform parity | Medium-low | package format and fallback scripts exist | repeated Windows tests, PowerShell path behavior |
| I. Planning harness | New | manifest v2 concept defined | repo-resident harness insertion and use |
| J. Native project context | Not started | concept designed | `tul use`, `tul current`, no-arg safe inference |
| K. Portable project harness | Not started | templates planned | project-harness templates for future `/ai` or other repos |

## Strategy rules

1. Short-term work should come from the capability map, not only from ad-hoc bug discovery.
2. If one capability receives many quick fixes, check whether it needs a medium-term redesign.
3. If a lesson changes user authority, safety, or the long-term purpose, escalate it to the manifest and decisions log.
4. If a lesson is merely execution friction, keep it in the learning log and ready queue.
5. Stage X target onboarding remains deferred until self-host loop friction is substantially lower.

## Near-term capability pressure

The next pressure cluster is **native context and no-arg command safety**:

- Store active project context.
- Support `tul use <project>` and `tul current`.
- Infer targets for read-only commands.
- Add `tul verify fresh` shorthand.
- Add mutating-command context conflict guards.
- Explain package manifest mismatches using `tul-package.yml`.

Before implementing that cluster, the planning harness itself should be inserted so that the design and follow-up lessons have a durable home.
