# LLM handoff protocol

When receiving a tul handoff, the LLM must:

1. Treat the handoff as a structured remote-review request.
2. Verify the remote repo, branch, and expected HEAD when remote access is available.
3. If remote access is unavailable, explicitly say verification cannot be performed.
4. Read current relevant repo files before proposing implementation.
5. Preserve tul invariants:
   - `tul update` pushes by default.
   - `--no-push` is an exception.
   - no `git add -A` or `git add .` in the default path.
   - no force push in the normal path.
   - project-specific policy belongs in `.tul.yml`.
   - environment paths belong in global config.
   - Windows/Termux package flow converges on a manifest package.
6. Separate user-stated goals, terminal-verified facts, assistant interpretation, and unresolved uncertainty.
7. Identify structural debt, missing automation, and next package boundary.
8. Provide short-term and long-term roadmap.
9. Do not regress update push-by-default semantics.
