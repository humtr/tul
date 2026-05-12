# Stage 7 bounded parallel planning

Stage 7 is the planning-control stage after the Stage 6 stabilization checkpoint.

The purpose is not to apply several packages at once. The purpose is to let several candidate workstreams be reasoned about in parallel while the runtime continues to accept one reviewed package at a time.

## Baseline

Use the latest user-provided `tul-vf-latest.md` as the runtime baseline. At the Stage 7 opening checkpoint, the accepted baseline is:

```text
HEAD: 5086c982ae5d52c586049d4fb21c8e7d4ada006d
Remote HEAD: 5086c982ae5d52c586049d4fb21c8e7d4ada006d
Release gate: PASS
Fresh clone verify: PASS
Latest package: tul-stage6-stabilization-checkpoint-bundle-v1
```

Use a source archive or fresh clone only when package generation or code-level diagnosis requires file contents.

## Core rule

```text
parallel planning, sequential gated update
```

This means:

1. Many candidate scopes may be compared.
2. One package is generated from the latest verified source baseline.
3. One package is applied with `tul update`.
4. One release gate closes the new baseline.
5. Only then may the next package be generated or applied.

## Stage 7 package classes

| Class | Meaning | Rule |
|---|---|---|
| Green | Disjoint docs/spec/template changes | Can be drafted in parallel, then applied one at a time. |
| Yellow | Shared coordination docs but no runtime behavior | Draft together or designate one owner package for final status/roadmap text. |
| Orange | Runtime code or release-gate logic changes | Serialize; produce one package only. |
| Red | Update/push/rollback/archive move/default export behavior | Serialize and require explicit risk, rollback, and acceptance gates. |

## Coordination files

The following files are coordination files:

```text
README.md
docs/manifest.md
docs/strategy.md
docs/roadmap.md
docs/status/current.md
docs/decisions.md
docs/learning-log.md
docs/checklists/loop-runtime.md
docs/checklists/planning-harness.md
```

If two candidate packages touch these files, serialize them unless one package is explicitly discarded or merged into the other. The final applied package owns the current status text.

## Runtime files

Runtime files include:

```text
bin/tul
lib/tulcore/*.py
```

Any runtime change is Orange or Red unless it is a version-only metadata bump. Runtime changes must state which behavior is changing and which command proves it.

## Artifact semantics files

Artifact semantics files include:

```text
docs/workflows/artifact-semantics.md
docs/llm/post-update-review.md
docs/llm/entrypoint.md
README.md
```

Do not split artifact vocabulary and artifact implementation into competing packages. If one package changes only vocabulary, mark it spec-only. If another changes runtime export behavior, wait for the spec package to close first.

## Candidate matrix at Stage 7 opening

| Candidate | Class | Apply timing |
|---|---|---|
| Stage 7 planning consolidation | Yellow | First |
| Acceptance gate template refinement | Green/Yellow | After consolidation baseline |
| Source export spec-only | Green | After consolidation baseline |
| Explicit `tul export source` implementation | Orange | After spec-only baseline |
| Docs drift checker | Orange | After planning docs stabilize |
| Review export automation | Red | Later decision only |
| Archive policy expansion | Red | Separate dry-run evidence first |
| Stage X target onboarding | Red | Deferred |

## Acceptance gate template

Every Stage 7 package must declare:

```text
Bundle name:
Goal:
Baseline HEAD:
Expected changed files:
Intentionally excluded files:
Parallel class:
Serialize because:
Acceptance criteria:
```

Minimum acceptance criteria:

```bash
tul package inspect <package.zip>
tul package check <package.zip> --target tul
tul package latest
tul update
# upload /sdcard/termux/import/tul/tul-vf-latest.md
```

The resulting latest artifact must show:

- Release gate PASS;
- matching HEAD and Remote HEAD;
- clean working tree;
- py_compile pass;
- git diff check pass;
- fresh clone pass;
- canonical latest verify artifact paths;
- runtime snapshots when expected.

## Exclusions for the first Stage 7 package

The first Stage 7 planning package should exclude:

- runtime behavior changes;
- source export implementation;
- review export automation;
- verify/pipeline/package hygiene/archive engine changes;
- external repo onboarding;
- force push, broad staging, deletion, or broad cleanup.

## Stop conditions

Stop and request a new baseline artifact or source context when:

- `tul-vf-latest.md` is missing, stale, or not PASS;
- the source archive does not plausibly correspond to the verified HEAD;
- two candidate packages both claim ownership of current status/roadmap text;
- runtime behavior changes are mixed with a large planning-doc rewrite;
- acceptance criteria cannot isolate the failure source.
