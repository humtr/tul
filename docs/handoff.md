> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# Handoff behavior

`tul handoff <project>` prints a compact handoff by default.

Compact handoff is a bridge artifact, not the full project contract. It should contain current runtime facts plus pointers to repo-resident documents that a fresh LLM can read.

## Compact handoff contents

Compact handoff includes:

- repo URL;
- branch;
- local HEAD;
- remote HEAD after fetch;
- working tree status;
- active package if available;
- outcome if available;
- commit hash if available;
- push verification if available;
- rollback command if available;
- state/report paths if available;
- verify artifact paths if available;
- pointers to durable repo documents.

## Read-next priority

A fresh LLM should start with:

1. the user-provided `tul-vf-latest.md` artifact, when present;
2. pasted `tul state` output, when the task involves state, rollback, cleanup, or archive behavior;
3. `docs/llm/entrypoint.md`;
4. `docs/llm/post-update-review.md`;
5. `docs/status/current.md`;
6. `docs/roadmap.md`;
7. `docs/workflows/stage7-bounded-parallel-planning.md`;
8. `docs/checklists/loop-runtime.md`.

## Full and instruction modes

Full handoff is available with:

```bash
tul handoff <project> --full
```

Project instructions are available with:

```bash
tul handoff <project> --instructions
tul instructions [project]
```

The README should stay concise. Runtime facts should stay in handoff output and verify artifacts. Durable status and planning should stay in `docs/status/current.md`, `docs/roadmap.md`, and `docs/checklists/loop-runtime.md`.


## Stage 7 handoff rule

A fresh LLM should treat `tul-vf-latest.md` as runtime truth, then use repo docs for durable planning. For Stage 7, the handoff should point to the bounded parallel planning guide before any package proposal. Parallel planning is allowed; parallel application is not.
