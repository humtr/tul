# Roadmap

## Completed

- Stage 0 — syntax/runtime recovery
- Stage 1 — runtime boundary restructure
- Stage 1.5 — no-op/state cleanup
- Stage 2 — LLM loop contract / compact README option 2
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

## Active track: tul development acceleration

The current priority is improving the speed and safety of tul's own self-hosting development loop.

Near-term candidates:

1. Package authoring polish: richer manifest templates, package diff summaries, and package provenance metadata.
2. Package report improvements: show authoring/check results in update reports.
3. Self-host loop hardening: repeated `tul update tul -l` should remain safe, inspectable, and fast.

## Stage X — future target onboarding

`humtr/ai` onboarding is intentionally deferred. It should happen after tul's own package creation, verification, and update flow is comfortable enough to reduce the human bridge burden.
