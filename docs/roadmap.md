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
## Macro Stage A v4

- Add final `tul run` decision summary.
- Keep stable latest artifacts and bounded root upload aliases: source/review/vf markdown.
- Keep latest JSON for local machine-readable refresh; it is not normally an upload requirement.

Reference package: `tul-macro-stage-a-run-final-upload-v4`.

## Macro Stage A v5 — final upload and inbox polish

Goal: close the human-facing one-run loop. `tul run` should end with a fixed decision block that is enough for manual acceptance, and `/sdcard/termux/import/tul` should serve as the single upload inbox for the current source/review/verify artifacts.

Scope:

```text
- keep stable latest artifacts for local automation
- keep one current commit-named source/review/vf markdown alias in the import root
- keep dated copies in logs/source, logs/review, and logs/verify
- include source/review/verify upload aliases in verify artifact metadata
- move selected packages from shared Download intake into the project-owned inbox after import
```

Reference package: `tul-macro-stage-a-final-upload-and-inbox-v5`.
