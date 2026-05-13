# source export spec

`source export` creates a full source-context transport artifact.

## Command

```bash
tul export source
```

Default output:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
```

## Layout

The zip root must contain repo files directly, not a wrapper directory.

Required metadata:

```text
source-manifest.json
source-file-list.txt
source-file-sha256s.txt
```

## Exclusions

Exclude:

```text
.git
__pycache__
.pytest_cache
node_modules
dist
build
work
archive
logs
*.pyc
*.zip
*.bak
```

## Freshness

Use `tul show exports` to compare source manifest HEAD with current HEAD. Freshness warnings are advisory unless explicitly promoted to release-gate criteria.
