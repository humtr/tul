# State cleanup workflow

`tul` keeps work state under the configured `platform.work_root`. Repeated package testing can create many no-op or imported states. These records are useful while debugging, but they should be easy to inspect and archive without deleting evidence.

## Recommended commands

```bash
tul state tul
tul state tul --all --limit 5
tul archive tul --noop --dry-run
tul archive tul --noop --keep 3
tul archive tul --imported --dry-run
```

Rules:

- `tul state <project>` shows the latest state only.
- `tul state <project> --all --limit N` shows the newest N matching states.
- `tul archive <project> --noop --keep N` archives older no-op states while keeping the newest N.
- `tul archive <project> --imported` archives imported/validated states that do not contain commits.
- `--dry-run` prints what would move without moving files.
- Published rollbackable states are not removed by `--noop` or `--imported`.
