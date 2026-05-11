# LLM Handoff Protocol

When receiving a `tul handoff`, the LLM must:

1. Verify remote repo/branch/HEAD when possible.
2. If remote access is unavailable, say so.
3. Read latest relevant files.
4. Separate user-stated goals, terminal-verified facts, assistant interpretation, and uncertainty.
5. Preserve invariants:
   - `tul update` pushes by default.
   - `--no-push` is the exception.
   - no `git add -A`.
   - no force push.
   - policy belongs in `.tul.yml`.
   - platform paths belong in global config.
6. Propose the next package and roadmap.
