# tul

`tul` means **Terminal Update Loop**.

`tul` is a local, human-controlled runtime for moving AI-generated work through this loop:

```text
LLM / assistant -> user -> terminal environment -> local repo/runtime -> commit + push -> verification/export -> LLM review
```

The current operational target is **`humtr/tul`** itself. Future target repositories remain deferred until this self-hosting loop reduces bridge work rather than multiplies it.

## Normal use

For ordinary operation, run one command from the repo:

```bash
cd ~/prj/tul

tul run
```

`tul run` performs the full user-facing loop:

```text
package found:
  update -> export -> verify fresh -> show

package not found:
  export -> verify fresh -> show
```

A successful run prepares the normal upload artifacts:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-source-latest.zip
/sdcard/termux/import/tul/tul-review-latest.zip
```

Use `tul package` only when you want to inspect the newest compatible package before running the loop.

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

Command boundaries:

- `tul show` is read-only state and diagnostic output. Use `tul show exports` for source/review freshness.
- `tul package` discovers, inspects, validates, and authors packages. With no arguments, it shows the newest compatible package candidate.
- `tul update` applies a package, runs safety checks, commits, pushes, and verifies remote HEAD.
- `tul verify` is quick/local and stdout-first. It does not rewrite latest verify artifacts by default.
- `tul verify fresh` performs fresh clone verification and writes `tul-vf-latest.md/json`.
- `tul export` creates source and review transport artifacts.
- `tul run` is the full Terminal Update Loop.
- `tul clean` is plan-only by default; `tul clean ... run` performs guarded moves.
- `tul recover` prints recovery plans by default and does not silently mutate the repo.
- `tul setup` reports setup status by default; setup subcommands perform setup tasks.

## LLM entrypoint

If you are an LLM, coding agent, or a new session reviewing this repo, start here:

1. Read `tul-vf-latest.md` when the user uploads it.
2. Read [`README.md`](README.md).
3. Read [`docs/status/current.md`](docs/status/current.md).
4. Read [`docs/manifest.md`](docs/manifest.md).
5. Read [`docs/roadmap.md`](docs/roadmap.md).
6. Read [`docs/commands.md`](docs/commands.md).
7. Read [`docs/package-spec.md`](docs/package-spec.md) before proposing or producing a package.

Do not rely on prior chat context when repo documents and runtime artifacts answer the question. Runtime facts live in `tul-vf-latest.md` and `tul show` snapshots, not in README prose.

## Artifact model

| Artifact | Role |
|---|---|
| Git remote + commit hash | canonical source/recovery authority |
| `tul-vf-latest.md` | runtime verification evidence |
| `tul-source-latest.zip` | source-context transport artifact |
| `tul-review-latest.zip` | changed-file review transport artifact |
| state/report/handoff files | local runtime records |

Zip artifacts are not backup authority. Recovery authority is Git remote plus commit hashes and recovery state.

Use `tul show exports` to inspect source/review freshness:

```bash
tul show exports
```

## Package contract

LLM-generated packages must converge on one cross-platform zip. The minimum package contract is `tul-package.yml + files/ + README.md`; normal cross-platform packages may also include helper scripts when explicitly needed:

```text
<package>.zip
  tul-package.yml
  README.md
  files/
```

`tul-package.yml` must declare target project/repo/branch, apply files, commit files, and commit message. Normal operation uses package metadata, not arbitrary script execution.

## Non-negotiable invariants

- User approval remains required before applying generated packages.
- Normal package application must not use `git add -A` or `git add .`.
- Force push is forbidden in normal operation.
- Push is included by default after successful validation and commit.
- `--no-push` and `--no-commit` are exceptions for recovery/debug.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- LLM packages should use `tul-package.yml + files/ + README.md`.

## Planning harness

The active planning ledger is repo-resident:

```text
docs/manifest.md
docs/roadmap.md
docs/status/current.md
docs/learning-log.md
docs/decisions.md
```

`docs/decisions.md` and `docs/learning-log.md` preserve rationale and lessons, but they are not part of the default read-next path.

## Current focus

Stage 7 is closed. Stage 8 is compacting active documentation ownership. Package `tul-doc-tree-compaction-stage2-pointer-compaction-v1` narrows runtime handoff and verify required-doc pointers to the active document set. The separate 2B deletion step removes retired compatibility and obsolete documentation from the active tree.
