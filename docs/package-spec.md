# tul package spec

A normal LLM-to-terminal package is a cross-platform archive with this minimum structure:

```text
<package>.zip
  tul-package.yml
  README.md
  files/
    ... repo-relative files ...
```

The manifest must include:

```yaml
version: 1
name: example-package

target:
  project: tul
  repo: humtr/tul
  branch: main

apply:
  mode: copy
  files:
    - from: files/bin/tul
      to: bin/tul

commit:
  files:
    - bin/tul
  message: Example package
```

Only `apply.mode: copy` is supported by the safe default runtime.

## Directory copy safety

File-to-file copy is the default and preferred form. Directory copy is considered high risk and is rejected unless the apply item explicitly opts in:

```yaml
apply:
  mode: copy
  files:
    - from: files/docs/status
      to: docs/status
      allow_directory: true
```

When directory copy is enabled, every resulting destination file must still be listed in `commit.files`. This keeps the final staged set explicit and prevents broad package writes from becoming broad git staging.

Before copying, `tul update` builds an `apply-plan.json` under the package work directory. The plan records every destination, whether a backup will be created, and whether the operation came from a directory copy. The package is rejected before copying if any planned destination falls outside `commit.files` or duplicates another destination.

## Deletion boundary

The package mechanism does not currently support safe delete operations. A package may replace files through explicit copy items, but it must not pretend to delete obsolete files. Deletion work requires a separate narrow `git rm` plan or a future package contract extension for safe deletes.

For document compaction, this means:

```text
2A: update runtime pointers and active docs through copy-mode package
2B: remove obsolete compatibility docs through a separate narrow cleanup step
```

## Required package strings

Documentation and verification gates may refer to the exact contract phrase:

```text
tul-package.yml + files/ + README.md
```
