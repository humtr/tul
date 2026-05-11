# LLM handoff protocol

`tul handoff` is a structured remote-review request.

## Compact by default

Default handoff output should be compact. It should include runtime facts and repo document pointers, not repeat the entire protocol every time.

Runtime facts include:

- mode
- project
- repo URL and path
- branch
- local HEAD
- remote HEAD after fetch, if available
- working tree status
- active package
- outcome
- commit hash, if any
- push verification result, if known
- rollback command, if available
- state/report paths

## Full mode

Use full mode when the receiving LLM needs the protocol inline:

```bash
tul handoff <project> --full
```

## LLM requirements

When receiving a tul handoff, the LLM must:

1. Treat it as a structured remote-review request.
2. Verify remote repo, branch, and expected HEAD when possible.
3. If remote verification is unavailable, say so explicitly.
4. Read current relevant repo files before proposing implementation.
5. Compare terminal-verified facts against remote state.
6. Preserve invariants:
   - `tul update` pushes by default.
   - `--no-push` is an exception.
   - no `git add -A` or `git add .` in the normal path.
   - no force push.
   - project policy belongs in `.tul.yml`.
   - environment paths belong in global config.
7. Separate user-stated goals, terminal-verified facts, source-backed facts, assistant interpretation, and uncertainty.
8. Identify structural debt and the next package boundary.
9. If generating files, produce a cross-platform `tul-package.yml + files/ + README.md` package.

## Runtime facts vs durable docs

Post-update runtime facts cannot be committed into the same implementation commit that produces them. Therefore:

- Repo documents store durable planning surfaces.
- Terminal handoff stores per-run facts such as commit hash, push verified, rollback command, report path, and state path.
- A handoff-only commit after every update is not the default because it creates log noise and self-reference problems.
