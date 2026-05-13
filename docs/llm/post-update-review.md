# post-run review

Use this workflow after a user applies a tul package.

## Required artifact

Primary evidence:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

It should show release gate status, HEAD/Remote HEAD, fresh clone status, and runtime snapshots.

Optional source/review context:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
/sdcard/termux/import/tul/tul-review-latest.zip
```

## Review order

1. Read `tul-vf-latest.md`.
2. Confirm HEAD, Remote HEAD, release gate, step count, working tree, and fresh clone.
3. Confirm latest package and commit from runtime state.
4. If source/review artifacts are stale or missing, say so explicitly.
5. Propose the next package only after the new baseline is clear.

## Command grammar

Normal user workflow is:

```bash
tul package
tul run
```

Stepwise workflow is:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Use `tul show exports` for artifact freshness. `export` is reserved for file creation.
