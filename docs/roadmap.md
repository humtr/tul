# roadmap

## Current baseline

The latest verified command-surface baseline is `c274a27e33dd2e13b91daf42e165042cf69b1d9f`.

The latest package recorded by the current status ledger is `tul-stage7-command-surface-status-sync-bundle-v1`.

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

1. Command-surface smoke test
   - verify `tul package`
   - verify `tul run dry`
   - verify `tul show`
   - verify `tul show exports`
   - verify `tul verify`
   - verify `tul verify fresh`
   - verify `tul export` only when fresh artifacts are intentionally regenerated

2. Command-surface follow-up only if smoke tests expose issues
   - fix parser/help mismatches
   - fix stale docs or handoff wording
   - keep the canonical top-level set stable unless a concrete conflict appears

3. Stage 7 continuation candidates
   - improve clean/recover/setup subcommand ergonomics if normal use shows friction
   - refine docs drift checker after observing false positives/negatives
   - keep export freshness warning-only unless an explicit release-gate decision is accepted

## Deferred

- release-gate failure on export freshness warnings
- broader cleanup behavior changes
- destructive cleanup automation
- external repository onboarding
- legacy alias compatibility layer
