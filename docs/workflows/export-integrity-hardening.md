# Stage 7 export integrity hardening

Status: active package target for `tul-stage7-export-integrity-hardening-bundle-v1`.

This workflow adds warning-only integrity checks around explicit source and review exports. It is the first compressed Stage 7 implementation step after explicit source export.

## Scope

This package combines three previously separate candidates:

1. export consistency hardening;
2. source bundle freshness warning;
3. docs drift checker.

It intentionally does not implement post-update automatic export. That remains the next Red-class package candidate.

## Command surface

```bash
tul export status
tul export status --json
tul state
tul verify fresh
```

`tul export status` is read-only. It inspects existing artifacts and repo documents, then prints warnings. It must not create, overwrite, stage, commit, push, archive, or delete anything.

## Source bundle checks

The checker inspects the default explicit source export path, normally:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
```

It verifies:

- zip readability;
- required metadata entries;
- `source-manifest.json` parseability;
- root layout equals `repo-files-at-zip-root`;
- manifest HEAD matches current repo HEAD;
- actual zip SHA256 matches the latest state record when the latest state records one.

If the source bundle exists but manifest HEAD differs from current HEAD, the status is `stale` and the user should run:

```bash
tul export source
```

## Review bundle checks

The checker inspects the default explicit review export path, normally:

```text
/sdcard/termux/import/tul/tul-review-latest.zip
```

It verifies:

- zip readability;
- required review entries;
- `export-manifest.json` parseability;
- review manifest HEAD matches current repo HEAD when present;
- whether the bundle is recorded in the latest state.

Review bundle absence is not automatically a failure. Some updates only need source context and release evidence.

## Docs drift checks

The initial docs drift checker is intentionally small and warning-only. It checks:

- `docs/status/current.md`;
- `docs/roadmap.md`;
- `docs/manifest.md`.

It warns if:

- current status does not mention the latest package recorded in tul state;
- docs still describe `tul export source` as not implemented or as only a future command after implementation has landed.

The checker should grow only after observed false positives are understood.

## Gate effect

Export integrity warnings do not fail the release gate in this package. They are advisory evidence for the user and the next LLM session.

Future packages may promote selected warnings to gate checks, but only after a separate acceptance gate.

## Acceptance

- `tul export status` prints source, review, and docs drift sections.
- `tul export status --json` prints machine-readable data.
- `tul state` includes the same warning-only export status after compact state.
- `tul verify fresh` includes a `tul export status` runtime snapshot.
- stale source bundles are warnings, not release gate failures.
- docs drift warnings are warnings, not release gate failures.
- existing `tul export source` and `tul export review` behavior remains unchanged.
