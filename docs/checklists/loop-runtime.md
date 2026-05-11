# Loop runtime checklist

Use this checklist when reviewing a package, handoff, or next-stage proposal.

## Required invariants

- [ ] `tul update <project>` remains the default full-loop command.
- [ ] Push is included by default after successful validation and commit.
- [ ] `--no-push` and `--no-commit` remain exceptions.
- [ ] `git add -A` and `git add .` are not used in the normal path.
- [ ] Force push is not used in the normal path.
- [ ] Remote HEAD verification remains part of successful update when push is enabled.
- [ ] Project-specific policy remains in `.tul.yml`.
- [ ] Environment paths and aliases remain in global config.
- [ ] Packages remain cross-platform `tul-package.yml + files/ + README.md` archives.

## Entrypoint strategy

- [ ] README is a concise LLM entrypoint, not the whole protocol.
- [ ] README links to `docs/llm/entrypoint.md`.
- [ ] README links to `docs/status/current.md`.
- [ ] README links to `docs/roadmap.md`.
- [ ] README links to `docs/checklists/loop-runtime.md`.
- [ ] Runtime facts are kept in handoff output, not hardcoded into README.
- [ ] `tul handoff <project>` is compact by default.
- [ ] `tul handoff <project> --full` includes the full protocol.
- [ ] `tul instructions` prints copy-ready project instructions.

## Package selection

- [ ] `tul update <project> --package PATH` applies an exact package.
- [ ] `tul update <project> --latest` selects the newest matching package from configured inbox roots.
- [ ] `tul update <project> -l` is accepted as shorthand for `--latest`.
- [ ] Latest selection does not scan work/archive roots by default.

## Validation commands

```bash
python -m py_compile bin/tul
python -m py_compile lib/tulcore/*.py
python bin/tul --version
python bin/tul handoff tul
python bin/tul handoff tul --full
python bin/tul handoff tul --instructions
python bin/tul instructions
python bin/tul update tul --latest --no-commit --no-push
python scripts/evaluate-entrypoint-strategy.py
git diff --check
```
