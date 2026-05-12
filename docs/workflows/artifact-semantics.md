# Artifact semantics checkpoint

This document freezes the current Stage 6 artifact vocabulary after the repo zip export work exposed a design problem: verification evidence, handoff evidence, source transfer, review transfer, and backup were being treated as one thing.

## Current baseline

Verified baseline: `da00aae271a82473f0958e4e66416a4d6f9d5801`.

Known runtime facts:

- `tul-vf-latest.md` lives at `/sdcard/termux/import/tul/tul-vf-latest.md`.
- Timestamped verify run artifacts live under `/sdcard/termux/import/tul/logs/verify/YYMMDD/`.
- `tul-vf-latest.md` includes compact `tul state` and `tul handoff` snapshots.
- `tul-main.zip` export is not yet a closed capability. A path in state is not sufficient proof that the export was produced by the current update, has the expected root layout, or matches the verified HEAD.

## Artifact roles

### Verify artifact

Purpose: release-gate evidence.

Canonical latest:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-vf-latest.json
```

The verify artifact records release gate status, HEAD/remote HEAD, checks, run artifact paths, and runtime snapshots. It is not a source archive and should not create source archives.

### Runtime state

Purpose: latest update decision view.

`tul state` should summarize the latest state, latest rollbackable commit, important artifacts, and cleanup suggestions. It must not display an artifact as successful unless the runtime has recorded evidence that the artifact was actually produced.

### Handoff artifact

Purpose: fresh-session orientation.

`tul handoff` and the handoff file should tell the next LLM where to start and which facts are runtime facts. Handoff should not grow into a full repo dump.

### Review bundle

Purpose: compact upload artifact for the next LLM review or diff-oriented diagnosis.

Proposed future latest path:

```text
/sdcard/termux/import/tul/tul-review-latest.zip
```

Expected contents:

```text
tul-vf-latest.md
state.json
handoff.md
git-log-latest.txt
changed-files.txt
diff.patch
files/<changed repo files>
```

The review bundle is not a backup. It should carry the smallest useful evidence for change tracking.

### Source bundle

Purpose: full repo source context for package generation or code-level diagnosis.

Proposed future explicit command:

```bash
tul export source
```

Proposed latest path:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
```

A source bundle must have repo files at zip root, for example:

```text
README.md
.tul.yml
bin/tul
lib/tulcore/__init__.py
```

A wrapper directory such as `tul-main/README.md` is not the canonical source-bundle shape.

### Backup

Purpose: recovery.

Backups are not zip exports. The durable backup and rollback authority is Git remote plus commit hashes and tul rollback state. Zip artifacts are transport artifacts for review or package generation.

## Corrected design rule

Do not model the update loop as:

```text
update -> verify -> export source zip
```

The safer model is:

```text
update -> verify -> state/handoff -> optional review export
```

Full source export remains explicit until its root-layout, freshness, and provenance checks are implemented and verified.

## Current implementation status

`repozip.py` exists, but automatic `tul-main.zip` export is retired from the default update loop. J2 removes misleading source zip state output. Future implementation should add explicit review/source export commands with evidence instead of reviving hidden update-side source export.

## Next bundles

1. Implement `tul export review` for diff-oriented review bundles.
3. Implement `tul export source` for explicit source bundles with root-layout checks.
4. Reconsider whether `tul update` should run review export automatically only after the review/source split is stable.
