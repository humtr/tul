# Stage 7 bounded parallel planning

Stage 7 is the planning-control stage after the Stage 6 stabilization checkpoint.

The operating rule is:

```text
parallel planning, sequential gated update
```

Multiple candidate bundles may be planned, compared, and rejected in parallel. Only one package is applied at a time, and each applied package must close with a new `tul-vf-latest.md` release-gate artifact.

## Current runtime baseline

Use the latest user-provided `tul-vf-latest.md` as the runtime baseline. At the terminology-audit checkpoint, the accepted baseline is:

```text
HEAD: 7d7b27a4eb81570482ff4d9eaba1dc7c83429272
Remote HEAD: 7d7b27a4eb81570482ff4d9eaba1dc7c83429272
Release gate: PASS
Fresh clone: PASS
Latest package: tul-stage7-terminology-audit-bundle-v1
```

If a newer artifact is available, it supersedes this document.

## Stage 7 package classes

| Class | Meaning | Typical work |
|---|---|---|
| Green | Isolated docs/templates with no runtime behavior and no ownership of current status. | copy-ready prompts, minor checklists, local wording cleanup |
| Yellow | Coordination docs, status/roadmap, artifact vocabulary, or spec-only packages. | source-export spec, package gates, manifest/roadmap sync |
| Orange | Bounded runtime or CLI behavior change. | `tul export source`, docs drift checker, check improvements |
| Red | Default behavior, cleanup/archive expansion, cross-repo onboarding, or high-risk automation. | automatic exports, broader archive moves, Stage X target onboarding |

## Serialization rules

Serialize packages when they touch any of the same ownership domains:

| Domain | Examples | Rule |
|---|---|---|
| Coordination files | README, manifest, strategy, roadmap, status, decisions, learning log, planning checklists | One package owns current planning text at a time. |
| Runtime files | `bin/tul`, `lib/tulcore/*.py` | Runtime behavior changes are Orange/Red except version-only metadata. |
| Artifact semantics | artifact-semantics, source-context, post-update review, handoff protocol | Do not split vocabulary and implementation into competing packages. |
| Acceptance gates | stage7 package gates, checklist templates | A package changing a gate must serialize before packages relying on that gate. |
| Cleanup/archive/export behavior | archive, sweep, update pipeline, review/source export | Require explicit risk, rollback, and acceptance gates. |

## Current candidate matrix

| Candidate | Class | State | Apply timing |
|---|---|---|---|
| Stage 7 planning consolidation | Yellow | Closed | Verified at `79d27fb...` |
| Terminology audit | Yellow | Closed | Verified at `7d7b27...` |
| Source export spec and gates | Yellow | Closed | Accepted before source-export implementation |
| Explicit `tul export source` implementation | Orange | Current | Adds manual source export; automatic export remains out of scope |
| Docs drift checker | Orange | Future | After planning docs stabilize |
| Review export automation | Red | Future | Separate decision only |
| Archive policy expansion | Red | Future | Separate dry-run evidence first |
| Stage X target onboarding | Red | Deferred | After self-host loop friction drops |

## Acceptance gate template

The detailed template lives in `docs/checklists/stage7-package-gates.md`. Every Stage 7 package must declare:

```text
Bundle name:
Goal:
Baseline HEAD:
Baseline artifact:
Source context used:
Expected changed files:
Intentionally excluded files:
Parallel class:
Serialize because:
Acceptance criteria:
Rollback expectation:
```

Minimum acceptance commands:

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

## Source-export boundary

`docs/workflows/source-export-spec.md` is the implemented command contract after the Orange source-export package closes. `tul export source` is runnable as a manual command; automatic source export remains Red class and must serialize into a later decision package.

## Stop conditions

Stop and request a new baseline artifact or source context when:

- `tul-vf-latest.md` is missing, stale, or not PASS;
- the source archive does not plausibly correspond to the verified HEAD;
- two candidate packages both claim ownership of current status/roadmap text;
- runtime behavior changes are mixed with a large planning-doc rewrite;
- a future command is presented as runnable before implementation closes;
- acceptance criteria cannot isolate the failure source.
