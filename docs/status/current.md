# Current status

Latest known version after this package: `0.8.1-native-context-readonly`.

Current mode: Stage 6 native context step 2 — active project context exists and read-only commands can infer project targets. No-arg update is still deferred.

## Current verified loop

The current normal self-host loop is:

```bash
tul package latest tul
tul update tul -l
tul verify fresh
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

## Current package

`tul_native_context_v1b`

Implemented scope:

- read-only no-arg project inference for `status`, `check`, `verify`, `state`, `handoff`, `report`, `package latest`, and `package list`.
- `tul verify fresh` shorthand for fresh-clone verification.
- current-directory project inference.
- read-only conflict warning when active project and current directory project differ.
- previous v1a scope remains: `tul use`, `tul current`, context storage, and default project support.

## Next package

`tul_native_context_v1c`

Expected scope:

- no-arg mutating command inference for `tul update`;
- context conflict guard for active project vs current directory;
- explicit target/package selection banner.

Package mismatch guidance remains a later sub-step after no-arg mutating commands are stable.

## Current risk notes

- Native context is partially implemented. Read-only commands infer targets; no-arg update is still not implemented.
- Stage X target onboarding remains deferred.
