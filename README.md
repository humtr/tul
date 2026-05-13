# tul

`tul` means **Terminal Update Loop**.

`tul` is a local, human-controlled runtime for safely moving AI-generated work through this loop:

```text
LLM / assistant -> user -> terminal environment -> local repo/runtime -> commit + push -> verification/export -> LLM review
```

The current operational target is **`humtr/tul`** itself. Future target repositories remain deferred until this self-hosting loop is stable enough to reduce bridge work rather than multiply it.

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

There is no legacy alias layer in the canonical Stage 7 command surface.

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

Auxiliary command defaults are intentionally conservative:

```text
tul clean    = plan-only cleanup summary
tul recover  = recovery plan only; no silent rollback
tul setup    = setup status only
```

Use explicit subcommands for bounded action, for example `tul clean states run`, `tul recover rollback`, or `tul setup use <project>`.

## Stepwise loop

Use this only for diagnostics or when the user explicitly wants to split the loop:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## LLM entrypoint

If you are an LLM, coding agent, or a new session reviewing this repo, start here:

1. Read `tul-vf-latest.md` when the user uploads it.
2. Read [`docs/llm/entrypoint.md`](docs/llm/entrypoint.md).
3. Read [`docs/status/current.md`](docs/status/current.md).
4. Read [`docs/roadmap.md`](docs/roadmap.md).
5. Read [`docs/manifest.md`](docs/manifest.md).
6. Read [`docs/llm/commands.md`](docs/llm/commands.md).
7. Read [`docs/protocols/command-grammar.md`](docs/protocols/command-grammar.md).
8. Read [`docs/checklists/loop-runtime.md`](docs/checklists/loop-runtime.md) and [`docs/checklists/stage7-package-gates.md`](docs/checklists/stage7-package-gates.md) before declaring a bundle safe.

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

LLM-generated packages must converge on one cross-platform zip. The minimum package contract is `tul-package.yml + files/ + README.md`; normal cross-platform packages also include `apply.sh` and `apply.ps1`:

```text
<package>.zip
  tul-package.yml
  README.md
  files/
  apply.sh
  apply.ps1
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
- LLM packages should use `tul-package.yml + README.md + files/ + apply.sh + apply.ps1`.

## Planning harness

The durable planning ledger is repo-resident:

```text
docs/manifest.md
docs/strategy.md
docs/roadmap.md
docs/status/current.md
docs/learning-log.md
docs/decisions.md
```

Stage 7 uses parallel planning and sequential gated update: many candidate plans may be drafted, but only one package is applied against the latest verified baseline at a time.

## Current focus

Stage 7 has closed command-surface redesign, run default finalization, README package-contract gate fix, run smoke gate, and command residue cleanup. The current work tightens the auxiliary `clean`, `recover`, and `setup` commands before the Stage 7 closure checkpoint.

## Current focus

Stage 7 is closed by the closure checkpoint once `tul verify fresh` reports the 33-step release gate PASS after applying it. The next work should begin Stage 8 planning: gate hardening, a lightweight smoke-test harness, and retired-module review.
