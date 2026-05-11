# Handoff behavior

`tul handoff <project>` prints a compact handoff by default.

Compact handoff includes:

- repo URL
- branch
- local HEAD
- remote HEAD after fetch
- working tree status
- active package if available
- commit hash if available
- push verification if available
- rollback command if available
- state/report paths if available
- pointers to durable repo documents

Full handoff is available with:

```bash
tul handoff <project> --full
```

Project instructions are available with:

```bash
tul handoff <project> --instructions
tul instructions [project]
```

The README should stay concise. Runtime facts should stay in handoff output. Durable status and planning should stay in `docs/status/current.md`, `docs/roadmap.md`, and `docs/checklists/loop-runtime.md`.
