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

Recovery and debug commands live under `recover`. The default behavior is status/plan output only.

## Summary

```bash
tul recover
```

Shows latest rollbackable commit, resume information, and safe next commands. It does not modify the repo.

## Rollback plan

```bash
tul recover rollback
```

This prints a safe `git revert` command for the latest rollbackable commit or a supplied commit. It does not silently mutate the repo.

## Resume plan

```bash
tul recover resume
```

Shows the latest state and recommended next commands.

## Advanced debug

```bash
tul recover apply
tul recover publish
```

These are conservative debug surfaces. They do not replace the normal `run` or `update` path. `recover apply` recommends the normal update path; `recover publish` only inspects staged files and does not commit or push.
