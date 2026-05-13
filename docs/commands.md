# tul commands

Canonical top-level commands:

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

There is no legacy alias layer in the Stage 7 command surface.

## Normal use

```bash
cd ~/prj/tul

tul run
```

`run` is the normal Terminal Update Loop. It applies a package when one is available. If no package is available, it refreshes current verification and transport artifacts.

## Optional preflight

```bash
tul package
```

Shows the newest compatible package candidate. It does not apply anything.

## Stepwise use

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Use this only when the user wants to inspect or split the loop.

## Status

```bash
tul show
tul show exports
tul show handoff
tul show report
tul show history 5
```

## Verification

```bash
tul verify        # quick/local, stdout-first
tul verify fresh  # fresh clone + latest verify artifacts
```

## Export

```bash
tul export         # source + review
tul export source
tul export review
```

`export` commands create files. Export freshness/status is shown by `tul show exports`.

## Cleanup

```bash
tul clean
tul clean states
tul clean states run 3
tul clean packages
```

The default `clean` path is plan-only. Use `run` in the clean namespace for guarded moves.

## Recovery

```bash
tul recover
tul recover rollback
tul recover resume
```

Recovery commands print plans or safe commands. They do not silently rewrite history.

## Setup

```bash
tul setup
tul setup init <target>
tul setup install
tul setup use <project>
```
