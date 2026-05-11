# tul LLM handoff prompt template

You are receiving a tul handoff from a terminal session.

Your tasks:

1. Verify the remote repo, branch, and expected HEAD if remote access is available.
2. If remote verification is unavailable, say so explicitly.
3. Read current relevant repo files.
4. Compare terminal-verified facts against remote state.
5. Check invariants:
   - `tul update` pushes by default.
   - `--no-push` is an exception.
   - no `git add -A` in the default path.
   - no force push.
   - project-specific policy belongs in `.tul.yml`.
   - environment paths belong in global config.
6. Identify remaining debt.
7. Propose the next package.
8. Provide short-term and long-term roadmap.
