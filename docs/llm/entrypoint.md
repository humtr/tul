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
7. Read `docs/checklists/loop-runtime.md` for acceptance criteria.
8. Read implementation files only when generating or reviewing a package.

Do not ask for a repo zip just to confirm a successful update when `tul-vf-latest.md` already proves release-gate status and includes runtime snapshots. Ask for standalone `tul state` or `tul handoff` only if the latest artifact is stale or missing those snapshots. Ask for a current repo zip when producing the next package or when the failure is code-level.

## Durable read order

1. `README.md`
2. `docs/manifest.md`
3. `docs/status/current.md`
4. `docs/strategy.md`
5. `docs/roadmap.md`
6. `docs/llm/post-update-review.md`
7. `docs/learning-log.md`
8. `docs/decisions.md`
9. `docs/checklists/loop-runtime.md`
10. `docs/checklists/planning-harness.md`
11. `docs/protocols/planning-loop.md`
12. `docs/llm/commands.md`
13. `docs/protocols/llm-handoff-protocol.md`
14. `docs/protocols/command-grammar.md`
15. `docs/workflows/update-pipeline.md`
16. `docs/workflows/verify.md`
17. `docs/workflows/package-authoring.md`
18. `docs/workflows/state-cleanup.md`
19. `docs/workflows/parallel-readiness.md`

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

Stage 6 uses bounded parallel self-host hardening. Read `docs/manifest.md`, `docs/strategy.md`, `docs/roadmap.md`, `docs/status/current.md`, `docs/learning-log.md`, and `docs/decisions.md` before proposing the next package.

The next package should be a bounded bundle with a clear success gate, not a large all-at-once rewrite.
