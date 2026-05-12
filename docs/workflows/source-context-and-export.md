# Source context and source export

This document prevents one specific ambiguity: source context can come from several places, but only tul-generated source export has tul provenance.

## Current rule

`tul export source` is implemented as an explicit command. After the post-update export automation package closes, normal `tul update` also refreshes the source bundle after successful commit, push, and fresh verification. It remains separate from `tul verify` and `tul export review`, and export failures are warning-only.

Current package-generation sessions may use source context from:

- `tul export source`, which writes a tul-proven source bundle;
- a GitHub-generated source archive such as `tul-main.zip`;
- a fresh clone at the verified commit;
- a manually created source zip whose generation command, root layout, and intended commit are known.

Only the first is a tul-proven explicit source export. The others remain manual source context.

## Current commands

```bash
tul export review
tul export source
tul export source --json
tul export source --out /path/to/tul-source-latest.zip
```

## Current source-context vocabulary

| Term | Use |
|---|---|
| `tul-main.zip` | Usually a GitHub-generated archive. Valid as manual source context when root layout and intended commit are understood. |
| `tul-review-latest.zip` | Implemented review/diff transport from `tul export review`. Not full source context. |
| `tul-source-latest.zip` | Implemented explicit full source-context bundle from `tul export source`. |
| `tul export source` | Explicit source export command; also used by the post-update export phase after successful updates. |

## Required checks before using source context

Before treating any source archive as package-generation input, check:

1. the runtime baseline from `tul-vf-latest.md`;
2. the archive root layout, for example whether it has a wrapper directory such as `tul-main/`;
3. whether the archive corresponds to the verified HEAD;
4. whether the files needed for the package are present;
5. whether the source context is being used only for reading/writing package payloads, not as backup evidence.

For a tul-generated source export, also check:

- `source-manifest.json`;
- `source-file-list.txt`;
- `source-file-sha256s.txt`;
- command output or state metadata for final archive SHA256, payload SHA256, byte count, source file count, root layout, rewritten, and verified-after-replace evidence.

## Boundary

Source export is explicit as a manual command and automatic as a post-update refresh after successful default updates. The automatic phase is intentionally after commit, push, and fresh verification, and failures are warning-only.

## Export status

`tul export status` is the warning-only inspection surface for source/review export freshness and small docs drift checks. It may be run manually or captured in verify snapshots. After the post-update export automation package closes, normal `tul update` should leave source/review artifacts current; stale/missing/invalid artifacts remain warnings, not release-gate failures.
