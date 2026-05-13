# roadmap

Stage 7 is closed. Stage 8 focuses on reducing operational drag after the command-surface and artifact model stabilized.

## Current baseline

- Normal user loop: `tul run`.
- Command surface: `show / package / update / verify / export / run / clean / recover / setup`.
- Runtime verification evidence: `tul-vf-latest.md`.
- Source/review transport artifacts: `tul-source-latest.zip` and `tul-review-latest.zip`.
- Package contract: `tul-package.yml + files/ + README.md`.

## Stage 8 queue

1. **Document active-tree compaction, phase 1.**
   Consolidate ownership into README, status, manifest, roadmap, commands, package-spec, decisions, learning-log, and the small template set. Preserve runtime-referenced compatibility docs until pointers are narrowed.

2. **Runtime pointer compaction, phase 2.**
   Narrow `tul show handoff` read-next and verify required-doc expectations to the compact active doc set. Then delete compatibility docs.

3. **Deletion-capable cleanup decision.**
   Decide whether document deletion should be handled by an explicit package-contract extension, a one-off manual Git operation, or a tightly scoped cleanup package after runtime pointers are updated.

4. **Windows environment doc ownership.**
   Decide whether `docs/windows-dwork-environment.md` belongs in this repo, a platform-specific subtree, or a separate user environment workspace.

5. **Decision/log compression.**
   Optionally compress `docs/decisions.md` and `docs/learning-log.md` after active tree compaction is complete.

## Deferred

- Non-package runtime refactor.
- External project-harness generalization.
- Windows track expansion.
- New target repositories beyond `humtr/tul`.

## Operating rule

Parallel planning is allowed. Mutating package application remains sequential and gated against the latest verified baseline.
