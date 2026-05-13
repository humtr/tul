# commands

This document is the canonical command-surface reference for `tul`.

## Canonical command surface

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

There is no legacy alias layer in the canonical command surface.

## Normal user loop

```bash
tul run
```

`run` is the ordinary user-facing command.

```text
package found:
  update -> export -> verify fresh -> show

package not found:
  export -> verify fresh -> show
```

## Command boundaries

### `tul show`

Read-only state and diagnostic output.

Common uses:

```bash
tul show
tul show exports
tul show handoff
tul show history 5
tul show --json
```

State queries belong under `show`, not `export`.

### `tul package`

Package discovery, inspection, validation, and authoring.

Common uses:

```bash
tul package
tul package list tul
tul package inspect <package.zip>
tul package check <package.zip> tul
```

With no arguments, `tul package` reports the newest compatible package candidate for the inferred project/repo/branch.

### `tul update`

Applies one compatible package, runs safety checks, commits, pushes, and verifies remote HEAD when push is enabled.

Normal package application must stage only the explicit `commit.files` from `tul-package.yml`. Do not use `git add -A` or `git add .` in the normal path.

### `tul verify`

Quick/local verification by default.

```bash
tul verify
tul verify fresh
```

`verify fresh` performs fresh clone verification and writes uploadable latest verification artifacts.

### `tul export`

File creation only.

```bash
tul export source
tul export review
```

Use `tul show exports` for source/review status. `tul export status` is intentionally outside the canonical namespace.

### `tul run`

Full Terminal Update Loop. This is the default command for ordinary use.

### `tul clean`

Plan-only by default. Guarded mutation requires an explicit action such as:

```bash
tul clean states run
```

### `tul recover`

Recovery planning by default. Mutating recovery requires an explicit action such as:

```bash
tul recover rollback
```

### `tul setup`

Setup status by default. Setup subcommands perform setup tasks such as project selection or initialization.

## Stepwise diagnostic loop

Use this only when splitting the normal loop is useful:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## Acceptance boundaries

- `show` reads.
- `export` writes files but does not mutate repo history.
- `package` inspects or prepares packages.
- `update` mutates repo files and Git history.
- `run` may mutate when a compatible package is available.
- `clean`, `recover`, and `setup` are conservative by default and require explicit subcommands for mutation.
