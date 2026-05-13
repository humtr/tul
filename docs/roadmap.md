# roadmap

## Current baseline

The latest verified baseline is `e36383dcd8a4e427971a675da93eaa744be4db9d`.

The latest applied package is `tul-stage7-command-surface-status-sync-bundle-v1`.

## Closed Stage 7 sequence

1. `tul-stage7-planning-consolidation-bundle-v1`
2. `tul-stage7-terminology-audit-bundle-v1`
3. `tul-stage7-source-spec-and-gates-bundle-v1`
4. `tul-stage7-source-export-implementation-bundle-v1`
5. `tul-stage7-export-integrity-hardening-bundle-v1`
6. `tul-stage7-post-update-export-automation-bundle-v1`
7. `tul-stage7-command-surface-redesign-bundle-v1`
8. `tul-stage7-command-surface-status-sync-bundle-v1`

## Immediate queue

1. `tul-stage7-run-default-finalization-bundle-v1`
   - make `tul run` the single normal user loop;
   - keep `tul package` as optional preflight only;
   - add `package not found` fallback: `export -> verify fresh -> show`;
   - update active docs and templates away from pre-redesign commands.

2. `tul-stage7-command-residue-cleanup-bundle-v1`
   - finish active workflow docs cleanup;
   - mark historical docs whose command examples intentionally predate Stage 7.

3. `tul-stage7-release-gate-command-surface-bundle-v1`
   - add warning-first command surface smoke checks;
   - scan templates for forbidden old command examples;
   - promote checks to gate conditions only after false positives are understood.

## Deferred

- release-gate failure on export freshness warnings;
- destructive cleanup automation;
- external repository onboarding;
- legacy alias compatibility layer.
