# roadmap

## Current baseline

The latest verified baseline is `70292083094d71387371c8705ae5828bb1442e31`.

The latest applied package is `tul-stage7-run-smoke-gate-bundle-v1`.

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

## Immediate queue

1. `tul-stage7-command-residue-cleanup-bundle-v1`
   - clean active docs/templates so they use the canonical Stage 7 command surface;
   - replace old command examples with `tul run`, `tul show`, `tul show exports`, `tul verify fresh`, `tul export`, `tul clean`, and `tul recover`;
   - add historical banners to pre-Stage 7 documents that intentionally retain old command examples.

2. `tul-stage7-release-gate-command-surface-bundle-v1`
   - add broader warning-first scans for active docs/templates;
   - exclude files marked historical;
   - promote checks to gate conditions only after false positives are understood.

3. `tul-stage7-closure-checkpoint-bundle-v1`
   - close Stage 7 after `tul run` smoke coverage, command residue cleanup, and command-surface scan coverage are stable.

## Deferred

- release-gate failure on export freshness warnings;
- destructive cleanup automation;
- external repository onboarding;
- legacy alias compatibility layer.
