# post-update export automation

Status: superseded by the `run` command boundary.

The earlier post-update export automation placed source/review export inside `update`. Stage 7 command-surface redesign moves the full-loop responsibility to `tul run`.

Final boundary:

```text
tul update = package apply + checks + commit + push + remote HEAD check
tul run    = package -> update -> export -> verify fresh -> show
```

Export failures remain warning-only. Artifact freshness is inspected with:

```bash
tul show exports
```

Artifact creation remains:

```bash
tul export
tul export source
tul export review
```
