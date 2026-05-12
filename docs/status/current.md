# Current status

Latest known version after this package: `0.8.3-native-context-package-guidance`.

Current mode: Stage 6 native context step 4 — active project context, no-arg read-only commands, guarded no-arg mutating commands, and package manifest mismatch guidance are available.

## Current verified loop

The current normal self-host loop is:

```bash
tul package latest
tul update
tul verify fresh
tul handoff
```

`PKG=...` should be exceptional. Normal use should prefer inbox discovery and native `tul update` when context is unambiguous.

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

## Current package

`tul_native_context_v1d`

Implemented scope:

- package discovery classifies matching, incompatible, and invalid inbox archives.
- `tul package latest` and `tul package list` explain incompatible package targets.
- no-match errors now show package manifest mismatch details and next command options.
- previous v1a/v1b/v1c scope remains: `tul use`, `tul current`, read-only no-arg commands, `tul verify fresh`, and guarded no-arg update/import/rollback.

## Next package

Next Stage 6 bundle

Expected scope:

- release gate summary for `tul verify`;
- compact state output;
- archive recommendations;
- docs consistency checks.

## Current risk notes

- Native context package guidance is implemented; release-gate and state-compact output remain pending.
- Stage X target onboarding remains deferred.
