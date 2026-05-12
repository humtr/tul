# State cleanup workflow

`tul` keeps work state under the configured `platform.work_root`. Repeated package testing can create many no-op, imported, or failed states. These records are useful while debugging, so cleanup should begin with a dry-run plan rather than an immediate move.

## Recommended inspection

```bash
tul state
tul state --all --limit 5
tul state --json
```

Default `tul state` is a decision view. It shows the latest state, latest rollbackable commit, key artifacts, and the recommended cleanup dry-run. Full history is explicit behind `--all` or `--json`.

## Dry-run first

Start with no-op state cleanup because no-op work states are usually clutter and do not contain commits. Keep the newest few records until repeated runs prove they are no longer useful.

```bash
tul archive --noop --dry-run --keep 3
```

The dry-run output should show:

- project and inferred target context when the target is omitted;
- work root and archive root;
- mode, selector, and keep count;
- total/noop/imported/failed/rollbackable inventory counts;
- latest state and latest rollbackable state as protected references;
- each selected source state directory and destination archive directory;
- an explicit note that no files were moved.

## Move only after review

After reviewing the dry-run list, rerun without `--dry-run` only if the selected source directories are correct. K1 intentionally allows actual moves only for no-op selections. Imported, failed, broad, and latest/default archive selections remain inspect-only until a later policy bundle.

```bash
tul archive --noop --keep 3
```

A successful no-op move prints the moved count and records an `archive_last_run` summary in the latest remaining state.

Imported or failed state cleanup should still start with dry-run:

```bash
tul archive --imported --dry-run --keep 3
tul archive --failed --dry-run --keep 3
```

## Rules

- `--dry-run` prints what would move without moving files.
- `--noop` selects no-op states.
- `--imported` selects imported/validated states without commits.
- `--failed` selects failed states.
- `--keep N` keeps the newest N selected states and archives the older selected states.
- Latest state and latest rollbackable state are protected references and are skipped by the archive engine.
- Actual moves currently require an explicit `--noop` selector.
- Default/latest archive without a selector is refused in move mode.
- Imported, failed, mixed, and broad `--all` cleanup are diagnostic dry-run paths until separately authorized.
- Archive cleanup moves state directories to the configured archive root; it does not delete them.
