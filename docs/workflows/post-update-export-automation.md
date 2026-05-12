# Post-update export automation

Status: Stage 7 Red-light implementation package.

## Purpose

Reduce human bridge work after a successful `tul update` by refreshing the two transport artifacts that fresh LLM sessions need most often:

- `tul-source-latest.zip` for full source context and package generation;
- `tul-review-latest.zip` for compact changed-file review transport.

This automation is intentionally separate from the release gate. It runs only after the core update has already committed, pushed, and passed fresh verification.

## Default order

```text
precheck
-> import
-> validate
-> apply
-> checks
-> sweep
-> publish
-> verify fresh
-> report/state/handoff
-> latest verify snapshot rewrite
-> post-update source export
-> post-update review export when changed files exist
-> latest verify snapshot refresh
```

## Failure policy

Post-update export failures are warning-only. They must not:

- roll back a successful commit;
- change push verification facts;
- turn a release-gate PASS into FAIL;
- change rollback authority;
- hide the fact that an artifact was stale, missing, skipped, or failed.

Failures are recorded in state/report/handoff and surfaced by `tul export status`.

## Escape hatches

Recovery/debug runs can disable all or part of the post-update export phase:

```bash
tul update --no-export
tul update --no-source-export
tul update --no-review-export
```

These options should not become the normal path. They exist for constrained storage, export-path failures, or focused update debugging.

## Acceptance gate

A successful automation package must show:

- release gate PASS and fresh clone PASS after the update;
- source export PASS after the update unless disabled;
- review export PASS after the update when changed files exist unless disabled;
- `tul export status` reports current artifacts after a normal update;
- latest state records `source_bundle_export`, `review_bundle_export`, and `post_update_exports`;
- report and handoff include post-update export outcome sections;
- export failures, if forced in a recovery test, are warning-only.
