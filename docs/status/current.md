# current status

Status: Macro Stage A is closed through the head-tagged source/review/verify upload loop. Macro Stage B starts from artifact consistency and docs/runtime truth separation.

Macro Stage B artifact-consistency hardening is closed for source bundle currentness: dirty source snapshots, payload/hash/list mismatches, and exporter-rejected unsafe paths are no longer allowed to appear as current source evidence.

## Runtime truth

Current runtime facts are not stored in this document. Use the head-tagged verify markdown and runtime commands:

```text
tul-vf-<head7>.md
tul show
tul show exports
```

The latest package identity belongs to state, `tul show`, `tul show exports`, and the verify artifact. This document should not be updated merely to mention the latest package name.

## Active read-next set

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

## Validation target

```bash
tul package
tul run
```

Expected result: the final screen says `Decision: PASS`, release gate PASS, CLI runtime smoke PASS, regression tests PASS, source/review current, docs drift clean, warnings none, and head-tagged upload files are printed.

## Artifact readiness

Fresh devices may have a synced repo before they have local transport artifacts or tul run state. `tul verify` regression tests must therefore validate the `show exports` command surface without requiring source/review artifacts to already be current or recorded in latest state. Artifact readiness remains a post-export/run acceptance condition.

## Cross-project application

`tul` exists to help development work in other projects, so artifact checks should generalize as operational guardrails, not as tul-only bookkeeping:

```text
- if an exporter rejects a path, the inspector must reject the same path;
- if an artifact records manifest, file list, size, and hash evidence, currentness must recompute and compare that evidence;
- dirty snapshots may be useful diagnosis material, but they are not current clean-HEAD evidence;
- platform-local scratch and review output belongs in the platform-safe temp root, such as ~/tmp on Termux;
- runtime truth belongs in head-tagged artifacts and tul show output, not in static status prose.
```
