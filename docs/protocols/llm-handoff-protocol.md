# LLM handoff protocol

When receiving a `tul handoff`, the LLM must treat it as a structured remote-review request.

Required behavior:

1. Verify the remote repo, branch, and expected HEAD when remote access is available.
2. If remote verification is unavailable, say so explicitly.
3. Read current relevant repo files before proposing implementation.
4. Compare terminal-verified facts against remote state.
5. Preserve invariants:
   - `tul update` pushes by default.
   - `--no-push` is an exception.
   - no `git add -A` or `git add .` in the normal path.
   - no force push.
   - project policy belongs in `.tul.yml`.
   - environment paths belong in global config.
6. Separate user-stated goals, terminal-verified facts, assistant interpretation, and uncertainty.
7. Identify structural debt and the next package boundary.
8. If generating files, produce a cross-platform `tul-package.yml` package.
