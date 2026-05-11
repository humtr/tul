# Project instructions: tul Terminal Update Loop

You are working on `humtr/tul`, the Terminal Update Loop runtime.

## Goal

Maintain a config-driven, manifest-driven, cross-platform loop where:

```text
LLM creates package
→ user downloads package
→ tul update <project>
→ tul applies/checks/sweeps/commits/pushes/verifies
→ tul prints rollback instructions and compact handoff
→ next LLM verifies remote state and proposes the next package
```

## Required invariants

- `tul update <project>` is the default full-loop command.
- Push is included by default after successful commit.
- `--no-push` and `--no-commit` are exceptions.
- Remote HEAD verification is required after push.
- Do not use `git add -A` or `git add .` in the normal path.
- Do not force push.
- Keep project policy in `.tul.yml`.
- Keep environment paths and aliases in global config.
- Generate cross-platform packages unless there is an explicit reason not to.

## Before proposing work

1. Verify remote repo/branch/HEAD when possible.
2. Read `docs/llm/entrypoint.md`.
3. Read `docs/status/current.md`.
4. Read `docs/roadmap.md`.
5. Read `docs/checklists/loop-runtime.md`.
6. Inspect relevant code before proposing implementation.

## Source separation

Separate:

- user-stated goals
- terminal-verified facts
- repo/source-backed facts
- assistant interpretation
- unresolved uncertainty

Do not attribute assistant-created framing to the user unless the user explicitly accepts it.

## Package output

When creating files, produce a single cross-platform package:

```text
<package>.zip
  tul-package.yml
  files/
  README.md
  apply.sh
  apply.ps1
```

The manifest should list explicit `commit.files`. Do not rely on broad staging.
