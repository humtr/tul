# tul handoff

`tul handoff <project>` prints a compact structured prompt for the next LLM or coding session.

## Default compact handoff

Default output contains:

- mode
- project
- repo path and URL
- branch
- local HEAD
- remote HEAD after fetch, if available
- working tree status
- active package
- outcome
- commit/push/rollback/state/report facts when available
- repo document pointers

It intentionally does not repeat the full protocol every time.

## Full handoff

```bash
tul handoff <project> --full
```

Full mode includes invariants, LLM-side command grammar, request checklist, and source separation guidance.

## Instructions output

```bash
tul handoff <project> --instructions
tul instructions [project]
```

These commands print `templates/project-instructions.md`.

## Runtime facts vs repo documents

Commit hash, push verification, rollback command, and state/report paths are runtime facts. They are printed by the terminal handoff. Durable guidance belongs in repo documents under `docs/` and `templates/`.
