# roadmap

## Current baseline

Macro Stage A is closed through the one-run verified upload loop and head-tagged artifact model. Macro Stage B is consolidating artifact consistency, package safety, and pipeline structure in small verified steps.

## Macro Stage A — one-run verified upload loop

Goal: keep one `tul run` invocation sufficient for normal package application, export, release verification, regression testing, and upload selection. The last screen should be sufficient for user decision-making.

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

### Macro Stage A launcher/setup hygiene

- extract launcher installation and diagnostics from `cli.py` into `lib/tulcore/launcher.py`;
- make `tul setup install` the only launcher installation command;
- update platform install scripts to call `setup install`;
- make POSIX/Termux launcher setup idempotently prepare `~/bin` and future-shell PATH wiring;
- add regression coverage so install scripts cannot drift back to legacy top-level `install`.

## Current macro candidates

### Macro Stage B — pipeline and artifact schema consolidation

- remove docs/status latest-package drift coupling;
- clarify review bundle state context;
- keep package archives zip-only;
- split `tul run` refresh phases without behavior change;
- centralize source/review artifact schema constants.

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
- v8: launcher/setup hygiene removes the stale top-level install path and makes `setup install` the canonical bootstrap command.

### Macro Stage A artifact test split

- keep `show exports` runtime coverage in regression tests;
- stop requiring local source/review artifacts to be generated or recorded before `tul verify` can pass on a fresh synced device;
- keep source/review current + warnings none as the final `tul run` / post-export acceptance condition.
