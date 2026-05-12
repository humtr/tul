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
2. Read [`docs/llm/post-update-review.md`](docs/llm/post-update-review.md) when reviewing a just-applied package or verify artifact.
3. Read [`docs/manifest.md`](docs/manifest.md) for vision, invariants, and change rules.
4. Read [`docs/status/current.md`](docs/status/current.md) for the current checkpoint.
5. Read [`docs/strategy.md`](docs/strategy.md) for the medium-term capability map.
6. Read [`docs/roadmap.md`](docs/roadmap.md) for the short-term ready queue and bundle candidates.
7. Read [`docs/workflows/parallel-readiness.md`](docs/workflows/parallel-readiness.md) before proposing the next bounded bundle.
8. Read [`docs/workflows/artifact-semantics.md`](docs/workflows/artifact-semantics.md) before treating any zip as review evidence, source evidence, or backup.
9. Read [`docs/learning-log.md`](docs/learning-log.md) for bottom-up lessons.
10. Read [`docs/decisions.md`](docs/decisions.md) for accepted planning decisions.
11. Read [`docs/checklists/loop-runtime.md`](docs/checklists/loop-runtime.md) and [`docs/checklists/planning-harness.md`](docs/checklists/planning-harness.md).
12. Read [`docs/protocols/llm-handoff-protocol.md`](docs/protocols/llm-handoff-protocol.md), [`docs/protocols/command-grammar.md`](docs/protocols/command-grammar.md), and [`docs/protocols/planning-loop.md`](docs/protocols/planning-loop.md) when relevant.

Do not rely on prior chat context when the repo documents answer the question. Do not treat web raw-view oddities as proof that files are broken; inspect GitHub file/blob view or use fresh clone checks for line counts and syntax.

For normal post-update review, the single upload artifact is `/sdcard/termux/import/tul/tul-vf-latest.md`. It includes the release gate plus compact `tul state` and `tul handoff` snapshots. Source/review zip export semantics are currently under correction; do not treat `tul-main.zip` as canonical backup, as a successful update artifact, or as verified source evidence. See [`docs/workflows/artifact-semantics.md`](docs/workflows/artifact-semantics.md).

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

Stage 6 introduces native project context in bounded steps. The current model supports an active project, read-only no-arg commands, `tul verify fresh`, and guarded no-arg `tul update` / `tul import` / `tul rollback` when the project can be inferred safely:

```bash
tul use tul
tul current
tul status
tul update
tul verify fresh
tul state
```

No-arg mutating commands use explicit context guards. If the active project differs from the current-directory project, `tul` refuses to continue and prints concrete choices such as `tul update tul`, `tul update <cwd-project>`, or `tul use <cwd-project>`.

Package-target mismatch guidance remains a later bundle: the package manifest is already enforced, but richer explanations for incompatible downloaded zip files are still pending.

## Default command model

## Launcher / install sync

Operational commands should be runnable from any directory once native context is set:

```bash
tul use tul
tul status
tul update
tul verify fresh
tul state
tul handoff
```

Explicit project arguments remain supported for clarity, recovery, and ambiguous contexts.

If `tul` on PATH behaves differently from `python ~/prj/tul/bin/tul`, the user launcher is stale. Resync it with:

```bash
tul install tul
# or, if the PATH launcher is too old to know install:
python ~/prj/tul/bin/tul install tul
```

Use `tul doctor tul` to compare the PATH launcher with the repo launcher.

Use the full-loop command:

```bash
tul update
```

`update` infers the project from explicit target, current directory, active project, default project, or the only configured project. It then selects the newest matching package from configured inbox roots. The explicit forms remain valid:

```bash
tul update <project>
tul update <project> --latest
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

## Current handoff artifacts

The normal post-update review artifact is:

- `/sdcard/termux/import/tul/tul-vf-latest.md`

It contains release-gate evidence plus compact runtime snapshots. Zip artifacts are not backups and are not automatically trusted as canonical source evidence. The Stage 6 artifact model now separates:

- verify artifact: release-gate evidence;
- review bundle: future compact diff-oriented upload artifact;
- source bundle: future explicit full source context for package generation;
- backup: Git remote, commit hashes, and rollback state.

See [`docs/workflows/artifact-semantics.md`](docs/workflows/artifact-semantics.md). Until the export model is corrected, ask for a repo/source zip only when package generation or code-level diagnosis actually needs it, and verify its root layout before using it.
