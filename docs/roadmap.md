# roadmap

## Current baseline

Stage 7 is closed. Stage 8 document tree compaction is reducing active documentation to a small stable set.

Latest verified baseline before 2B:

```text
HEAD: b7c2007753bb12eae23c5328b3b8d3be15e2f034
Latest package: tul-doc-tree-compaction-stage2-pointer-compaction-v1
Release gate: PASS
Read-next: six active docs
Docs drift: clean
```

## Stage 8 — document tree compaction

### 2A: runtime pointer compaction

Status: done.

Acceptance achieved:

```text
tul verify fresh: PASS
tul show handoff read-next:
  README.md
  docs/status/current.md
  docs/manifest.md
  docs/roadmap.md
  docs/commands.md
  docs/package-spec.md
docs drift: clean
```

### 2B: obsolete-doc deletion

Status: in progress.

Goal:

- remove retired compatibility docs;
- remove obsolete workflow and experiment records from the active tree;
- remove old prompt and project-harness templates;
- retain durable decision and lesson records;
- keep the Windows environment note deferred rather than deleting it.

Acceptance:

```text
tul verify fresh: PASS
tul show handoff read-next remains six active docs
tul show exports reports current source/review bundles
docs drift: clean
source bundle file count decreases from the pre-2B count
```

## Deferred

- safe package-level delete support;
- broader runtime refactor;
- retired module cleanup;
- cross-repo onboarding;
- relocation decision for docs/windows-dwork-environment.md.
