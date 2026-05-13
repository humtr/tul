# package discovery

Package discovery is under `package`.

## Default

```bash
tul package
```

Shows the newest compatible package from configured inbox roots. It does not apply anything.

## List

```bash
tul package list
```

Shows matching, incompatible, and invalid candidates.

## Check and inspect

```bash
tul package inspect <package.zip>
tul package check <package.zip>
```

Use these before manual package review or when diagnosing candidate selection.

## Relationship to run

Normal users may skip preflight and run:

```bash
tul run
```

If no compatible package exists, `run` refreshes current artifacts instead of treating the absence as a failed update.
