# recovery and debug

Normal work goes through:

```bash
tul run
```

Stepwise work goes through:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Recovery and debug commands live under `recover`.

## Summary

```bash
tul recover
```

Shows latest rollbackable commit, resume information, and safe next commands.

## Rollback plan

```bash
tul recover rollback
```

This command does not silently mutate the repo. It prints the safe rollback command.

## Resume plan

```bash
tul recover resume
```

Shows the latest state and recommended next commands.

## Apply/publish debug

```bash
tul recover apply
tul recover publish
```

These are conservative debug surfaces. They do not replace the normal `run` or `update` path.
