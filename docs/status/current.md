# current status

Status: Stage 7 is closed. Stage 8 document tree compaction is in progress.

Current verified baseline before this package:

```text
HEAD: 71312088ed070f4cd305f3998980b64b75d9b341
Remote HEAD: 71312088ed070f4cd305f3998980b64b75d9b341
Latest package: tul-doc-tree-compaction-stage1-readme-gate-fix-v1
Release gate: PASS
Steps: 33 pass, 0 fail
Fresh clone: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

Current package under review: `tul-doc-tree-compaction-stage2-pointer-compaction-v1`.

## Current objective

2A narrows runtime document pointers without deleting files:

- `tul show handoff` read-next should point only to active docs.
- `tul verify` required-doc checks should require active docs only.
- `tul setup init` should not recreate retired documentation namespaces.
- README, status, roadmap, manifest, command, and package-spec docs should describe the same active tree.

## Active read-next set

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

## Compatibility layer

The following files may still exist after 2A, but they are no longer active sources of truth once this package is applied:

```text
docs/llm/*
docs/protocols/*
docs/checklists/*
docs/handoff.md
docs/tracks/loop-runtime.md
docs/workflows/parallel-readiness.md
templates/llm-initial-review-prompt.md
templates/llm-post-update-review-prompt.md
```

Actual deletion is deferred to 2B because the safe package apply mechanism supports `apply.mode: copy`, not delete operations.

## Canonical command surface

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

## Normal loop

```bash
tul run
```

Semantics:

```text
package found:
  update -> export -> verify fresh -> show

package not found:
  export -> verify fresh -> show
```

## Next queue

1. Apply `tul-doc-tree-compaction-stage2-pointer-compaction-v1`.
2. Confirm `tul verify fresh` reports PASS.
3. Confirm `tul show handoff` read-next lists only the active six docs.
4. Proceed to 2B: narrow `git rm` cleanup of compatibility and obsolete docs.
