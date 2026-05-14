# roadmap

## Current baseline

Stage 8 document compaction is closed. Stage 9A review/current-HEAD export hardening is closed. Stage 9B regression test harness is closed. Stage 9C CLI/parser/verify seam extraction is closed after `tul-stage9c-cli-helper-restore-v1`.

## Macro Stage A — one-run verified upload loop

Active package: `tul-macro-stage-a-head-tag-canonical-v7`.

Goal: make one `tul run` invocation enough for normal package application, export, release verification, regression testing, and upload selection. The last screen should be sufficient for user decision-making.

Current scope:

```text
- keep CLI runtime smoke in the verify gate for the local repo
- keep regression tests in the verify gate for the local repo
- keep fresh-clone verification focused on repo/doc/parser/compile checks
- keep export side effects outside verify; `tul run` exports before verify
- make head-tagged artifacts the canonical upload artifacts
- stop producing or displaying root-level latest artifacts as current evidence
```

Canonical upload set:

```text
tul-source-<head7>.zip
tul-review-<head7>.zip
tul-vf-<head7>.md
```

Acceptance:

```bash
tul package
tul run
```

Expected final block:

```text
Decision: PASS
Gates: release=PASS; cli-smoke=PASS; regression=PASS
Artifacts: source=current; review=current; docs=clean; warnings=none; upload=ready
```

The import root should contain the three head-tagged upload files for the current HEAD. Dated archives remain under `logs/source`, `logs/review`, and `logs/verify`.

## Next macro candidates

### Macro Stage B — pipeline and artifact schema consolidation

- split `run_update` into phase helpers;
- centralize source/review manifest schemas;
- clarify review bundle state context.

### Macro Stage C — state and verify module decomposition

- split state store/select/format/archive;
- split verify runner/artifact/snapshot rendering.

### Macro Stage D — safe delete/rename package operations

- add guarded delete/rename support to the package contract.

## Macro Stage A completed substeps

- v2: `verify fresh` includes CLI runtime smoke and regression tests.
- v4: `tul run` ends with a compact final decision block.
- v5: shared Download roots are intake-only; selected packages move into the project-owned inbox.
- v6: root upload aliases are head-tagged and old head aliases are pruned.
- v7: head-tagged artifacts become canonical; latest-named root artifacts are not current evidence.
