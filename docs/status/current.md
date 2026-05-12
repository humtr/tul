# Current status

Latest known version: `0.8.8-archive-cleanup-dryrun-bundle`.

Current mode: Stage 6 bounded parallel self-host hardening. Native context, package mismatch guidance, update-integrated fresh verification, canonical verify artifact layout, compact state output, package authoring diagnostics, and archive dry-run guidance are available. The compact gate and authoring diagnostics bundles have passed release gate and are now normal loop baseline behavior.

## Current verified loop

The intended normal self-host loop is:

```bash
tul package latest
tul update
# upload /sdcard/termux/import/tul/logs/verify/tul-vf-latest.md when review evidence is needed
```

`tul update` should print the update report first, including commit, push verification, rollback, changed files, and checks. It should then run a compact post-update `verify fresh` gate, write markdown/json verify artifacts, and print the LLM handoff. New verify runs use the canonical layout without requiring an extra bootstrap command.

## Current bundle

Package: `tul_stage6_archive_cleanup_dryrun_bundle_v1`

Commit message: `Improve archive cleanup dry-run output`

Scope:

1. Make `tul state` recommend archive dry-run before cleanup.
2. Allow `tul archive` to use guarded native context when the project target is omitted.
3. Print work-state inventory, selected cleanup class, keep count, archive root, and protected reference states.
4. Improve `tul archive --noop --dry-run --keep N` output without adding automatic destructive cleanup.
5. Preserve verify, update, rollback, package authoring, and Windows behavior for later bundles.

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

## Package authoring convention

Before distribution, a package should pass:

```bash
tul package check /path/to/package.zip --target tul
```

The check should identify:

- missing or nested root `tul-package.yml`;
- missing root `README.md`;
- absent or unreferenced `files/` payload;
- generated/cache files in the archive;
- `apply.files` sources that are missing from payload;
- destination/`commit.files` mismatches;
- target project/repo/branch mismatches when `--target` is supplied.

## State cleanup convention

State cleanup is intentionally dry-run first. Routine inspection should use:

```bash
tul archive --noop --dry-run --keep 3
```

The dry-run output should show inventory counts, selected state directories, destination archive directories, latest state, and latest rollbackable state before any files are moved. Actual archive moves remain explicit by re-running without `--dry-run` after review.

## Next likely bundles

- handoff discoverability bundle;
- parallel-readiness gate bundle;
- Windows parity bundle;
- parallel-readiness gate bundle.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.
