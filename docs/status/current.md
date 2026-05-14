# current status

Status: Macro Stage A v4 is in progress via `tul-macro-stage-a-run-final-upload-v4`.

Baseline before this package:

```text
HEAD: ec1ddedf10fea2659aa96a88615b5d055913aae3
Remote HEAD: ec1ddedf10fea2659aa96a88615b5d055913aae3
Latest package: tul-macro-stage-a-run-final-upload-v4
Release gate: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Objective

Make one `tul run` invocation sufficient for the normal user loop after a package is available or after no package is found. The loop should refresh transport artifacts and run the release gate, and the release gate should now include the Stage 9B regression harness plus read-only CLI runtime smoke.

## Active read-next set

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

## Validation after applying

```bash
python3 -m unittest discover -s tests
python3 -m py_compile bin/tul lib/tulcore/*.py
git diff --check
tul run dry
tul export
tul verify fresh
tul show exports
```

Expected result: regression tests pass, release gate PASS, source/review current, docs drift clean, and warnings none.
- Macro Stage A v4 target: `tul run` prints a final decision block and writes commit-named upload aliases in the import root.
