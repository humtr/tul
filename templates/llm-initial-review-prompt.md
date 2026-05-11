# tul initial review prompt

You are receiving an initial-review handoff for a tul-managed repo.

Tasks:

1. Verify the remote repo, branch, and HEAD if remote access is available.
2. If verification is unavailable, say so explicitly.
3. Read `README.md`, `docs/llm/entrypoint.md`, `docs/status/current.md`, `docs/roadmap.md`, and `docs/checklists/loop-runtime.md`.
4. Inspect relevant code before proposing implementation.
5. Identify structural debt and the next safe package boundary.
6. Preserve all tul invariants.
7. If generating files, produce a cross-platform tul package.

Output:

- remote/fresh clone verification result
- manifest/invariant check
- high-risk defects
- next package scope
- modified file list
- acceptance criteria
- short/medium/long roadmap
