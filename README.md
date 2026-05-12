# tul

`tul` means **Terminal Update Loop**.

`tul` is a local, human-controlled runtime for safely moving AI-generated work through this loop:

```text
LLM / assistant → user → terminal environment → local repo/runtime → commit + push → remote verification → LLM handoff
```

The first operational target is **`humtr/ai`**. This repo, **`humtr/tul`**, is the self-hosting tooling repo that makes the loop reliable across Windows, Termux, GitHub, and LLM-assisted sessions.

## LLM entrypoint

If you are an LLM, coding agent, or a new session reviewing this repo, start here:

1. Read [`docs/llm/entrypoint.md`](docs/llm/entrypoint.md).
2. Read [`docs/manifest.md`](docs/manifest.md) for vision, invariants, and change rules.
3. Read [`docs/status/current.md`](docs/status/current.md) for the current checkpoint.
4. Read [`docs/strategy.md`](docs/strategy.md) for the medium-term capability map.
5. Read [`docs/roadmap.md`](docs/roadmap.md) for the short-term ready queue and bundle candidates.
6. Read [`docs/learning-log.md`](docs/learning-log.md) for bottom-up lessons.
7. Read [`docs/decisions.md`](docs/decisions.md) for accepted planning decisions.
8. Read [`docs/checklists/loop-runtime.md`](docs/checklists/loop-runtime.md) and [`docs/checklists/planning-harness.md`](docs/checklists/planning-harness.md).
9. Read [`docs/protocols/llm-handoff-protocol.md`](docs/protocols/llm-handoff-protocol.md), [`docs/protocols/command-grammar.md`](docs/protocols/command-grammar.md), and [`docs/protocols/planning-loop.md`](docs/protocols/planning-loop.md) when relevant.

Do not rely on prior chat context when the repo documents answer the question. Do not treat web raw-view oddities as proof that files are broken; inspect GitHub file/blob view or use fresh clone checks for line counts and syntax.

## Project identity

`tul` applies standardized LLM-generated packages, validates them, commits them, pushes them, verifies remote HEAD, prints rollback guidance, and generates an LLM-ready handoff.

The durable project contract lives in repo documents. Runtime facts live in terminal handoff output.

## Planning harness

README is the entrypoint, not the full planning ledger. For Stage 6 and later, tul uses a repo-resident planning harness:

```text
manifest → strategy → roadmap → status → learning log → decisions
```

- [`docs/manifest.md`](docs/manifest.md) states the vision, invariants, human role, and manifest change rules.
- [`docs/strategy.md`](docs/strategy.md) tracks medium-term capability areas and maturity.
- [`docs/roadmap.md`](docs/roadmap.md) holds the short-term ready queue and bundle candidates.
- [`docs/status/current.md`](docs/status/current.md) records the current checkpoint and next package.
- [`docs/learning-log.md`](docs/learning-log.md) records bottom-up lessons from updates.
- [`docs/decisions.md`](docs/decisions.md) records accepted planning decisions.

The same harness should be portable to future target repositories such as `humtr/ai`, but `humtr/ai` onboarding remains **Stage X** until tul's self-host loop is sufficiently stable.


## Non-negotiable invariants

- `tul update <project>` is the default full-loop command.
- Push is included by default after successful validation and commit.
- `--no-push` and `--no-commit` are exceptions for debugging or recovery.
- Remote HEAD verification is part of successful update when push is enabled.
- Do not use `git add -A` or `git add .` in the normal update path.
- Do not force push in the normal path.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- LLM packages should use `tul-package.yml + files/ + README.md`.


## Native context

Stage 6 introduces native project context in bounded steps. The first step stores the active project without changing update semantics:

```bash
tul use tul
tul current
tul projects
```

For now, mutating commands still require an explicit target:

```bash
tul update tul -l
tul verify tul --fresh-clone
```

Later bundles will add safe no-arg read-only commands, `tul verify fresh`, and finally guarded no-arg update.

## Default command model

## Launcher / install sync

Operational commands should be runnable from any directory through the configured project alias:

```bash
tul status tul
tul update tul --latest
tul state tul
tul handoff tul
```

If `tul` on PATH behaves differently from `python ~/prj/tul/bin/tul`, the user launcher is stale. Resync it with:

```bash
tul install tul
# or, if the PATH launcher is too old to know install:
python ~/prj/tul/bin/tul install tul
```

Use `tul doctor tul` to compare the PATH launcher with the repo launcher.

Use the full-loop command:

```bash
tul update <project>
```

When the package has already been downloaded into a configured inbox root, use the explicit latest form:

```bash
tul update <project> --latest
# or
tul update <project> -l
```

`--latest` scans configured `platform.inbox_roots` and selects the newest package whose manifest matches the target project/repo/branch. It does **not** scan work/archive roots, because those can contain stale or already-applied copies.

For an exact file path, use:

```bash
tul update <project> --package /path/to/package.zip
```

The update loop is expected to:

```text
sync precheck
→ import package
→ validate manifest
→ safe apply
→ check
→ sweep repo-local backups
→ verify changed files
→ stage intended files only
→ staged check
→ commit
→ push
→ verify remote HEAD
→ print rollback instructions
→ write report/state/handoff
→ print compact LLM handoff
```

Split commands exist for debugging, recovery, and manual intervention. They must not replace the default full loop.

## Runtime facts

Do not treat README text as proof that a package was applied or pushed. Runtime facts belong in `tul handoff` output:

- commit hash;
- push verified;
- remote HEAD after fetch;
- rollback command;
- state path;
- report path;
- working tree status.

Use compact handoff by default:

```bash
tul handoff tul
```

Use full handoff only when the receiving LLM needs the protocol inline:

```bash
tul handoff tul --full
```

Print copy-ready project instructions with:

```bash
tul instructions
# or
tul handoff tul --instructions
```

## Package contract

LLM-generated packages should converge on one cross-platform zip:

```text
<package>.zip
  tul-package.yml
  files/
    ... repo-relative files ...
  README.md
```

Bootstrap fallback scripts may be included during transition:

```text
apply.sh
apply.ps1
```

Normal operation should use `tul-package.yml`, not arbitrary script execution.
