# LLM entrypoint for tul

You are reading the `humtr/tul` repository, the Terminal Update Loop runtime.

## Purpose

`tul` exists to make this loop fast and verifiable:

```text
LLM creates a cross-platform package
→ user downloads it
→ tul update <project>
→ tul applies/checks/sweeps/commits/pushes/verifies
→ tul prints rollback instructions and compact handoff
→ the next LLM verifies remote state and proposes the next package
```

## Read order

1. `README.md`
2. `docs/status/current.md`
3. `docs/roadmap.md`
4. `docs/checklists/loop-runtime.md`
5. `docs/llm/commands.md`
6. `docs/protocols/llm-handoff-protocol.md`
7. `docs/protocols/command-grammar.md`
8. `docs/workflows/update-pipeline.md`

## Non-negotiable invariants

- `tul update <project>` is the default full-loop command.
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
tul update <project> --latest
# or
tul update <project> -l
```

Use `--package PATH` only when the user wants to apply a specific file.

Do not ask the user to paste long absolute package paths when the package is already in a configured inbox root and `--latest` is sufficient.

## Current next stage

After Option 2 adoption, the next stage is Stage 2.5: apply safety audit. Focus on directory copy safety, apply plan logging, and manifest destination allowlists.
