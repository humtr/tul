# roadmap

## Current baseline

The latest verified baseline before the Stage 7 closure checkpoint is `e965194ee8573b4a9938c87fab42b058ecf020b2`.

The latest applied package is `tul-stage7-clean-recover-setup-ux-bundle-v1`.

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
13. `tul-stage7-clean-recover-setup-ux-bundle-v1`
14. `tul-stage7-closure-checkpoint-bundle-v1`

## Stage 7 closure criteria

Stage 7 is closed when the closure checkpoint is applied and the following stay true:

- `tul run` is the normal user loop.
- source, review, and verify artifacts are current after a normal run.
- the command surface is `show`, `package`, `update`, `verify`, `export`, `run`, `clean`, `recover`, and `setup`.
- removed top-level commands are absent from parser/help.
- `export` contains file-producing commands only.
- active docs/templates use current command grammar.
- historical docs are marked when they retain old command examples.
- `clean`, `recover`, and `setup` are conservative by default.
- release gate reports command-surface smoke checks.

## Stage 8 candidate queue

1. `tul-stage8-gate-hardening-plan-bundle-v1`
   - decide which command-surface and doc-residue scans stay warning-only and which become hard release-gate checks;
   - add a small matrix for false-positive handling before promoting any scan.

2. `tul-stage8-test-harness-baseline-bundle-v1`
   - introduce a repo-local smoke test harness for `show`, `package`, `verify`, `export`, `run`, `clean`, `recover`, and `setup` without requiring a live package inbox;
   - keep it separate from release-gate promotion until stable.

3. `tul-stage8-cleanup-retired-modules-plan-bundle-v1`
   - review retired helpers and compatibility-only modules such as old repo zip helpers, package hygiene internals, sweep helpers, and publish/debug helpers;
   - classify keep, hide, fold, or delete candidates;
   - avoid deletion until a separate source-backed package proves no call sites remain.

4. `tul-stage8-cross-repo-onboarding-plan-bundle-v1`
   - plan multi-repo adoption only after the self-hosting loop remains stable;
   - require explicit project policy, path, and package-target mismatch gates.

## Deferred

- destructive cleanup automation;
- rollback auto-execution;
- external repository onboarding implementation;
- legacy alias compatibility layer.
