# roadmap

## Current baseline

Stage 8 document compaction is closed. Stage 9A review/current-HEAD export hardening is closed. Stage 9B regression test harness is closed. Stage 9C CLI/parser/verify seam extraction is closed after `tul-stage9c-cli-helper-restore-v1`.

## Macro Stage A — run-verified artifact loop

Active package: `tul-macro-stage-a-run-verified-artifacts-v2`.

Goal: reduce user round-trips by making the normal `tul run` path refresh source/review artifacts and then run a release gate that includes regression tests and read-only CLI runtime smoke.

Scope:

```text
- add CLI runtime smoke to the verify gate for the local repo
- add regression tests to the verify gate for the local repo
- keep fresh-clone verification focused on repo/doc/parser/compile checks
- keep export side effects outside verify; `tul run` continues to export before verify
- preserve command surface, package contract, and artifact paths
```

Acceptance:

```bash
python3 -m unittest discover -s tests
python3 -m py_compile bin/tul lib/tulcore/*.py
git diff --check
tul run dry
tul export
tul verify fresh
tul show exports
```

Expected result:

```text
unittest: PASS
verify includes local repo: CLI runtime smoke
verify includes local repo: regression tests
Release gate: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

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
