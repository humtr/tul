# artifact semantics

Artifacts have different authority levels.

## Authorities

| Artifact | Role |
|---|---|
| Git remote + commit hash | canonical source/recovery authority |
| `tul-vf-latest.md` | uploadable runtime verification evidence |
| `tul-source-latest.zip` | full source context transport artifact |
| `tul-review-latest.zip` | diff-oriented review transport artifact |
| state/report/handoff files | local runtime records |

Zip artifacts are not backup authority. Recovery authority is Git remote plus commit hashes and recovery state.

## Commands

```bash
tul show
tul show exports
tul export
tul verify fresh
```

`export` creates files. `show exports` inspects freshness/status.

## Normal loop

```bash
tul run
```

A successful normal loop should leave verification and transport artifacts current.

## Source context

Use `tul-source-latest.zip` as the normal source baseline for LLM package generation. Use GitHub/fresh clone comparison for large CLI/runtime redesigns, source export changes, or suspected file omission.
