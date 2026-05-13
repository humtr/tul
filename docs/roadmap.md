# roadmap

## Current baseline

The latest verified baseline is `5984adba54866b5ae55844feade83bd3d4477355`.

The latest applied package is `tul-stage7-readme-package-contract-gate-fix-bundle-v1`.

## Closed Stage 7 sequence

1. `tul-stage7-planning-consolidation-bundle-v1`
2. `tul-stage7-terminology-audit-bundle-v1`
3. `tul-stage7-source-spec-and-gates-bundle-v1`
4. `tul-stage7-source-export-implementation-bundle-v1`
5. `tul-stage7-export-integrity-hardening-bundle-v1`
6. `tul-stage7-post-update-export-automation-bundle-v1`
7. `tul-stage7-command-surface-redesign-bundle-v1`
8. `tul-stage7-command-surface-status-sync-bundle-v1`
9. `tul-stage7-run-default-finalization-bundle-v1`
10. `tul-stage7-readme-package-contract-gate-fix-bundle-v1`

## Immediate queue

1. `tul-stage7-run-smoke-gate-bundle-v1`
   - add release-gate smoke checks for canonical command help;
   - reject removed top-level command regression;
   - confirm `export` remains file-producing only;
   - confirm `run` package-not-found fallback markers are present.

2. `tul-stage7-command-residue-cleanup-bundle-v1`
   - finish active workflow docs cleanup;
   - mark historical docs whose command examples intentionally predate Stage 7.

3. `tul-stage7-release-gate-command-surface-bundle-v1`
   - add broader warning-first scans for active docs/templates;
   - promote checks to gate conditions only after false positives are understood.

4. `tul-stage7-closure-checkpoint-bundle-v1`
   - close Stage 7 after `tul run` smoke coverage and command residue cleanup are stable.

## Deferred

- release-gate failure on export freshness warnings;
- destructive cleanup automation;
- external repository onboarding;
- legacy alias compatibility layer.
