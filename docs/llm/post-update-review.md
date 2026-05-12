# LLM post-update review guide

This guide is for a fresh LLM session receiving `tul-vf-latest.md`, a repo zip, or additional terminal output after a package has been applied. Current latest markdown includes the release gate plus compact `tul state` and `tul handoff` snapshots.

## Source hierarchy

Use this order when facts differ:

1. User-provided terminal artifacts from the current turn, especially `/sdcard/termux/import/tul/tul-vf-latest.md`.
2. Runtime snapshots inside `tul-vf-latest.md`, especially `### tul state` and `### tul handoff`.
3. User-provided standalone `tul state` or `tul handoff` output when newer than the latest artifact.
4. Source context such as a manually provided repo zip or fresh clone contents when code-level work is needed.
5. Durable repo documents such as `docs/status/current.md`, `docs/roadmap.md`, and `docs/checklists/loop-runtime.md`.
6. `docs/workflows/artifact-semantics.md` for the current artifact vocabulary.
7. Prior chat summaries, only as context.

Do not treat prior chat claims as repository truth when the artifact or repo contradicts them.

## Fast review path

For a normal successful package application, the user should only need to upload:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

A review can usually be closed if the artifact shows:

- `Release gate: PASS`;
- local HEAD and remote HEAD match;
- fresh clone verification passed;
- working tree is clean;
- `py_compile` passed;
- `git diff --check` passed;
- verify artifacts use the canonical layout.

Ask for standalone `tul state` or `tul handoff` output only when the latest artifact is missing the runtime snapshots, appears stale, or the user has run newer commands after the artifact was created.

Ask for source context only when producing the next package, doing code-level review, or investigating a failure that cannot be resolved from the verify artifact and terminal output. Do not assume `tul-main.zip` is a verified current source export merely because a path appears in state. Until source/review export is reworked, verify the zip root layout before using it and prefer the latest verified HEAD as the source-of-truth identifier.

## Normal next commands

After receiving a generated package saved in the configured inbox roots:

```bash
tul package latest
tul update
```

For evidence upload after update:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
```

For state-sensitive bundles:

```bash
tul state
```

For cleanup inspection:

```bash
tul archive --noop --dry-run --keep 3
```

## Bundle proposal checklist

Before proposing or generating the next package:

- identify the latest verified HEAD;
- name the current completed bundle;
- state whether the release gate is closed;
- name the next bounded bundle;
- list files likely to change;
- list files intentionally excluded;
- define acceptance criteria;
- preserve package shape: `tul-package.yml + files/ + README.md + apply.sh + apply.ps1`;
- avoid `git add -A`, force push, broad cleanup, and policy hardcoding.

## Next-bundle readiness gate

Before proposing or generating another package, apply `docs/workflows/parallel-readiness.md`. At minimum, state:

- latest verified HEAD;
- whether local and remote HEAD match;
- whether the release gate is closed;
- the completed bundle name;
- the next bundle name and goal;
- expected changed files;
- intentionally excluded files;
- acceptance criteria;
- parallel class: Green, Yellow, Orange, or Red.

Generate only one implementation package from verified source context. If two candidate bundles touch the same runtime file or acceptance gate, serialize them.

## Source separation

When summarizing the handoff, separate:

- user-provided terminal facts;
- repo-documented guidance;
- assistant interpretation;
- unresolved or unverified assumptions.


## Artifact caution

Current Stage 6 export semantics are under correction. Treat artifacts as follows:

- `tul-vf-latest.md`: release-gate and runtime snapshot evidence.
- `tul-review-latest.zip`: explicit compact review/diff bundle created by `tul export review`.
- `tul-source-latest.zip` or equivalent source export: planned future explicit source context, not backup.
- `tul-main.zip`: historical/transitional name; do not treat it as automatically trusted evidence unless current runtime output includes freshness and root-layout evidence.

A valid source bundle must have repo files at zip root, such as `README.md`, `.tul.yml`, `bin/tul`, and `lib/tulcore/__init__.py`. A wrapper such as `tul-main/README.md` is not the canonical source shape.


## Optional review bundle

When the receiving LLM needs changed-file evidence beyond `tul-vf-latest.md`, run:

```bash
tul export review
```

Then upload:

```text
/sdcard/termux/import/tul/tul-review-latest.zip
```

The review bundle is a transport artifact, not a backup and not a full source archive. After export, `tul-vf-latest.md` should be refreshed so the runtime snapshot shows the review bundle path and evidence.

## Stage 6 checkpoint review

When reviewing a K3 or Stage 6 exit package, confirm that `docs/workflows/stage6-stabilization-checkpoint.md` agrees with the latest runtime facts and that no zip artifact is treated as backup evidence.
