# command grammar

Stage 7 canonical top-level commands:

```text
show package update verify export run clean recover setup
```

## Default meanings

- `tul show`: read-only state, export, and next-action summary.
- `tul package`: newest compatible package candidate.
- `tul update`: apply package, commit, push, remote-HEAD check.
- `tul verify`: quick/local verification.
- `tul verify fresh`: fresh clone verification and latest verify artifacts.
- `tul export`: create source and review transport artifacts.
- `tul run`: normal full Terminal Update Loop.
- `tul clean`: cleanup plan.
- `tul recover`: recovery plan.
- `tul setup`: setup status.

## Normal loop

```bash
tul run
```

`run` handles package-present and package-absent cases.

## Flag policy

Use positional words for common modes. Reserve flags for paths, machine output, and exceptional behavior:

```text
--json
--out
--no-push
--no-commit
--no-export
--force
--allow-dirty
```

## Removed old grammar

Do not use old top-level command grammar in active instructions. Historical docs may mention it only when clearly marked historical.
