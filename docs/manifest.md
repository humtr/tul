# manifest

`tul` is the Terminal Update Loop runtime for applying LLM-generated packages under user control.

## Durable invariants

- User approval remains required before applying generated packages.
- Normal package application must not use `git add -A` or `git add .`.
- Force push is forbidden in normal operation.
- Push is included by default after successful validation and commit.
- `--no-push` and `--no-commit` are recovery/debug exceptions, not the normal path.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- Zip artifacts are transport artifacts, not backup authority.
- Recovery authority is Git remote + commit hash + rollback/recovery state.
- Parallel planning is allowed; mutating package application is sequential and gated.

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

Command ownership:

- `show`: read-only state, history, handoff, exports, and diagnostic output.
- `package`: package discovery, inspection, validation, and authoring.
- `update`: apply one package, run safety checks, commit, push, and remote-HEAD check.
- `verify`: quick/local verification by default; `verify fresh` writes uploadable verification artifacts.
- `export`: file creation only; status-only behavior belongs under `show`.
- `run`: normal full Terminal Update Loop.
- `clean`: cleanup planning by default; guarded mutation requires explicit action.
- `recover`: recovery planning by default; rollback requires explicit action.
- `setup`: setup status by default; setup subcommands perform setup tasks.

## Normal user loop

```bash
tul run
```

`run` owns the normal user-facing loop. If a compatible package is available, it updates first. If no compatible package is available, it refreshes source/review/verify artifacts for the current HEAD.

## Stepwise diagnostic loop

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Use the stepwise loop only for diagnostics, review, recovery, or explicit user-directed decomposition.

## Artifact authority

| Artifact | Authority |
|---|---|
| Git remote + commit hash | source and recovery authority |
| `tul-vf-latest.md` | latest verification evidence |
| `tul-source-latest.zip` | full source transport artifact |
| `tul-review-latest.zip` | changed-file review transport artifact |
| local state/report/handoff files | runtime records, not backup authority |

Source/review bundles are current only when `tul show exports` reports them current for the active HEAD.

## Package ownership

The package contract is owned by `docs/package-spec.md`.

Minimum package structure:

```text
<package>.zip
  tul-package.yml
  README.md
  files/
```

Normal packages use `apply.mode: copy`. Every destination must be covered by `commit.files`; this preserves explicit staging and prevents broad package writes from becoming broad git staging.

## Documentation ownership

Active durable docs are:

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

Rationale and lessons are retained in:

```text
docs/decisions.md
docs/learning-log.md
```

Compatibility docs under `docs/llm`, `docs/protocols`, selected `docs/checklists`, and selected `docs/workflows` may remain temporarily while runtime handoff/verify pointers still reference them. They are not independent sources of truth once merged into the active docs.
