# tul LLM handoff prompt template

You are receiving a `tul` handoff.

Treat it as a remote-review request, not as proof that you have already verified the remote repo.

Do these steps:

1. Verify repo, branch, HEAD, and changed files when remote access is available.
2. If remote access is unavailable, state that explicitly.
3. Read current relevant files before proposing implementation.
4. Check invariants:
   - `tul update` pushes by default.
   - `--no-push` and `--no-commit` are exceptions.
   - default staging is explicit only.
   - no force push.
   - config/policy are separated from engine code.
5. Separate:
   - user-stated goals
   - terminal-verified facts
   - assistant interpretation
   - unresolved uncertainty
6. Propose the next package boundary and roadmap.
