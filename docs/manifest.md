# manifest

`tul` is the Terminal Update Loop runtime for applying LLM-generated packages under user control.

## Invariants

- User approval remains required before applying generated packages.
- Normal package application must not use `git add -A` or `git add .`.
- Force push is forbidden in normal operation.
- Push is included by default after successful validation and commit.
- Project policy belongs in `.tul.yml`.
- Environment paths belong in global config.
- Zip artifacts are not backup authority. Recovery authority is Git remote + commit hash + rollback/recovery state.
- Parallel planning is allowed; update/apply work remains sequential and gated against the latest verified baseline.

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

## Active document ownership

Default LLM read-next is limited to:

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

Ownership:

| File | Owns |
|---|---|
| `README.md` | user/LLM entrypoint and artifact model summary |
| `docs/status/current.md` | current verified state and immediate queue |
| `docs/manifest.md` | durable invariants |
| `docs/roadmap.md` | future queue and deferred work |
| `docs/commands.md` | command grammar and command boundaries |
| `docs/package-spec.md` | package contract and package safety |

`docs/decisions.md` and `docs/learning-log.md` preserve rationale and lessons. They are not default read-next docs.

## Package contract

The package contract is owned by `docs/package-spec.md`.

The minimum structure is:

```text
tul-package.yml + files/ + README.md
```

## Artifact model

| Artifact | Role |
|---|---|
| Git remote + commit hash | canonical source/recovery authority |
| `tul-vf-latest.md` | runtime verification evidence |
| `tul-source-latest.zip` | source-context transport artifact |
| `tul-review-latest.zip` | changed-file review transport artifact |
| state/report/handoff files | local runtime records |

## Stage status

Stage 7 is closed. Stage 8 has reduced active documentation ownership and moved runtime pointers to the active documentation set; 2B removes retired compatibility and obsolete docs from the active tree.
