# tul

`tul` means **Terminal Update Loop**.

`tul` is a local, human-controlled runtime for moving LLM-generated work through a bounded loop:

```text
LLM / assistant -> user -> terminal -> local repo/runtime -> commit + push -> verification/export -> LLM review
```

The current operational target is **`humtr/tul`**. Future target repositories remain deferred until this self-hosting loop reliably reduces bridge work.

## Normal use

For ordinary operation, run one command from the repo:

```bash
cd ~/prj/tul

tul run
```

`tul run` is the default user loop:

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

Use split commands only for inspection, diagnostics, recovery, or explicit user-directed decomposition.

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

Command boundaries:

- `tul show` is read-only state and diagnostic output. Use `tul show exports` to inspect source/review freshness.
- `tul package` discovers, inspects, validates, and authors packages. With no arguments, it shows the newest compatible package candidate.
- `tul update` applies one compatible package, runs safety checks, commits, pushes, and verifies remote HEAD.
- `tul verify` is quick/local and stdout-first. `tul verify fresh` performs fresh clone verification and writes `tul-vf-latest.md/json`.
- `tul export` creates file artifacts only. Status belongs under `tul show`, not `tul export`.
- `tul run` is the full Terminal Update Loop.
- `tul clean` is plan-only by default; guarded mutation requires an explicit `run` subcommand.
- `tul recover` prints recovery plans by default; rollback requires an explicit subcommand.
- `tul setup` reports setup status by default; setup subcommands perform setup tasks.

## LLM read-next

When reviewing the repo from uploaded artifacts, use this order:

```text
1. tul-vf-latest.md
2. README.md
3. docs/status/current.md
4. docs/manifest.md
5. docs/roadmap.md
6. docs/commands.md
```

Read `docs/package-spec.md` only when producing or reviewing a package. Read `docs/decisions.md` or `docs/learning-log.md` only when design rationale or lessons are needed.

Do not rely on prior chat context when repo documents and runtime artifacts answer the question. Runtime facts live in `tul-vf-latest.md` and `tul show` snapshots, not in README prose.

## Artifact model

| Artifact | Role |
|---|---|
| Git remote + commit hash | canonical source/recovery authority |
| `tul-vf-latest.md` | runtime verification evidence |
| `tul-source-latest.zip` | source-context transport artifact |
| `tul-review-latest.zip` | changed-file review transport artifact |
| state/report/handoff files | local runtime records |

Zip artifacts are transport artifacts, not backup authority. Recovery authority is Git remote plus commit hashes and recovery state.

Use `tul show exports` to inspect source/review freshness:

```bash
tul show exports
```

## Package contract

LLM-generated packages must converge on one cross-platform archive. The package contract is:

```text
<package>.zip
  tul-package.yml
  README.md
  files/
```

Normal cross-platform packages may also include `apply.sh` and `apply.ps1` as human-readable helpers, but the safe runtime path is package metadata with `apply.mode: copy`.

`tul-package.yml` must declare target project/repo/branch, apply files, commit files, and commit message. Normal operation uses package metadata, not arbitrary script execution.

## Non-negotiable invariants

- User approval remains required before applying generated packages.
- Normal package application must not use `git add -A` or `git add .`.
- Force push is forbidden in normal operation.
- Push is included by default after successful validation and commit.
- `--no-push` and `--no-commit` are exceptions for recovery/debug.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- Parallel planning is allowed; package application is sequential and gated against the latest verified baseline.

## Current focus

Stage 7 is closed. The current work is Stage 8 document-tree compaction: reduce active documentation ownership, remove duplicated guidance, and keep runtime-facing read-next guidance narrow without changing command behavior.
