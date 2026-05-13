# current status

Status: Stage 7 `tul run` is the normal user loop. The latest verified baseline after the README package-contract gate fix is stable, and the next package adds command-surface/run smoke checks to the release gate.

Current verified baseline:

```text
HEAD: 5984adba54866b5ae55844feade83bd3d4477355
Remote HEAD: 5984adba54866b5ae55844feade83bd3d4477355
Latest package: tul-stage7-readme-package-contract-gate-fix-bundle-v1
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
- run default finalization
- README package-contract gate fix

## Current package

Apply `tul-stage7-run-smoke-gate-bundle-v1` to make the release gate check the Stage 7 command surface more directly.

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

The default user-facing loop is one command:

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

## Next queue

1. Apply `tul-stage7-run-smoke-gate-bundle-v1`.
2. Confirm release gate PASS with `tul run` or `tul verify fresh`.
3. Continue command residue cleanup and historical-doc marking.
4. Add broader warning-first scans for old command examples in active docs/templates.
