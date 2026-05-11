# Commands

Primary loop:

```bash
tul update <project>
tul update <project> -l
tul update <project> --latest
```

Package discovery:

```bash
tul package latest tul
tul package list tul
tul package inspect /path/to/package.zip
tul update tul --latest --dry-run
```

Package authoring:

```bash
tul package scaffold NAME --target tul --message "Commit message"
tul package add NAME --target tul FILE [FILE...]
tul package summary NAME
tul package zip NAME --out /sdcard/Download/NAME.zip --force
tul package check /sdcard/Download/NAME.zip --target tul
```

Verification:

```bash
tul verify tul
tul verify tul --fresh-clone
```

Recovery/debug:

```bash
tul state tul
tul state tul --all --limit 5
tul archive tul --noop --dry-run
tul rollback tul
tul import tul -l
```

Split commands are recovery/debug tools. The default workflow remains `tul update <project> -l`.
