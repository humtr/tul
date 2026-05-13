# roadmap

## Current baseline

The latest verified baseline is `8534311ce661c5ffee34b638705a61a6e4d84874`.

The latest applied package is `tul-stage7-command-residue-cleanup-bundle-v1`.

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
11. `tul-stage7-run-smoke-gate-bundle-v1`
12. `tul-stage7-command-residue-cleanup-bundle-v1`

## Immediate queue

1. `tul-stage7-clean-recover-setup-ux-bundle-v1`
   - keep `tul clean` plan-only by default;
   - make `tul clean states run 3` parse `3` as keep count;
   - keep `tul recover` plan-only by default;
   - keep `tul setup` status-only by default;
   - document the auxiliary command contract.

2. `tul-stage7-closure-checkpoint-bundle-v1`
   - close Stage 7 after run, export, command surface, docs, and auxiliary UX are all verified.

## Deferred

- destructive cleanup automation;
- rollback auto-execution;
- external repository onboarding;
- legacy alias compatibility layer.
