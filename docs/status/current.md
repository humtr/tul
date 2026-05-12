# Current status

Latest known version after this package: `0.8.0-native-context-a`.

Current mode: Stage 6 native context step 1 — active project context is stored, but no-arg update is still deferred.

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

## Current package

`tul_native_context_v1a`

Implemented scope:

- `tul use <project>`.
- `tul current`.
- active project context storage.
- optional default project support through `tul use <project> --default`.
- `tul projects` active/default display.
- `tul doctor` runtime context display.

## Next package

`tul_native_context_v1b`

Expected scope:

- no-arg read-only commands;
- `tul verify fresh` shorthand;
- current-directory project inference;
- read-only conflict banner.

Native no-arg update and package mismatch guidance should remain later sub-steps after read-only inference is stable.

## Current risk notes

- Native context is only partially implemented. `tul use` and `tul current` exist; no-arg update is still not implemented.
- Stage X target onboarding remains deferred.
