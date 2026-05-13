# cleanup workflow

Cleanup is under `clean`. The default behavior is always plan-only.

## Default summary

```bash
tul clean
```

This prints bounded state cleanup and package cleanup plans. It must not move or delete files.

## State cleanup

```bash
tul clean states
tul clean states run
tul clean states run 3
```

`tul clean states` shows the guarded cleanup plan. `tul clean states run` executes the bounded state cleanup with the default keep count of 3. `tul clean states run 3` is the explicit form and keeps the newest 3 selected noop state directories.

The numeric keep argument is interpreted as a keep count when it appears after `run`. A project/path target remains available for non-active project workflows.

## Package cleanup

```bash
tul clean packages
tul clean packages run
```

Package cleanup preserves the shared Download folder rule: unrelated files outside the project inbox are report-only unless explicitly ingested by the package policy.

## Backup cleanup

```bash
tul clean backups
tul clean backups run
```

Backup cleanup is guarded. The plan form reports the repo and scope before anything moves. The run form moves repo-local tul backup files/directories out of the repo.
