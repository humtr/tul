# current status

Status: Stage 7 command surface is closed, verified, and ready for `tul run` finalization.

Current verified baseline:

```text
HEAD: e36383dcd8a4e427971a675da93eaa744be4db9d
Remote HEAD: e36383dcd8a4e427971a675da93eaa744be4db9d
Latest package: tul-stage7-command-surface-status-sync-bundle-v1
Release gate: PASS
Fresh clone: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Closed Stage 7 checkpoints

- planning consolidation
- terminology audit
- source spec and gates
- explicit source export implementation
- export integrity hardening
- post-update export automation
- command-surface redesign around `tul run`
- command-surface status sync

## Canonical command surface

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

## Normal loop

The default user-facing loop is now one command:

```bash
tul run
```

Semantics:

```text
package found:
  update -> export -> verify fresh -> show

package not found:
  export -> verify fresh -> show
```

`package not found` is not an error for `tul run`; it means there is no update to apply, so the command refreshes uploadable verification and transport artifacts for the current HEAD.

## Stepwise loop

Use this only when the user explicitly wants to split the loop:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## Next queue

1. Apply `tul-stage7-run-default-finalization-bundle-v1`.
2. Confirm that `tul run` works both when a package is present and when no package is present.
3. Continue cleanup of active docs and templates so new sessions see `tul run` as the normal path.
4. Defer release-gate expansion until the command surface has passed one normal-use cycle.
