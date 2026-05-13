# tul package spec

This document owns the package contract for `tul`.

## Normal package structure

A normal LLM-to-terminal package is a cross-platform archive with this structure:

```text
<package>.zip
  tul-package.yml
  README.md
  files/
```

Optional helper scripts may be included:

```text
  apply.sh
  apply.ps1
```

The safe runtime path uses `tul-package.yml` metadata with `apply.mode: copy`; arbitrary helper scripts are not the normal application mechanism.

## Manifest contract

Example:

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
    - from: files/docs/commands.md
      to: docs/commands.md

commit:
  files:
    - docs/commands.md
  message: Example package
```

Required properties:

- `version: 1`
- `name`
- `target.project`
- `target.repo`
- `target.branch`
- `apply.mode: copy`
- explicit `apply.files`
- explicit `commit.files`
- `commit.message`

Every applied destination must be listed in `commit.files`.

## Directory copy safety

File-to-file copy is preferred. Directory copy is high-risk and rejected unless an apply item explicitly opts in:

```yaml
apply:
  mode: copy
  files:
    - from: files/docs/llm
      to: docs/llm
      allow_directory: true
```

When directory copy is enabled, every resulting destination file must still be listed in `commit.files`.

## Staging safety

Normal package application must not use:

```bash
git add -A
git add .
```

Only the manifest-declared `commit.files` should be staged.

## Package scope rules

Good packages are small, explicit, and independently verifiable.

- Keep code and documentation changes separated unless one cannot be validated without the other.
- Avoid broad rewrites when a bounded replacement is enough.
- Do not modify runtime command behavior in a documentation-only package.
- Do not change package contract and package content in the same package unless the contract change is the package's explicit purpose.
- Preserve rollback through Git commit hashes and runtime recovery state.

## Current deletion limitation

The safe default package path supports copy operations. It does not provide a separate delete operation in `apply.mode: copy`.

Therefore document-tree compaction should be staged as:

1. merge active content into canonical docs;
2. keep runtime-referenced compatibility docs until pointers are narrowed;
3. delete obsolete docs only through a follow-up package or manual step that explicitly handles deletions and validation.

Do not fake deletion by hiding broad behavior in helper scripts.

## Acceptance gate

Before considering a package ready:

- manifest target must match the active project/repo/branch;
- `apply.files` and `commit.files` must match exactly;
- package README must state scope, non-goals, expected result, and validation;
- no broad staging or force push is allowed;
- `tul verify fresh` or `tul run` must pass after application.
