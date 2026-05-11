# tul commands

Default workflow:

```bash
tul update <project> -l
```

`-l` is the short form of `--latest`; it selects the newest matching package from configured inbox roots.

## Core loop

```bash
tul status tul
tul verify tul
tul verify tul --fresh-clone
tul package latest tul
tul update tul -l
tul state tul
```

## Package discovery and authoring

```bash
tul package list tul
tul package latest tul
tul package inspect /sdcard/Download/package.zip
tul package check /sdcard/Download/package.zip --target tul
```

Create a package skeleton:

```bash
tul package scaffold tul_example_v1 --target tul --message "Example package"
```

Create a root-correct zip:

```bash
tul package zip tul_example_v1 --out /sdcard/Download/tul_example_v1.zip
```

## Recovery/debug

Split commands are recovery/debug tools, not the default workflow:

```bash
tul import tul -l
tul state tul --all --limit 5
tul archive tul --noop --dry-run
tul rollback tul
tul resume tul
```
