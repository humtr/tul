# cleanup workflow

Cleanup is under `clean`.

## Default

```bash
tul clean
```

Default cleanup is plan-only. It must not move or delete files.

## State cleanup

```bash
tul clean states
tul clean states run 3
```

`clean states` shows the guarded cleanup plan. `clean states run 3` moves bounded selected state directories according to the current selector and keep count.

## Package cleanup

```bash
tul clean packages
tul clean packages run
```

Package cleanup should preserve the shared Download folder rule: unrelated files outside the project inbox are report-only unless explicitly ingested by the package policy.

## Backup cleanup

```bash
tul clean backups
tul clean backups run
```

Backup cleanup is guarded and should report source and destination paths before moving anything.
