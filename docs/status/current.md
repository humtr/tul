# Current status

Latest known version after this package: `0.7.5-verify-artifacts`.

Latest completed stage: Stage 5.5 — package authoring polish.

Current mode: Stage 6 baseline — planning harness inserted; verify artifact logging is the next bridge-reduction step before native-context implementation.

## Current verified loop

The current normal self-host loop is:

```bash
tul package latest tul
tul update tul -l
tul verify tul --fresh-clone
tul handoff tul
```

`PKG=...` should be exceptional. Normal use should prefer inbox discovery and `-l`.

## Current next package

`tul_verify_artifacts_v1`

Purpose:

- Insert manifest/strategy/roadmap/status/learning/decisions planning harness.
- Preserve README as compact entrypoint.
- Record Stage 6 as accelerated self-host hardening.
- Keep `/ai` as Stage X.

## Next after that

`tul_native_context_v1a`

Expected scope:

- `tul use <project>`.
- `tul current`.
- active project context storage.
- default project support.

Native no-arg update and package mismatch guidance should be implemented in later sub-steps after context storage is stable.

## Current risk notes

- The uploaded source baseline does not contain `docs/manifest.md`, `docs/strategy.md`, `docs/learning-log.md`, or `docs/decisions.md`; this package introduces them.
- Native context is not implemented yet and must not be documented as complete.
- Stage X target onboarding remains deferred.

## Verify artifacts

`tul verify` writes markdown and JSON artifacts under the platform log root. On Termux, upload this file instead of pasting long terminal output:

```text
/sdcard/termux/import/tul/logs/verify/tul-verify-latest.md
```
