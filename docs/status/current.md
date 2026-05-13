# current status

Status: **Stage 8 document tree compaction is closed.**

Verified repo baseline:

```text
Project: tul
Repo: humtr/tul
Branch: main
HEAD: fb7ea10b93371e33f0f90a61e949eb621a7087b3
Remote HEAD: fb7ea10b93371e33f0f90a61e949eb621a7087b3
Release gate: PASS
Steps: 33 pass, 0 fail
Fresh clone: PASS
Working tree: clean
Docs drift: clean
```

## Closed work

```text
Stage 1: active docs were consolidated into canonical owners.
2A: runtime handoff/read-next and verify required-doc pointers were narrowed.
2B: obsolete compatibility/workflow/experiment/template documents were removed.
Stage 8 finalization: active ownership overlap is closed in README, status, manifest, roadmap, commands, package-spec, and templates.
```

## Active read-next

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

Supporting ledgers:

```text
docs/decisions.md
docs/learning-log.md
```

Deferred environment note:

```text
docs/windows-dwork-environment.md
```

Retained templates:

```text
templates/llm-handoff-prompt.md
templates/milestone-checklist.md
templates/project-instructions.md
```

## Artifact status boundary

The source bundle is the source-context transport artifact and is current at the Stage 8 deletion baseline with 47 files.

The review bundle can remain stale after a narrow manual `git rm` deletion commit because the latest package state still points at the previous package-run state. This does not invalidate the release gate or the source tree compaction; it is a known artifact/state-model boundary and a candidate for a later review/state-model improvement.

## Current command surface

The canonical top-level commands remain:

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

Normal loop:

```bash
tul run
```

## Next

No further document-tree compaction is required.

Optional later work belongs outside Stage 8:

```text
- make manual git rm / delete commits produce current review evidence;
- add safe package-level delete support, if explicitly approved;
- decide whether docs/windows-dwork-environment.md belongs in this repo or a separate environment notebook.
```
