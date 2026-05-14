# current status

Status: Macro Stage A v7 is in progress via `tul-macro-stage-a-head-tag-canonical-v7`.

Baseline before this package:

```text
HEAD: ddb0cdde0bebf435b6402c29b41c672a0aefeb5b
Remote HEAD: ddb0cdde0bebf435b6402c29b41c672a0aefeb5b
Latest package: tul-macro-stage-a-head-only-upload-root-v6
Release gate: PASS
CLI runtime smoke: PASS
Regression tests: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Objective

Make head-tagged artifacts the only current upload artifacts. The canonical upload set is:

```text
tul-source-<head7>.zip
tul-review-<head7>.zip
tul-vf-<head7>.md
```

No root-level `latest` transport or verify files should be produced or displayed as current evidence. Verify JSON remains a dated run-log artifact only.

## Upload inbox policy

The import root is a head-tagged human upload inbox. It should show only the current commit-named upload artifacts at the root. Dated archival copies remain under `logs/source/YYMMDD`, `logs/review/YYMMDD`, and `logs/verify/YYMMDD`.

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

Expected result: the final screen says `Decision: PASS`, source/review/vf head-tagged upload files are shown, root `latest` files are absent, release gate PASS, source/review current, docs drift clean, and warnings none.
