# Parallel readiness gate

This guide decides whether tul can start the next bounded bundle, whether multiple proposed bundles can be prepared in parallel, and when work must be serialized.

## Inputs

Use current-turn evidence in this order:

1. `tul-vf-latest.md` for release-gate facts and embedded state/handoff snapshots.
2. `tul state` output for latest package, rollbackable commit, cleanup, and handoff state.
3. Current repo zip or fresh clone contents for code-level package generation.
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
| Green | Disjoint docs-only changes | Can be drafted in parallel, then applied one at a time. |
| Yellow | Shared docs but no shared runtime files | Draft in parallel only if one bundle owns final status/roadmap text. |
| Orange | Any shared runtime file | Serialize. Do not produce competing packages. |
| Red | verify/update/pipeline/rollback/archive move behavior | Serialize and require explicit acceptance criteria. |

A bundle is not parallel-safe merely because it is small. It must have compatible touched files and compatible acceptance gates.

## File-overlap rules

Always serialize when two candidate bundles touch the same runtime file, especially:

- `lib/tulcore/pipeline.py`;
- `lib/tulcore/verify.py`;
- `lib/tulcore/state.py`;
- `lib/tulcore/package.py`;
- `lib/tulcore/authoring.py`;
- `lib/tulcore/handoff.py`;
- `lib/tulcore/cli.py`;
- `bin/tul`.

Docs may overlap only when the first bundle's result is treated as the baseline before producing the second package. `docs/status/current.md`, `docs/roadmap.md`, `docs/learning-log.md`, `docs/decisions.md`, and `docs/checklists/loop-runtime.md` are coordination files; they should usually be updated by the package actually being generated, not by multiple pending bundles.

## Required proposal shape

Before generating a package, state:

```text
Bundle name:
Goal:
Expected changed files:
Intentionally excluded files:
Acceptance criteria:
Parallel class: Green / Yellow / Orange / Red
Serialize because: ...
Proceed condition: latest verify PASS + current repo zip at target HEAD
```

## Acceptance gates

Every bounded package should keep the normal acceptance gate:

```bash
tul package latest
tul update
# upload /sdcard/termux/import/tul/tul-vf-latest.md
```

Add state or handoff checks only when the bundle changes state, archive, rollback, handoff, or cleanup behavior. Add package-check synthetic tests when the bundle changes package validation. Add a one-time `tul verify fresh` bootstrap note only when the package modifies verify behavior itself.

## Stop rules

Stop and serialize when:

- the latest release gate is not PASS;
- the uploaded repo zip does not match the verified HEAD;
- two candidate bundles touch the same runtime file;
- one bundle changes verify/update/pipeline behavior;
- one bundle changes actual archive moves, deletion, rollback, or push behavior;
- acceptance criteria for the two bundles cannot be evaluated independently.

## Current Stage 6 guidance

Stage 6 remains bounded parallel, not unrestricted parallel. The safe rhythm is:

1. close one package with verify/state evidence;
2. declare the new baseline commit;
3. classify the next bundle;
4. generate one package from the current repo zip;
5. apply with `tul update`;
6. review the new `tul-vf-latest.md`;
7. request `tul state` or `tul handoff` only when the bundle touched those surfaces.
