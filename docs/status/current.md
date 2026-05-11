# Current Status

Latest stage in progress: **Stage 5 — tul development acceleration**.

Latest package in this stage: `tul_package_discovery_polish_v1`.

## Current goals

- Keep `tul update <project>` as the default full-loop command.
- Preserve push-by-default semantics.
- Reduce manual verification work with `tul verify`.
- Keep README as the compact LLM entrypoint.
- Keep runtime facts in handoff/report/state output.

## Current verification command

```bash
tul verify tul
```

For fresh clone verification:

```bash
tul verify tul --fresh-clone
```

## Deferred

`humtr/ai` onboarding is Stage X and is intentionally deferred until tul self-hosting is smoother.


## Active Stage 5.2 focus

Package discovery is now the active acceleration surface. The goal is to make `tul update <project> --latest` transparent before it applies anything. Use `tul package latest`, `tul package list`, and `tul update --latest --dry-run` to inspect candidate choice.
