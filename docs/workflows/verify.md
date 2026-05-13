# verify workflow

`verify` checks the repo. It is top-level because verification is a core runtime action.

## Modes

```bash
tul verify
tul verify fresh
```

`verify` without arguments is quick/local and stdout-first. It should not rewrite latest upload artifacts.

`verify fresh` performs fresh clone verification and writes the latest uploadable verification artifacts:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-vf-latest.json
```

## Runtime snapshots

The latest verify markdown should include canonical snapshots:

```text
tul show
tul show handoff
tul show exports
```

## Relationship to run

Normal users should not need to call `verify fresh` after `tul run`; `run` performs export and fresh verification as part of the loop.

Use explicit `verify fresh` when refreshing artifacts without applying a package, or when diagnosing release-gate behavior.
