# tul Roadmap

Current verified stage: **Stage 5.1 — verify/fresh-clone acceleration**.

## Completed

- Stage 0 — Syntax/runtime recovery
- Stage 1 — Runtime boundary restructure
- Stage 1.5 — No-op/state cleanup
- Stage 2 — LLM loop contract and compact README entrypoint
- Stage 2.1 — Launcher/install sync
- Stage 2.1.1 — Doctor/no-op output polish
- Stage 2.5 — Apply safety audit
- Stage 3 — Recovery/debug commands
- Stage 3.1 — Recovery state selection
- Stage 4 — Init/config onboarding

## Stage 5 — tul development acceleration

Goal: reduce manual bridge work during tul self-hosting before onboarding other target repos.

### Stage 5.1 — Verify/fresh-clone acceleration

Add:

```bash
tul verify tul
tul verify tul --fresh-clone
```

This replaces repeated manual command blocks for fetch, HEAD comparison, `py_compile`, `git diff --check`, and required document checks.

### Stage 5.2 — Package discovery polish

Improve `--latest` visibility:

- show selected package and candidate reason
- warn about duplicate package names
- avoid stale work/archive packages
- keep inbox roots as the source of truth

### Stage 5.3 — State cleanup UX

Improve routine cleanup:

- archive old no-op states
- keep published states by default
- make cleanup non-destructive and reversible

### Stage 5.4 — Package authoring helper

Explore package creation helpers for standardized `tul-package.yml + files/ + README.md` packages.

## Stage X — future target onboarding

`humtr/ai` onboarding is intentionally parked as Stage X. It should happen after tul self-hosting and package/debug UX are smoother.
