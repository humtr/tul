# parallel readiness

Stage 7 allows parallel planning but keeps application sequential and gated.

## Runtime facts

Use these surfaces:

```bash
tul show
tul show exports
tul verify fresh
```

`show exports` reports source/review freshness and docs drift as warning-only diagnostics.

## Conflict rule

Serialize packages that touch coordination files:

```text
docs/status/current.md
docs/roadmap.md
docs/manifest.md
docs/decisions.md
docs/learning-log.md
```

Serialize any implementation package against the package that defines its acceptance gate.

## Normal application

```bash
tul run
```

Use stepwise commands only for diagnostics or when the user explicitly requests decomposition.
