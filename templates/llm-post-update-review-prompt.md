# tul post-update review prompt

Review the latest tul handoff and remote repo state.

1. Verify remote HEAD when possible.
2. Read compact handoff runtime facts.
3. Read `docs/status/current.md`, `docs/roadmap.md`, and `docs/checklists/loop-runtime.md`.
4. Check for invariant regressions.
5. Propose the next package boundary.
6. If generating a package, use `tul-package.yml + files/ + README.md` and advise `tul update <project> --latest` when saved in inbox roots.
