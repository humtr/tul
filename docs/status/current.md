# current status

Status: Macro Stage A is closed through the head-tagged source/review/verify upload loop. Macro Stage B starts from artifact consistency and docs/runtime truth separation.

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
