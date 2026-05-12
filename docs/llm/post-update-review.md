# LLM post-update review guide

This guide is for a fresh LLM session receiving a `tul` handoff, a `tul-vf-latest.md` artifact, a `tul state` output, or a repo zip after a package has been applied.

## Source hierarchy

Use this order when facts differ:

1. User-provided terminal artifacts from the current turn, especially `/sdcard/termux/import/tul/logs/verify/tul-vf-latest.md`.
2. User-provided `tul state` output.
3. The current repo zip or fresh clone contents.
4. Durable repo documents such as `docs/status/current.md`, `docs/roadmap.md`, and `docs/checklists/loop-runtime.md`.
5. Prior chat summaries, only as context.

Do not treat prior chat claims as repository truth when the artifact or repo contradicts them.

## Fast review path

For a normal successful package application, the user should only need to upload:

```text
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.md
```

A review can usually be closed if the artifact shows:

- `Release gate: PASS`;
- local HEAD and remote HEAD match;
- fresh clone verification passed;
- working tree is clean;
- `py_compile` passed;
- `git diff --check` passed;
- verify artifacts use the canonical layout.

Ask for `tul state` output only when the package changed state, handoff, cleanup, rollback, or archive behavior.

Ask for a fresh repo zip only when producing the next package, doing code-level review, or investigating a failure that cannot be resolved from the verify artifact and terminal output.

## Normal next commands

After receiving a generated package saved in the configured inbox roots:

```bash
tul package latest
tul update
```

For evidence upload after update:

```text
/sdcard/termux/import/tul/logs/verify/tul-vf-latest.md
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

Generate only one implementation package from the current repo zip. If two candidate bundles touch the same runtime file or acceptance gate, serialize them.

## Source separation

When summarizing the handoff, separate:

- user-provided terminal facts;
- repo-documented guidance;
- assistant interpretation;
- unresolved or unverified assumptions.
