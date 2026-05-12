# Current status

Latest known version: `0.8.7-authoring-diagnostics-bundle`.

Current mode: Stage 6 bounded parallel self-host hardening. Native context, package mismatch guidance, update-integrated fresh verification, canonical verify artifact layout, and compact state output are available. The compact gate bundle has passed release gate and is now the normal loop baseline.

## Current verified loop

The intended normal self-host loop is:

```bash
tul package latest
tul update
# upload /sdcard/termux/import/tul/logs/verify/tul-vf-latest.md when review evidence is needed
```

`tul update` should print the update report first, including commit, push verification, rollback, changed files, and checks. It should then run a compact post-update `verify fresh` gate, write markdown/json verify artifacts, and print the LLM handoff. New verify runs use the canonical layout without requiring an extra bootstrap command.

## Current bundle

Package: `tul_stage6_authoring_diagnostics_bundle_v1`

Commit message: `Improve package authoring diagnostics`

Scope:

1. Strengthen `tul package check` diagnostics for root layout, manifest, payload, and commit file consistency.
2. Improve invalid archive and no-match remediation guidance.
3. Keep package authoring guidance aligned with the bounded self-host loop.
4. Preserve verify, pipeline, rollback, and Windows behavior for later bundles.

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

## Next likely bundles

- archive cleanup dry-run bundle;
- handoff discoverability bundle;
- Windows parity bundle;
- parallel-readiness gate bundle.

## Deferred

Stage X target onboarding, including `humtr/ai`, remains deferred until tul's self-host loop is stable enough to reduce rather than increase bridge work.
