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

## Current next stage

The current stage is the LLM loop contract. Make the loop easy for a fresh LLM or coding agent to discover without relying on long chat history.
