# manifest

`tul` is the Terminal Update Loop runtime for applying LLM-generated packages under user control.

## Invariants

- User approval remains required before applying generated packages.
- Normal package application must not use `git add -A` or `git add .`.
- Force push is forbidden in normal operation.
- Project policy belongs in `.tul.yml`.
- Environment paths belong in global config.
- Zip artifacts are not backup authority. Recovery authority is Git remote + commit hash + rollback/recovery state.

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

## Command meanings

- `show`: read-only state and diagnostic output.
- `package`: package discovery, inspection, validation, and authoring.
- `update`: apply package, run safety checks, commit, push, and remote-HEAD check.
- `verify`: quick/local verification by default; `fresh` writes uploadable verify artifacts.
- `export`: file creation only; no status-only subcommands live here.
- `run`: the normal full Terminal Update Loop.
- `clean`: cleanup planning by default.
- `recover`: recovery planning by default.
- `setup`: setup status by default.

## Normal user loop

```bash
tul run
```

`run` is responsible for the whole user-facing loop. If a compatible package is available, it updates first. If no compatible package is available, it refreshes source/review/verify artifacts for the current HEAD.

## Stepwise loop

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Use the stepwise loop only for debugging, review, or user-directed decomposition.

## Current baseline

The command-surface redesign, run default finalization, README package-contract gate fix, run smoke gate, and command residue cleanup are closed at `8534311ce661c5ffee34b638705a61a6e4d84874`. The next package tightens the auxiliary `clean`, `recover`, and `setup` UX before the Stage 7 closure checkpoint.
