# LLM entrypoint for tul

You are reading the `humtr/tul` repository, the Terminal Update Loop runtime.

## Purpose

`tul` exists to make this loop fast and verifiable:

```text
LLM creates a cross-platform package
→ user downloads it
→ tul update
→ tul applies/checks/sweeps/commits/pushes/verifies
→ tul prints rollback instructions and compact handoff
→ the next LLM verifies remote state and proposes the next bounded package
```

## Fast start for a fresh LLM

Use this order unless the user gives a narrower task:

1. Check the latest user-provided `tul-vf-latest.md` artifact if present.
2. Check any pasted `tul state` output if the task involves state, rollback, cleanup, or handoff.
3. Read this file.
4. Read `docs/llm/post-update-review.md` for the review protocol.
5. Read `docs/status/current.md` and `docs/roadmap.md` for the current bundle boundary.
6. Read `docs/workflows/parallel-readiness.md` before proposing the next bounded bundle.
7. Read `docs/workflows/artifact-semantics.md` before treating any zip as review evidence, source evidence, or backup.
8. Read `docs/checklists/loop-runtime.md` for acceptance criteria.
9. Read implementation files only when generating or reviewing a package.

Do not ask for source context just to confirm a successful update when `tul-vf-latest.md` already proves release-gate status and includes runtime snapshots. Ask for standalone `tul state` or `tul handoff` only if the latest artifact is stale or missing those snapshots. Ask for source context when producing the next package or when the failure is code-level, and verify archive/root layout before using it. A GitHub-generated `tul-main.zip` can be manual source context, but it is not a tul runtime backup or a tul-proven explicit source export.

## Durable read order

1. `README.md`
2. `docs/manifest.md`
3. `docs/status/current.md`
4. `docs/strategy.md`
5. `docs/roadmap.md`
6. `docs/llm/post-update-review.md`
7. `docs/workflows/artifact-semantics.md`
8. `docs/learning-log.md`
9. `docs/decisions.md`
10. `docs/checklists/loop-runtime.md`
11. `docs/checklists/planning-harness.md`
12. `docs/protocols/planning-loop.md`
13. `docs/llm/commands.md`
14. `docs/protocols/llm-handoff-protocol.md`
15. `docs/protocols/command-grammar.md`
16. `docs/workflows/update-pipeline.md`
17. `docs/workflows/verify.md`
18. `docs/workflows/package-authoring.md`
19. `docs/workflows/state-cleanup.md`
20. `docs/workflows/parallel-readiness.md`
21. `docs/workflows/stage7-bounded-parallel-planning.md`

## Current self-host review loop

For normal review, expect the user to run:

```bash
tul package latest
tul update
```

Then the user should upload:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

A package is normally closed when the artifact shows `Release gate: PASS`, matching local/remote HEAD, clean working tree, py_compile pass, git diff check pass, and canonical verify artifact paths.

## Non-negotiable invariants

- `tul update` is the default full-loop command.
- Commit and push are included by default after validation.
- `--no-commit` and `--no-push` are recovery/debug exceptions.
- Remote HEAD verification is required when push is enabled.
- Never use `git add -A` or `git add .` in the normal update path.
- Never force push in the normal path.
- Project policy belongs in `.tul.yml`.
- Environment paths and project aliases belong in global config.
- LLM packages should be cross-platform `tul-package.yml + files/ + README.md` packages.

## Package selection

When the user has downloaded a package to configured inbox roots, prefer:

```bash
tul update
# or, when explicitness is useful:
tul update tul --latest
```

Use `--package PATH` only when the user wants to apply a specific file.

Do not ask the user to paste long absolute package paths when the package is already in a configured inbox root and `--latest` or native `tul update` is sufficient.

## Current planning mode

Stage 7 uses bounded parallel planning with sequential gated application. Read `docs/manifest.md`, `docs/strategy.md`, `docs/roadmap.md`, `docs/status/current.md`, `docs/learning-log.md`, `docs/decisions.md`, and `docs/workflows/stage7-bounded-parallel-planning.md` before proposing the next package.

The first Stage 7 package may be a large planning consolidation package because it owns the coordination docs and excludes runtime behavior changes. Later packages should be smaller bounded bundles with clear success gates.


## Source context handoff

For compact change review, prefer the explicit review bundle:

```bash
tul export review
```

For package generation or code-level diagnosis, ask for source context when needed and verify its root layout before use. A GitHub-generated `tul-main.zip` is acceptable manual source context when it plausibly corresponds to the verified HEAD, but it is not a tul runtime backup or a tul-proven explicit source export. A future explicit `tul export source` command may replace this ambiguity, but it is not implemented yet and must not be suggested as a runnable command.

## Stage 7 planning checkpoint

Before proposing implementation work, read `docs/workflows/stage7-bounded-parallel-planning.md` and confirm the latest `tul-vf-latest.md` release gate is PASS. Treat Stage 6 as closed only when the runtime artifact confirms the Stage 6 stabilization checkpoint commit.


## Stage 7 gate reference

Before generating a Stage 7 package, read `docs/checklists/stage7-package-gates.md`. Do not implement `tul export source` until `docs/workflows/source-export-spec.md` is accepted by the latest verified baseline and the package is explicitly classified Orange.
