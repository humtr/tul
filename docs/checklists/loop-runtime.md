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

## Launcher sync

- [ ] `tul doctor tul` reports whether PATH `tul` is synced with repo `bin/tul` and exits with status 0.
- [ ] `tul install tul` can resync a stale launcher.
- [ ] Operational commands work from outside the repo directory.

```bash
cd ~
tul status tul
tul update tul --latest
tul state tul
tul handoff tul
```

## Apply safety

- [ ] `apply.py` builds an apply plan before copying files.
- [ ] `apply-plan.json` is written to the package work directory.
- [ ] Directory copy is rejected unless `allow_directory: true` is set on the apply item.
- [ ] Every planned destination is covered by manifest `commit.files`.
- [ ] Duplicate apply destinations are rejected before any copy occurs.
- [ ] Existing path traversal and repo-escape protections remain in place.
- [ ] `tul state <project>` can show `Apply Plan` and `Apply Log` paths after a run.

## Validation commands

```bash
python -m py_compile bin/tul
python -m py_compile lib/tulcore/*.py
python bin/tul --version
tul doctor tul
tul install tul
python bin/tul handoff tul
python bin/tul handoff tul --full
python bin/tul handoff tul --instructions
python bin/tul instructions
python bin/tul update tul --latest --no-commit --no-push
python scripts/evaluate-entrypoint-strategy.py
git diff --check
```


## Doctor/no-op output

```bash
cd ~
tul doctor tul
echo $?
tul update tul --latest
tul state tul
```

Expected:

- `tul doctor tul` has no shell-level `Aborted` message.
- exit code is `0`.
- no-op handoff/report/state say `Push verified: not applicable for no-op`.

## Stage 3 recovery/debug commands

Status: package prepared. Recovery/debug surface includes `tul import`, `tul state --all/--json`, `tul archive --all`, rollback-from-state, and conservative `resume/apply` guidance. Split commands remain recovery/debug tools; default workflow remains `tul update <project>`.


## Recovery state selection update

`tul import <project> --latest` creates a validated/imported state without a commit. That state may become the newest state, but it is not rollbackable. `tul rollback <project>` now skips non-commit states and selects the newest rollbackable state with a commit. `tul state <project>` shows a latest rollbackable state hint when the newest state has no commit.


## Init/config onboarding checklist

```bash
tul init tul
tul projects
tul status tul
tul handoff tul

tul init ~/prj/tul --no-handoff
tul init humtr/tul --no-handoff
```

Expected:

- global config exists and preserves existing keys.
- `projects.tul.path` points to the repo.
- `.tul.yml` exists and has version/name/repo/branch/track/check commands.
- init does not switch branches or perform merge/rebase.
- initial-review handoff points the next LLM to README and docs/llm/entrypoint.md.

## Verification acceleration checklist

Use this instead of manual repeated command blocks:

```bash
tul verify tul
```

For fresh clone verification:

```bash
tul verify tul --fresh-clone
```

Expected result:

- Result: pass
- local HEAD matches remote HEAD
- working tree clean
- `py_compile` passes for `bin/tul` and `lib/tulcore/*.py`
- `git diff --check` passes
- README and LLM entrypoint/status/roadmap/checklist/protocol docs exist


## Package discovery polish

Before using `--latest`, verify candidate selection when needed:

```bash
tul package list tul
tul package latest tul
tul update tul --latest --dry-run
```

Acceptance checks:

- `package latest` shows the selected package and selection reason.
- `package list` reports duplicate package names when present.
- `update --latest --dry-run` creates an apply plan without modifying repo files.
- Work/archive roots are not used as latest-package sources.
