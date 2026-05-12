# Parallel readiness gate

This guide decides whether tul can start the next bounded bundle, whether multiple proposed bundles can be prepared in parallel, and when work must be serialized.

## Inputs

Use current-turn evidence in this order:

1. `tul-vf-latest.md` for release-gate facts and embedded state/handoff snapshots.
2. `tul state` output for latest package, rollbackable commit, cleanup, and handoff state.
3. Source context such as a GitHub-generated `tul-main.zip`, manually created source zip, fresh clone contents, or future explicit source export for code-level package generation.
4. Repo documents for durable guidance.

Do not use prior chat memory as the source of truth when these inputs disagree.

## Single-bundle readiness

A new bundle can start when all of these are true:

- latest verify artifact says `Release gate: PASS`;
- local HEAD and remote HEAD match;
- fresh clone verification passed;
- working tree is clean;
- `py_compile` passed;
- `git diff --check` passed;
- canonical verify layout is present;
- `tul state` is `handoff-ready` / `published` when state output is relevant;
- the next bundle has a bounded topic and a named exclusion list.

If any release-gate item fails, do not generate another implementation package. Diagnose or rollback first.

## Parallel bundle classes

Use this classification before preparing more than one bundle idea.

| Class | Meaning | Rule |
| --- | --- | --- |
| Green | Disjoint docs-only/spec-only changes | Can be drafted in parallel, then applied one at a time. |
| Yellow | Shared coordination docs but no shared runtime files | Draft in parallel only if one package owns final status/roadmap text. |
| Orange | Any runtime code, check, or export behavior change | Serialize. Do not produce competing packages. |
| Red | verify/update/pipeline/rollback/archive move/push/default export behavior | Serialize and require explicit acceptance criteria and rollback reasoning. |

A bundle is not parallel-safe merely because it is small. It must have compatible touched files and compatible acceptance gates.

## Coordination files

Always treat these as coordination files:

- `README.md`;
- `docs/manifest.md`;
- `docs/strategy.md`;
- `docs/roadmap.md`;
- `docs/status/current.md`;
- `docs/learning-log.md`;
- `docs/decisions.md`;
- `docs/checklists/loop-runtime.md`;
- `docs/checklists/planning-harness.md`.

Docs may overlap only when the first bundle's result is treated as the baseline before producing the second package. The package that changes `docs/status/current.md` owns current status text for that update.

## Runtime file-overlap rules

Always serialize when two candidate bundles touch the same runtime file, especially:

- `lib/tulcore/pipeline.py`;
- `lib/tulcore/verify.py`;
- `lib/tulcore/state.py`;
- `lib/tulcore/package.py`;
- `lib/tulcore/authoring.py`;
- `lib/tulcore/handoff.py`;
- `lib/tulcore/cli.py`;
- `bin/tul`.

A version-only metadata bump may accompany a docs package, but runtime behavior must not change in that package.

## Artifact semantics rules

Serialize when two candidate bundles change the meaning or production of:

- `tul-vf-latest.md`;
- `tul-review-latest.zip`;
- future `tul-source-latest.zip` after implementation;
- state/report/handoff artifact evidence;
- backup or rollback authority.

A GitHub-generated `tul-main.zip` may be manual source context, but do not treat it as backup or as a tul-proven source export.

## Required proposal shape

Before generating a package, state:

```text
Bundle name:
Goal:
Baseline HEAD:
Expected changed files:
Intentionally excluded files:
Acceptance criteria:
Parallel class: Green / Yellow / Orange / Red
Serialize because: ...
Proceed condition: latest verify PASS + source context plausibly matching target HEAD when code generation is needed
```

## Acceptance gates

Every bounded package should keep the normal acceptance gate:

```bash
tul package latest
tul update
# upload /sdcard/termux/import/tul/tul-vf-latest.md
```

Before update, run package inspection/checking when practical:

```bash
tul package inspect <package.zip>
tul package check <package.zip> --target tul
```

Add state or handoff checks only when the bundle changes state, archive, rollback, handoff, or cleanup behavior. Add package-check synthetic tests when the bundle changes package validation. Add a one-time `tul verify fresh` bootstrap note only when the package modifies verify behavior itself.

## Stop rules

Stop and serialize when:

- the latest release gate is not PASS;
- the source context does not plausibly match the verified HEAD;
- two candidate bundles touch the same runtime file;
- two candidate bundles compete over current status/roadmap text;
- one bundle changes verify/update/pipeline behavior;
- one bundle changes actual archive moves, deletion, rollback, or push behavior;
- acceptance criteria for the two bundles cannot be evaluated independently.

## Stage 7 guidance

Stage 7 remains bounded parallel, not unrestricted parallel. The safe rhythm is:

1. close one package with verify/state evidence;
2. declare the new baseline commit;
3. classify the next bundle;
4. generate one package from the current verified runtime baseline plus matching source context;
5. apply with `tul update`;
6. review the new `tul-vf-latest.md`;
7. request `tul state` or `tul handoff` only when the bundle touched those surfaces.

For the first Stage 7 package, a large planning consolidation commit is acceptable because it intentionally owns the coordination docs and excludes runtime behavior changes.
