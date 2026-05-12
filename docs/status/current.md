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

`tul_update_verify_gate_smoke_v1`

Purpose:

- make the next normal `tul update` exercise the update-integrated fresh verification gate;
- prove that one command can apply, commit, push, verify remote HEAD, run fresh verification, and write the uploadable verify artifact;
- preserve the visible order: update report, commit/push/rollback, fresh verification gate, then LLM handoff.

Baseline implemented by `tul_update_verify_gate_v1`:

- normal `tul update` runs post-update `verify fresh`;
- fresh verify markdown/json artifacts are written automatically;
- update report, state, and handoff include verify gate result and artifact paths;
- terminal output order is update report → verify fresh summary → LLM handoff;
- `--no-verify` is available for exceptional debugging paths.

## Next package

Bundle 6 — State compactness and docs consistency

Expected scope:

- compact state output;
- archive recommendations;
- docs consistency checks;
- further release-gate polish if update output remains too verbose.

## Current risk notes

- Native context package guidance is implemented.
- Update-integrated release-gate artifacts are implemented and this smoke package is intended to verify that the integration works on the next package application.
- If `tul update` does not refresh `tul-vf-latest.md` to the smoke commit, the release-gate integration needs a follow-up fix.
- State-compact output remains pending.
- Stage X target onboarding remains deferred.

## Smoke-test expectation

After applying `tul_update_verify_gate_smoke_v1`, the user should be able to upload only:

```text
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.md
```

The artifact HEAD should match the new smoke-test commit. If it still points at the previous commit, the post-update verify hook did not run or did not refresh the latest artifact.
