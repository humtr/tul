# tul post-run review prompt

Review the latest tul runtime evidence and repo state.

1. Treat `tul-vf-latest.md` as the runtime verification evidence.
2. Confirm HEAD, Remote HEAD, release gate, fresh clone, and working tree facts.
3. Check the `tul show exports` snapshot for source/review freshness.
4. Read `docs/status/current.md`, `docs/roadmap.md`, and `docs/checklists/loop-runtime.md`.
5. Check for invariant regressions.
6. Propose the next package boundary.
7. If generating a package, use `tul-package.yml + files/ + README.md`.
8. Normal user application is `tul run`.
