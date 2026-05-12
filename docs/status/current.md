# Current status

Latest known version after this package: `0.8.4-update-verify-gate`.

Current mode: Stage 6 release-gate integration — native context and package mismatch guidance are available, and normal `tul update` now runs a post-update fresh verification gate.

## Current verified loop

The current normal self-host loop is now:

```bash
tul package latest
tul update
# upload /sdcard/termux/import/tul/logs/verify/tul-vf-latest.md when review evidence is needed
```

`tul update` prints the update report first, including commit, push verification, and rollback. It then runs a compact `verify fresh` release gate, writes the markdown/json verify artifacts, and prints the LLM handoff.

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

`tul_update_verify_gate_v1`

Implemented scope:

- normal `tul update` runs post-update `verify fresh`;
- fresh verify markdown/json artifacts are written automatically;
- update report, state, and handoff include verify gate result and artifact paths;
- terminal output order is update report → verify fresh summary → LLM handoff;
- `--no-verify` is available for exceptional debugging paths.

## Next package

Next Stage 6 bundle

Expected scope:

- compact state output;
- archive recommendations;
- docs consistency checks;
- further release-gate polish if update output remains too verbose.

## Current risk notes

- Native context package guidance is implemented. Update-integrated release-gate artifacts are implemented; state-compact output remains pending.
- Stage X target onboarding remains deferred.
