# current status

Status: Stage 7 command-surface redesign prepared.

Current verified baseline before this package:

```text
HEAD: 57c80c403a651ea30319916ddc81b19a14384e6a
Latest package: tul-stage7-post-update-export-automation-bundle-v1
Release gate: PASS
Fresh clone: PASS
```

## Closed Stage 7 checkpoints

- planning consolidation
- terminology audit
- source spec and gates
- explicit source export implementation
- export integrity hardening
- post-update export automation

## Active change

The command surface is being simplified to the canonical top-level commands:

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

The design has no canonical legacy alias layer.

## Next verification

After applying the command-surface redesign package, use the old command only for that package application. After it lands, the normal workflow becomes:

```bash
tul package
tul run
```
