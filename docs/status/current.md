# Current status

Latest known version: `0.8.6-compact-gate-bundle`.

Current mode: Stage 6 bounded parallel bundle entry. Native context, package mismatch guidance, and update-integrated fresh verification are available. The update-integrated verify gate has passed smoke and is now treated as the normal loop baseline.

## Current verified loop

The intended normal self-host loop is:

```bash
tul package latest
tul update
# upload /sdcard/termux/import/tul/logs/verify/tul-vf-latest.md when review evidence is needed
```

`tul update` should print the update report first, including commit, push verification, rollback, changed files, and checks. It should then run a compact post-update `verify fresh` gate, write markdown/json verify artifacts, and print the LLM handoff. Because this package changes `verify.py`, the update process that applies it may still use the old verify layout for its own immediate post-update gate; one manual `tul verify fresh` after application confirms the new layout.

## Current bundle

Package: `tul_stage6_compact_gate_bundle_v1`

Commit message: `Compact verify gate and state output`

Scope:

1. Canonical verify log layout implementation.
2. Verify release-gate summary polish.
3. Compact default `tul state` output.
4. Docs/checklist consistency update for Stage 6 bounded parallel entry.

## Verify artifact convention

Canonical latest files remain directly under the verify log root:

```text
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.md
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.json
```

Timestamped run artifacts live in YYMMDD date folders directly under the verify log root. There is no `runs/` layer:

```text
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-153345-a1dcc39.md
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-f-260512-153345-a1dcc39.json
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-l-260512-153345-a1dcc39.md
/sdcard/termux/import/tul/logs/verify/260512/tul-vf-l-260512-153345-a1dcc39.json
```

Do not write both `vf` and `verify` naming families. `tul-vf-latest.md/json` are the only canonical latest artifacts. Legacy `tul-verify-latest.*` aliases are no longer generated.

## State output convention

Default `tul state` is a decision view: latest state, latest rollbackable commit, important artifacts, cleanup suggestion, and pointers to full history commands.

Long state output remains available with:

```bash
tul state --all --limit 5
tul state --json
```

## Next likely bundles

- authoring and diagnostics bundle;
- Windows parity bundle;
- archive recommendation polish;
- additional state cleanup UX if no-op/imported states keep accumulating.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.
