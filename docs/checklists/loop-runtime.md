# Loop runtime checklist

## Invariants

- [ ] `tul update <project>` remains the default full-loop command.
- [ ] Push is included by default after a successful commit.
- [ ] `--no-push` and `--no-commit` are exceptions.
- [ ] Remote HEAD verification is performed after push.
- [ ] No `git add -A` or `git add .` in the normal path.
- [ ] No force push in the normal path.
- [ ] Project-specific policy remains in `.tul.yml`.
- [ ] Environment paths and aliases remain in global config.
- [ ] Successful update writes report/state/handoff and prints compact handoff.

## Stage 2 acceptance

- [ ] `python -m py_compile bin/tul`
- [ ] `python -m py_compile lib/tulcore/*.py`
- [ ] `python bin/tul handoff tul` prints compact handoff.
- [ ] `python bin/tul handoff tul --full` prints full loop contract.
- [ ] `python bin/tul handoff tul --instructions` prints project instructions.
- [ ] `python bin/tul instructions` prints project instructions.
- [ ] `docs/llm/entrypoint.md` exists.
- [ ] `docs/llm/commands.md` exists.
- [ ] `docs/status/current.md` exists.
- [ ] `docs/roadmap.md` exists.
- [ ] `docs/checklists/loop-runtime.md` exists.
- [ ] `git diff --check` passes.
