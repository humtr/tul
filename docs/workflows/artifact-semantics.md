# Artifact semantics checkpoint

This document freezes the Stage 7 artifact vocabulary after the Stage 6 source/review export discussion exposed a design problem: verification evidence, handoff evidence, source transfer, review transfer, and backup were being treated as one thing.

## Current baseline

Verified baseline after explicit source export implementation:

```text
a5db5d01d96277e83913ec17506c22e3284424eb
```

Known runtime facts:

- `tul-vf-latest.md` lives at `/sdcard/termux/import/tul/tul-vf-latest.md`.
- Timestamped verify run artifacts live under `/sdcard/termux/import/tul/logs/verify/YYMMDD/`.
- `tul-vf-latest.md` includes compact `tul state` and `tul handoff` snapshots.
- `tul export review` writes `/sdcard/termux/import/tul/tul-review-latest.zip` and records review bundle evidence in state/report/handoff.
- Automatic `tul-main.zip` export is not a closed capability.
- `tul export source` is implemented as an explicit manual source-context export command.
- `tul export status` is the warning-only freshness and docs-drift inspection surface.
- The source-export contract is documented in `docs/workflows/source-export-spec.md`.
- A GitHub-generated `tul-main.zip` may be used as manual source context if the root layout and intended commit are understood, but it is not a tul runtime backup or a tul-proven explicit source export.

## Standard vocabulary

| Term | Current meaning |
|---|---|
| Runtime baseline | The latest `tul-vf-latest.md` evidence for HEAD, Remote HEAD, release gate, working tree, and fresh clone status. |
| Review bundle | Implemented compact diff/review transport created by `tul export review`. |
| Source context | File contents used for code-level diagnosis or package generation. Prefer an explicit source export, then a fresh clone, then a GitHub source archive as fallback. |
| Source export | Implemented explicit manual tul command/artifact for full source context with provenance. |
| GitHub source archive | Manual source context, usually with a wrapper root such as `tul-main/`. Not tul-proven runtime evidence. |
| Backup/recovery authority | Git remote, commit hashes, and tul rollback state. Zip artifacts are not backup authority. |

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

### Source context

Purpose: full repo source contents for package generation or code-level diagnosis.

Current accepted source-context providers:

- a GitHub-generated source archive such as `tul-main.zip`, after checking root layout and intended commit;
- a fresh clone at the verified commit;
- a manually created source zip, if its generation command and root layout are understood.

Source context is not automatically runtime evidence. A source archive can be useful for reading files without becoming backup authority.

### Source export

Purpose: tul-generated full repo source context with provenance.

Implemented manual command:

```bash
tul export source
```

Default update behavior after the post-update export automation package closes: a successful normal `tul update` refreshes the source bundle after commit, push, and fresh verification. Export failures are warning-only and do not change release-gate, commit, push, or rollback facts.

Latest path:

```text
/sdcard/termux/import/tul/tul-source-latest.zip
```

A tul-proven source export must record:

- command that produced it;
- HEAD and remote HEAD at export time when available;
- root layout evidence;
- sha256;
- byte size;
- file count;
- exclusion rules.

A canonical tul source export should have repo files at zip root, for example:

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
update -> verify -> state/handoff -> optional explicit review export -> future optional explicit source export
```

Full source export remains explicit and unimplemented until its root-layout, freshness, and provenance checks are implemented and verified. The pre-implementation specification is accepted in `docs/workflows/source-export-spec.md`, but the command remains non-runnable.

## Current implementation status

`repozip.py` remains a retired helper from the source-zip experiment, but current source export is implemented separately through `lib/tulcore/source.py` and `tul export source`. J2 removed misleading source zip state output. J3 added explicit `tul export review` for diff-oriented review bundles. J4 records the explicit review export in state/report/handoff and refreshes latest runtime snapshots. Stage 7 adds explicit source export as a manual command; automatic source export remains out of the default update loop.

## Next bundles

1. Keep review export explicit and evidence-backed.
2. Keep terminology clear: runtime baseline, review bundle, source context, proposed source export, and backup are separate roles.
3. Keep the accepted source export spec in `docs/workflows/source-export-spec.md`.
4. Keep `tul export source` explicit-only unless a later Red-class automation decision closes.
5. Reconsider automatic review export only after explicit behavior remains stable across additional packages.

## Export integrity status

`tul export status` is the warning-only inspection surface for source/review export freshness and small docs drift checks. It may be run manually or captured in verify snapshots. After the post-update export automation package closes, normal `tul update` should leave source/review artifacts current; stale/missing/invalid artifacts remain warnings, not release-gate failures.
