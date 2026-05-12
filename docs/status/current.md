# Current status

Latest known version after this package: `0.8.2-native-context-update`.

Current mode: Stage 6 native context step 3 — active project context exists, read-only commands infer targets, and guarded no-arg mutating commands are available for update/import/rollback.

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

`tul_native_context_v1c`

Implemented scope:

- no-arg `tul update` as inferred project + latest matching package.
- no-arg `tul import` and `tul rollback` with mutating context inference.
- mutating-command conflict guard for active project vs current directory project.
- target inference banner for no-arg mutating commands.
- previous v1a/v1b scope remains: `tul use`, `tul current`, read-only no-arg commands, and `tul verify fresh`.

## Next package

`tul_native_context_v1d`

Expected scope:

- package manifest mismatch guidance;
- classification of matching, incompatible, invalid, and duplicate downloaded packages;
- clearer next-command suggestions when the newest downloaded zip targets another project.

## Current risk notes

- Native context is mostly implemented for target inference. Package mismatch guidance is still pending.
- Stage X target onboarding remains deferred.
