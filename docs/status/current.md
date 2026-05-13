# current status

Status: Stage 7 `tul run` is the normal user loop. The latest verified baseline after the run smoke gate package is stable. The next package cleans command-surface residue from active docs/templates and marks historical documents.

Current verified baseline:

```text
HEAD: 70292083094d71387371c8705ae5828bb1442e31
Remote HEAD: 70292083094d71387371c8705ae5828bb1442e31
Latest package: tul-stage7-run-smoke-gate-bundle-v1
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
- run smoke gate

## Current package

Apply `tul-stage7-command-residue-cleanup-bundle-v1` to remove old command examples from active docs/templates and mark historical docs that intentionally retain pre-Stage 7 command grammar.

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

## Next queue

1. Apply `tul-stage7-command-residue-cleanup-bundle-v1`.
2. Confirm release gate PASS with `tul run` or `tul verify fresh`.
3. Add warning-first scans for removed command examples in active docs/templates.
4. Close Stage 7 after command residue cleanup and gate expansion are stable.
