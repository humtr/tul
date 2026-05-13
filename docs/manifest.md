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
- `update`: apply package, commit, push, remote-HEAD check.
- `verify`: quick/local verification by default; `fresh` writes uploadable verify artifacts.
- `export`: file creation only.
- `run`: full Terminal Update Loop.
- `clean`: cleanup planning by default.
- `recover`: recovery planning by default.
- `setup`: setup status by default.

## Normal user loop

```bash
tul package
tul run
```
