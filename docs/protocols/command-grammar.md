# tul command grammar

This document defines the canonical terminal command grammar after the Stage 7 command-surface redesign.

## Canonical top-level commands

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

No legacy alias layer is part of the canonical grammar.

## Role boundaries

- `show`: read-only state and diagnostic output.
- `package`: package discovery, inspection, validation, and authoring helpers.
- `update`: package application, checks, commit, push, and remote-HEAD check.
- `verify`: repo verification. No-arg is quick/local; `fresh` writes uploadable verify artifacts.
- `export`: artifact creation only. Status inspection belongs to `show exports`.
- `run`: the full Terminal Update Loop.
- `clean`: cleanup planning by default; guarded moves only with `run` under the clean namespace.
- `recover`: recovery planning by default.
- `setup`: setup status by default; setup actions under `init`, `install`, and `use`.

## Normal commands

```bash
tul package
tul run
```

## Stepwise commands

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## Option policy

Prefer positional words for modes: `fresh`, `dry`, `run`, `source`, `review`, `exports`.

Keep `--` options for output format, explicit paths, and safety exceptions only:

```text
--json
--out
--no-commit
--no-push
--no-export
--force
--allow-dirty
```
