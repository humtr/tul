# tul commands

Primary full-loop command:

```bash
tul update <project> -l
# equivalent: tul update <project> --latest
```

Use `--package PATH` only when selecting an exact package manually.

## Package discovery

```bash
tul package list tul
tul package latest tul
tul package inspect /sdcard/Download/package.zip
tul update tul -l --dry-run
```

## Verification

```bash
tul verify tul
tul verify tul --fresh-clone
```

## State cleanup

```bash
tul state tul
tul state tul --all --limit 5
tul archive tul --noop --dry-run
tul archive tul --noop --keep 3
tul archive tul --imported --dry-run
```

`archive` moves state directories to `platform.archive_root`; it does not delete them.

## Recovery

```bash
tul rollback tul
tul resume tul
```

Split commands remain recovery/debug tools. The default workflow is still `tul update <project>`.
