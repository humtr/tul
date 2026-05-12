# Artifact semantics checkpoint

This document freezes the Stage 7 artifact vocabulary after the Stage 6 source/review export discussion exposed a design problem: verification evidence, handoff evidence, source transfer, review transfer, and backup were being treated as one thing.

## Current baseline

Verified baseline at Stage 7 opening:

```text
5086c982ae5d52c586049d4fb21c8e7d4ada006d
```

Known runtime facts:

- `tul-vf-latest.md` lives at `/sdcard/termux/import/tul/tul-vf-latest.md`.
- Timestamped verify run artifacts live under `/sdcard/termux/import/tul/logs/verify/YYMMDD/`.
- `tul-vf-latest.md` includes compact `tul state` and `tul handoff` snapshots.
- `tul export review` writes `/sdcard/termux/import/tul/tul-review-latest.zip` and records review bundle evidence in state/report/handoff.
- Automatic `tul-main.zip` export is not a closed capability.
- A GitHub-generated `tul-main.zip` may be used as manual source context if the root layout and intended commit are understood, but it is not a tul runtime backup or a tul-proven explicit source export.

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

Current explicit command:

```bash
tul export review
```

Current latest path:

```text
/sdcard/termux/import/tul/tul-review-latest.zip
```

Expected contents:

```text
tul-vf-latest.md
state.json
report.md
handoff.md
git-head.txt
git-log-latest.txt
working-tree.txt
changed-files.txt
diff.patch
files/<changed repo files only>
export-manifest.json
```

The review bundle is not a backup and not a full source archive. It carries the smallest useful evidence for change tracking and LLM review.

### Source bundle

Purpose: full repo source context for package generation or code-level diagnosis.

Future explicit command:

```bash
tul export source
```

Future latest path:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
```

A tul-proven source bundle must record:

- command that produced it;
- HEAD and remote HEAD at export time when available;
- root layout evidence;
- sha256;
- byte size;
- file count;
- exclusion rules.

A canonical tul source bundle should have repo files at zip root, for example:

```text
README.md
.tul.yml
bin/tul
lib/tulcore/__init__.py
```

A wrapper directory such as `tul-main/README.md` is not the canonical tul source-export shape. A GitHub-generated archive may still be useful manual source context; it just has different provenance semantics.

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
update -> verify -> state/handoff -> optional explicit review export -> optional explicit source export
```

Full source export remains explicit until its root-layout, freshness, and provenance checks are implemented and verified.

## Current implementation status

`repozip.py` exists, but automatic `tul-main.zip` export is retired from the default update loop. J2 removed misleading source zip state output. J3 added explicit `tul export review` for diff-oriented review bundles. J4 records the explicit review export in state/report/handoff and refreshes latest runtime snapshots. Stage 7 should add explicit source export only after the spec and acceptance gate are accepted.

## Next bundles

1. Keep review export explicit and evidence-backed.
2. Write a source export spec before implementation.
3. Implement `tul export source` for explicit source bundles with root-layout checks if source context remains a repeated bridge cost.
4. Reconsider automatic review export only after explicit behavior remains stable across additional packages.
