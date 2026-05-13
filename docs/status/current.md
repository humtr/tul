# current status

Status: **Stage 8 document tree compaction is closed; Stage 9A review artifact freshness hardening is being applied.**

Runtime truth remains `tul-vf-latest.md` and `tul show`. This file records the latest durable status summary and must mention the latest package so docs-drift checks can stay clean.

## Verified baseline before this package

```text
Project: tul
Repo: humtr/tul
Branch: main
Verified HEAD: 4b3354678b476d34a9d741b1db64247f5ccc8942
Remote HEAD: 4b3354678b476d34a9d741b1db64247f5ccc8942
Release gate: PASS
Steps: 33 pass, 0 fail
Fresh clone: PASS
Working tree: clean
Source bundle: current, 47 files
Review bundle: current, 9 changed files
```

## Latest package marker

```text
Latest package: tul-stage9a-review-current-head-export-v1
```

After this package is applied, the exact post-apply commit hash is recorded by `tul-vf-latest.md`, `tul show`, and Git remote state.

## Closed work

```text
Stage 1: active docs were consolidated into canonical owners.
2A: runtime handoff/read-next and verify required-doc pointers were narrowed.
2B: obsolete compatibility/workflow/experiment/template documents were removed.
Stage 8 ownership finalization: active ownership overlap was closed.
Environment note normalization: Windows D:\work was moved conceptually under a general environment-profile area.
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

Environment profiles:

```text
docs/environments/README.md
```

Retained templates:

```text
templates/llm-handoff-prompt.md
templates/milestone-checklist.md
templates/project-instructions.md
```

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
- split large runtime modules only when a concrete feature requires it.
```

## Stage 9A focus

```text
Problem: `tul export review` could create a freshly written but stale review bundle after manual Git commits because it used the latest tul state commit and changed_files as its primary review basis.
Resolution package: tul-stage9a-review-current-head-export-v1
Expected behavior: review export manifests use the current Git HEAD as `head`; the latest tul state commit is recorded only as `state_commit` context.
Acceptance: `tul export review` followed by `tul show exports` reports Review bundle status: current for the current HEAD.
```
