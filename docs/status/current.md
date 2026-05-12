# Current status

Latest known version after this package: `0.7.6-verify-artifact-names`.

Current mode: Stage 6 baseline — planning harness is inserted and verify output is artifact-backed.

## Current verified loop

The current normal self-host loop is:

```bash
tul package latest tul
tul update tul -l
tul verify tul --fresh-clone
tul handoff tul
```

`PKG=...` should be exceptional. Normal use should prefer inbox discovery and `-l` until native no-arg context is implemented.

## Verify artifact upload convention

`tul verify` writes markdown and JSON artifacts under the platform log root. On Termux, upload the short timestamped markdown file when comparing runs:

```text
/sdcard/termux/import/tul/logs/verify/tul-vf-f-<yymmdd>-<hhmmss>-<head>.md
```

If only the latest run matters, upload:

```text
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.md
```

Compatibility aliases such as `tul-verify-latest.md` are still written, but the shorter `tul-vf-*` names are preferred.

## Current next package

`tul_native_context_v1a`

Expected scope:

- `tul use <project>`.
- `tul current`.
- active project context storage.
- default project support.

Native no-arg update and package mismatch guidance should be implemented in later sub-steps after context storage is stable.

## Current risk notes

- Native context is not implemented yet and must not be documented as complete.
- Stage X target onboarding remains deferred.
