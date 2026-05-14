# current status

Status: Macro Stage A v6 is in progress via `tul-macro-stage-a-head-only-upload-root-v6`.

Baseline before this package:

```text
HEAD: 85e13c75592ed87e8458d9b1531deea5b9a6c9db
Remote HEAD: 85e13c75592ed87e8458d9b1531deea5b9a6c9db
Latest package: tul-macro-stage-a-final-upload-and-inbox-v5
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

The import root is now a head-only human upload inbox. It should show only the current commit-named upload artifacts at the root:

```text
tul-source-<head7>.zip
tul-review-<head7>.zip
tul-vf-<head7>.md
```

Root-level `*-latest.*` artifacts are removed after export/verify. Dated archival copies remain under `logs/source/YYMMDD`, `logs/review/YYMMDD`, and `logs/verify/YYMMDD`. Verify JSON remains in dated logs for machine-readable inspection, but it is not a normal manual upload target.

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

Expected result: the final screen says `Decision: PASS`, source/review/vf head-tagged upload files are shown, root latest files are absent, release gate PASS, source/review current, docs drift clean, and warnings none.
