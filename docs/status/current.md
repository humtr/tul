# current status

Status: Stage 7 command-surface redesign closed and verified.

Current verified baseline:

```text
HEAD: c274a27e33dd2e13b91daf42e165042cf69b1d9f
Remote HEAD: c274a27e33dd2e13b91daf42e165042cf69b1d9f
Latest package: tul-stage7-command-surface-status-sync-bundle-v1
Previous package: tul-stage7-command-surface-redesign-bundle-v1
Release gate: PASS
Fresh clone: PASS
Source bundle: current
Review bundle: current
```

The command-surface redesign package landed at `c274a27e33dd2e13b91daf42e165042cf69b1d9f`. A first verify snapshot failed because the already-running verifier still checked pre-redesign README entrypoint terms. A subsequent `tul verify fresh` using the new verifier passed with 25 pass, 0 fail. This is recorded as a bootstrap gate-drift lesson, not a runtime failure.

## Closed Stage 7 checkpoints

- planning consolidation
- terminology audit
- source spec and gates
- explicit source export implementation
- export integrity hardening
- post-update export automation
- command-surface redesign around `tul run`
- command-surface status sync

## Current canonical command surface

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

Normal loop:

```bash
tul package
tul run
```

Stepwise loop:

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## Current warning-only status

`tul show exports` is the advisory export and docs-drift inspection surface. The latest post-redesign verify showed source/review artifacts current and a single docs drift warning because this file did not yet mention `tul-stage7-command-surface-redesign-bundle-v1`. This package closes that ledger drift by recording the redesign closure and this status-sync package name.

## Next queue

1. Smoke-test the new canonical command surface in normal use:
   - `tul package`
   - `tul run dry`
   - `tul show exports`
   - `tul verify`
   - `tul verify fresh`

2. If command smoke tests are clean, consider the command-surface redesign stable enough for Stage 7 continuation.

3. Keep broader cleanup behavior changes, release-gate enforcement on export freshness, and external repository onboarding deferred.
