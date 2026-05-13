# current status

Status: Stage 7 `tul run` finalization is applied, exports are current, and the remaining release-gate issue is a narrow README package-contract phrase fix.

Current verified baseline before this hotfix:

```text
HEAD: 3c99639f04ae5cf8d2a5356e26a00b3cc113ebd6
Remote HEAD: 3c99639f04ae5cf8d2a5356e26a00b3cc113ebd6
Latest package: tul-stage7-run-default-finalization-bundle-v1
Release gate: FAIL
Failure scope: README entrypoint terms only
Missing term: tul-package.yml + files/ + README.md
Fresh clone: otherwise PASS
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

## Current hotfix

Apply `tul-stage7-readme-package-contract-gate-fix-bundle-v1` to restore the exact README package-contract phrase required by the current release gate while preserving the simplified Stage 7 command surface.

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

1. Apply `tul-stage7-readme-package-contract-gate-fix-bundle-v1`.
2. Confirm release gate PASS with `tul verify fresh`.
3. Run `tul run` once with no pending package to confirm artifact-refresh fallback behavior.
4. Continue command residue cleanup and release-gate expansion only after this narrow gate fix is closed.
