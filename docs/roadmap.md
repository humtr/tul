# tul Roadmap

## Current mode

Stage 6 — accelerated self-host hardening.

The project is moving from single-issue sequential patches to bounded bundles of parallel work. The roadmap is now a ready queue and bundle planner, not a static linear checklist.

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

## Ready queue

Ready queue items can be bundled when they share a capability area and have compatible risk.

- Planning harness insertion: manifest, strategy, learning log, decisions, planning loop.
- Active project context: `tul use <project>`, `tul current`, context state file.
- No-arg read-only commands: `tul status`, `tul verify`, `tul state`, `tul handoff`, `tul package latest`.
- Short fresh verification syntax: `tul verify fresh` while keeping `--fresh-clone` compatibility.
- No-arg mutating commands: `tul update`, `tul import`, `tul rollback` with conflict guards.
- Context conflict UX: active project vs current-directory project safety messages.
- Package mismatch guidance: explain incompatible package manifests and present next commands.
- Verify release gate summary: top-line PASS/FAIL and remediation commands.
- State compact output: latest state, latest published, latest rollbackable, cleanup suggestion.
- Package check diagnostics: clearer failure messages and package authoring guidance.
- Windows parity pass: launcher shim, config paths, inbox roots, `update -l`, verify fresh clone.

## Bundle candidates

### Bundle 1 — Planning harness

Package: `tul_planning_harness_v1`

Scope:

- README planning-harness pointers.
- `docs/manifest.md`.
- `docs/strategy.md`.
- `docs/learning-log.md`.
- `docs/decisions.md`.
- `docs/protocols/planning-loop.md`.
- `docs/checklists/planning-harness.md`.
- project harness templates.

### Bundle 2 — Native context v1a

Scope:

- `tul use <project>`.
- `tul current`.
- active project context file.
- `default_project` support.
- projects output shows active/default.

### Bundle 3 — Native context v1b

Scope:

- no-arg read-only commands.
- `tul verify fresh` shorthand.
- current-directory project inference.
- read-only conflict banner.

### Bundle 4 — Native context v1c/d

Scope:

- no-arg `tul update` as inferred project + latest matching package.
- mutating-command context conflict guard.
- package mismatch classification and guidance.

### Bundle 5 — Release gate and state compactness

Scope:

- verify release gate summary.
- compact state output.
- archive recommendation output.
- docs consistency checks.

## Extraction rules

- Pull short-term items from `docs/strategy.md` capability pressure.
- Keep each bundle coherent and bounded.
- After each published package, update `docs/status/current.md` and add lessons to `docs/learning-log.md` when appropriate.
- Escalate repeated capability friction to `docs/strategy.md`.
- Escalate authority/safety/vision changes to `docs/manifest.md` and `docs/decisions.md`.

## Deferred: Stage X

`humtr/ai` onboarding is intentionally deferred. It should resume only after tul's self-host harness, verification, package discovery, state recovery, and native context are stable enough to reduce rather than multiply bridge work.
