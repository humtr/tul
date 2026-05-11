# LLM handoff protocol

A tul handoff is a structured remote-review request.

## Default behavior

`tul handoff <project>` is compact by default. It should contain runtime facts and pointers to repo-resident documents, not the full protocol text.

Use full mode only when needed:

```bash
tul handoff <project> --full
```

Use instructions mode when creating or refreshing a ChatGPT/Codex-style project prompt:

```bash
tul handoff <project> --instructions
tul instructions [project]
```

## Runtime fact boundary

Runtime facts belong in terminal output:

- commit hash
- push verified
- remote HEAD after fetch
- rollback command
- state path
- report path
- working tree status

Durable guidance belongs in repo files:

- `README.md`
- `docs/llm/entrypoint.md`
- `docs/status/current.md`
- `docs/roadmap.md`
- `docs/checklists/loop-runtime.md`
- `templates/project-instructions.md`

## Required LLM behavior

When receiving a tul handoff, the LLM must:

1. Treat the handoff as a structured remote-review request.
2. Verify remote repo, branch, and expected HEAD when possible.
3. If remote verification is unavailable, say so explicitly.
4. Read current relevant repo files before proposing implementation.
5. Preserve tul invariants:
   - `tul update` pushes by default.
   - `--no-push` and `--no-commit` are exceptions.
   - no broad staging.
   - no force push.
   - project policy belongs in `.tul.yml`.
   - environment paths and aliases belong in global config.
6. Separate user-stated goals, terminal-verified facts, assistant interpretation, and unresolved uncertainty.
7. If generating files, produce a cross-platform `tul-package.yml + files/ + README.md` package.

## Package execution guidance

If the package will be downloaded into configured inbox roots, prefer:

```bash
tul update <project> --latest
```

If an exact path is required, use:

```bash
tul update <project> --package /path/to/package.zip
```
