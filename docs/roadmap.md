# roadmap

## Current baseline

Stage 7 is closed. The latest verified baseline before 2A is:

```text
HEAD: 71312088ed070f4cd305f3998980b64b75d9b341
Latest package: tul-doc-tree-compaction-stage1-readme-gate-fix-v1
Release gate: PASS
```

## Stage 8 — document tree compaction

### 2A: runtime pointer compaction

Package: `tul-doc-tree-compaction-stage2-pointer-compaction-v1`

Goal:

- narrow `tul show handoff` read-next to six active docs;
- narrow `tul verify` required docs to active docs only;
- stop `tul setup init` from recreating retired docs namespaces;
- keep compatibility files in place until deletion is safe.

Acceptance:

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

### 2B: compatibility and obsolete-doc deletion

Proceed only after 2A passes.

Candidate deletion groups:

```text
docs/llm/*
docs/protocols/*
docs/checklists/*
docs/handoff.md
docs/tracks/loop-runtime.md
docs/workflows/*
docs/experiments/*
templates/llm-initial-review-prompt.md
templates/llm-post-update-review-prompt.md
templates/project-harness/*
```

Use a narrow `git rm` list. Do not use broad deletion or `git add -A`.

## Deferred

- safe package-level delete support;
- broader runtime refactor;
- retired module cleanup;
- cross-repo onboarding;
- relocation decision for `docs/windows-dwork-environment.md`.
