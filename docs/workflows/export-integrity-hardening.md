# export integrity hardening

Export integrity is inspected through:

```bash
tul show exports
```

It is warning-only. It does not affect release gate unless a later decision promotes specific checks.

## Source bundle checks

- zip exists;
- zip test passes;
- `source-manifest.json` exists;
- manifest HEAD matches current HEAD for current status;
- root layout is `repo-files-at-zip-root`;
- state-recorded SHA matches actual SHA when recorded.

## Review bundle checks

- zip exists;
- manifest HEAD matches current HEAD for current status;
- changed file count is available;
- latest state records the bundle when expected.

## Docs drift

Docs drift diagnostics are small active-ledger checks. They should not be mistaken for a full documentation audit.
