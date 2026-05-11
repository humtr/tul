# Option 1 — README only

## LLM entrypoint

If you are an LLM, coding agent, or new session reviewing this repo, this README is the primary source of truth.

Start here and derive the next action from this file alone.

## Project identity

`tul` means Terminal Update Loop. It is a cross-platform loop runtime for moving AI-generated packages through terminal application, validation, commit, push, remote verification, rollback guidance, and LLM handoff.

Core loop:

```text
LLM creates package
→ user downloads package
→ tul update <project>
→ tul applies/checks/sweeps/commits/pushes/verifies
→ tul prints rollback hint and LLM handoff
→ next LLM reviews remote repo and proposes next package
```

## Invariants

- `tul update <project>` is the default full-loop command.
- Push is included by default.
- `--no-push` and `--no-commit` are exceptions.
- Remote HEAD verification is required for successful update.
- Do not use `git add -A` or `git add .`.
- Do not force push.
- Default rollback is `git revert <commit>` followed by `git push origin <branch>`.
- Project-specific policy belongs in `.tul.yml`.
- Environment paths and project aliases belong in global config.
- LLM-generated packages should be cross-platform `tul-package.yml + files/ + README.md` packages.

## Current status

Latest verified stage: Stage 1.5 — no-op/state cleanup.
Latest verified commit at the time of this experiment: `42c77b0 Handle no-op updates and archive state`.

Completed:

- Stage 0 — syntax/runtime recovery.
- Stage 1 — runtime boundary restructure.
- Stage 1.5 — no-op/state cleanup.

Next:

- Stage 2 — LLM loop contract.

## Next implementation target

Implement production README and handoff behavior based on this README-only design.

## Risks

- README can become too large.
- Current status inside README can become stale.
- Runtime facts such as commit hash, push success, and remote verification cannot be known before `tul update` runs.
- New LLMs may treat README text as runtime proof rather than durable guidance.
- Updating README for every status change may create noisy commits.

## Acceptance criteria

A new LLM reading only this README should identify:

- the project purpose;
- the full-loop invariant;
- the current stage;
- the next package boundary;
- the package format;
- the verification commands;
- the rollback policy.
