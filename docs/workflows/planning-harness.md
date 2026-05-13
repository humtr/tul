# planning harness

The planning harness keeps long-running tul work reviewable.

## Core files

```text
docs/manifest.md
docs/strategy.md
docs/roadmap.md
docs/status/current.md
docs/learning-log.md
docs/decisions.md
```

## Normal loop

```bash
tul run
```

Use stepwise commands only for diagnostics:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## Planning rule

Parallel planning is allowed. Application remains sequential and gated. If two packages touch coordination files, serialize them.
