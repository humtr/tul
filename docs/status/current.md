# current status

Status: Macro Stage A v5 is in progress via `tul-macro-stage-a-final-upload-and-inbox-v5`.

Baseline before this package:

```text
HEAD: 85e13c75592ed87e8458d9b1531deea5b9a6c9db
Remote HEAD: 85e13c75592ed87e8458d9b1531deea5b9a6c9db
Latest package: tul-macro-stage-a-run-final-upload-v4
Release gate: PASS
CLI runtime smoke: PASS
Regression tests: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Objective

Make one `tul run` invocation sufficient for the normal user loop and make its last screen enough for a human decision. The final block should show PASS/CHECK, gate status, artifact status, warning status, and the three commit-named upload files.

## Upload inbox policy

The import root remains the human-facing upload inbox. It should show stable latest artifacts plus one current commit-named alias for each upload artifact:

```text
tul-source-latest.zip
tul-review-latest.zip
tul-vf-latest.md
tul-vf-latest.json
tul-source-<head7>.zip
tul-review-<head7>.zip
tul-vf-<head7>.md
```

Commit-named aliases are also kept in dated log folders. Older root aliases are pruned. `tul-vf-latest.json` is kept for local machine-readable refresh and is not a normal manual upload target.

## Package intake policy

Shared Download roots are intake-only. If a valid selected package is found in a shared external inbox such as `/sdcard/Download`, `tul run` copies it to the work directory and then moves the original archive into the project-owned inbox under the import root. Packages already under the project import root are not moved again.

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
tul package
tul run
```

Expected result: the final screen says `Decision: PASS`, source/review/vf upload aliases are shown, release gate PASS, source/review current, docs drift clean, and warnings none.
