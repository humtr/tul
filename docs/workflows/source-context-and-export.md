# source context and export

`source context` is the repo file content needed for code review or package generation.

## Normal source baseline

```bash
tul export source
```

This writes:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
```

The source zip has repo files at the zip root plus source metadata files.

## Normal loop

```bash
tul run
```

`run` should keep source and review artifacts current.

## Status

```bash
tul show exports
```

Shows whether the source/review artifacts are current, stale, missing, invalid, or unrecorded.

## GitHub comparison

For source-export implementation changes, command-surface redesigns, or suspected file omission, compare:

```text
git rev-parse HEAD
git rev-parse origin/main
git ls-files
source-file-list.txt
```
