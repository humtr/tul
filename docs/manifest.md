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

## Artifact model

| Artifact | Role |
|---|---|
| Git remote + commit hash | canonical source/recovery authority |
| `tul-vf-latest.md` | runtime verification evidence |
| `tul-source-latest.zip` | source-context transport artifact |
| `tul-review-latest.zip` | changed-file review transport artifact |
| state/report/handoff files | local runtime records |

## Stage 7 closure

Stage 7 closes after these capabilities are in place and verified:

- explicit source export;
- explicit review export;
- export freshness diagnostics under `tul show exports`;
- automatic source/review refresh inside the normal loop;
- compact command surface without legacy top-level aliases;
- `tul run` as the single normal user loop;
- command-surface smoke checks in `tul verify fresh`;
- active-doc command-residue cleanup;
- conservative auxiliary commands: `clean`, `recover`, and `setup`.

The verified pre-closure baseline is `e965194ee8573b4a9938c87fab42b058ecf020b2`. The closure checkpoint records completion and moves planning to Stage 8.
