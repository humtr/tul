# tul commands

Canonical user-facing terminal commands:

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

There is no canonical legacy alias layer. Use these namespaces directly.

## Normal loop

```bash
cd ~/prj/tul

tul package
tul run
```

`run` performs package selection, update, export, fresh verification, and final status output.

## Stepwise loop

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## Status and review

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

## Artifacts

```bash
tul export         # source + review
tul export source
tul export review
```

## Cleanup and recovery

```bash
tul clean
tul clean states
tul clean states run 3
tul clean packages
tul recover
tul recover rollback
```

## Setup

```bash
tul setup
tul setup init <target>
tul setup install
tul setup use <project>
```
