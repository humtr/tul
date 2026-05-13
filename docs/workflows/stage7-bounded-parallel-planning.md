# Stage 7 bounded parallel planning

Stage 7 allows multiple candidate plans to be drafted or compared, but only one package is applied against the latest verified baseline at a time.

## Normal application

```bash
tul run
```

## Runtime checks

Use:

```bash
tul show
tul show exports
tul verify fresh
```

## Bundle classes

| Class | Meaning |
|---|---|
| Green | isolated docs/template cleanup |
| Yellow | coordination docs or command docs touched |
| Orange | bounded runtime behavior change |
| Red | update/run/recovery behavior or release-gate semantics |

## Serialization rules

Serialize packages that touch:

```text
docs/status/current.md
docs/roadmap.md
docs/manifest.md
docs/decisions.md
docs/learning-log.md
```

Serialize implementation work against the package that defines its acceptance gate.

## Current Stage 7 direction

The command surface is closed around `tul run`. The current follow-up is run-default finalization and active docs/templates cleanup.
