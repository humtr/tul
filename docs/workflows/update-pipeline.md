# update and run pipeline

Stage 7 separates `update` from `run`.

## Command boundary

`tul update` updates the repository:

```text
package selection -> import -> manifest validation -> safe apply -> checks -> sweep -> stage listed files -> commit -> push -> remote HEAD check -> report/state/handoff
```

`tul run` performs the full Terminal Update Loop:

```text
package -> update -> export -> verify fresh -> show
```

This split prevents `update` from accumulating every post-update responsibility.

## Normal workflow

```bash
cd ~/prj/tul

tul package
tul run
```

## Stepwise workflow

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## Exact package path

```bash
tul update /path/to/package.zip
```

## Dry planning

```bash
tul update dry
tul run dry
```

`update dry` plans the update step only. `run dry` shows the whole-loop plan.

## Verification artifacts

`tul verify` is quick/local and does not rewrite latest artifacts by default.

`tul verify fresh` writes the uploadable verification artifacts:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-vf-latest.json
```

## Export artifacts

`tul export` creates both explicit transport artifacts:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
/sdcard/termux/import/tul/tul-review-latest.zip
```

`tul show exports` inspects freshness and drift. It does not create files.
