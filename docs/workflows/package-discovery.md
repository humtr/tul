# Package Discovery Workflow

Package discovery is intentionally explicit and inspectable.

## Source roots

`tul package list`, `tul package latest`, and `tul update --latest` scan only configured `platform.inbox_roots`. They do not scan work/archive roots.

## Matching rule

A candidate must have a root `tul-package.yml` whose `target.project`, `target.repo`, and `target.branch` match the resolved project.

## Selection rule

The selected candidate is the newest matching archive by filesystem modification time.

## Inspection commands

```bash
tul package list tul
tul package latest tul
tul package inspect /sdcard/Download/package.zip
tul update tul --latest --dry-run
```

`--dry-run` imports, validates, and creates an apply plan. It does not modify repo files.

## Safety notes

If duplicate package names appear, remove stale downloads or use `--package PATH` explicitly.
