# Loop runtime checklist

Before accepting a package:

```bash
tul package latest
tul package check /sdcard/Download/<package>.zip --target tul
tul update
# If the package modifies verify.py and the immediate post-update artifact still uses the old bootstrap layout:
tul verify fresh
# Upload instead of pasting long output:
# /sdcard/termux/import/tul/logs/verify/tul-vf-latest.md
```

Use explicit targets when context is ambiguous:

```bash
tul update tul -l
tul verify tul --fresh-clone
```

For package authoring:

```bash
tul package scaffold NAME --target tul --message "Commit message"
tul package add NAME --target tul FILE [FILE...]
tul package summary NAME
tul package zip NAME --out /sdcard/Download/NAME.zip --force
tul package check /sdcard/Download/NAME.zip --target tul
```

Invariants:

- `tul update` pushes by default.
- `-l` / `--latest` selects from configured inbox roots only.
- No `git add -A` or `git add .` in the normal path.
- No force push.
- Repo policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- Root verify latest artifacts are `tul-vf-latest.md/json` only.
- Timestamped verify run artifacts live under `logs/verify/<YYMMDD>/` without a `runs/` layer.

## Planning harness checkpoint

- [x] README links to the planning harness or LLM entrypoint documents.
- [x] `docs/manifest.md` exists and states vision/invariants.
- [x] `docs/strategy.md` exists and defines capability map.
- [x] `docs/roadmap.md` contains ready queue and bundle candidates.
- [x] `docs/status/current.md` names current mode and next package.
- [x] `docs/learning-log.md` records known execution lessons.
- [x] `docs/decisions.md` records accepted planning decisions.
- [x] `docs/protocols/planning-loop.md` defines top-down and bottom-up planning.

## Verify artifact checkpoint

- [x] `tul verify tul` prints artifact paths.
- [x] `tul verify tul --fresh-clone` writes markdown and JSON artifacts.
- [x] `tul verify fresh` is accepted as shorthand for fresh-clone verification.
- [x] Termux default artifact path is `/sdcard/termux/import/tul/logs/verify/`.
- [x] The stable latest file can be uploaded instead of pasting terminal output.
- [x] `--no-log` remains available for exceptional runs.

## Verify artifact filenames

- [x] `tul-vf-latest.md` is the canonical latest markdown upload file.
- [x] `tul-vf-latest.json` is the canonical latest machine-readable file.
- [x] Fresh run artifacts use `tul-vf-f-YYMMDD-HHMMSS-<head7>.md/json`.
- [x] Local run artifacts use `tul-vf-l-YYMMDD-HHMMSS-<head7>.md/json`.
- [x] Timestamped run artifacts are stored under `logs/verify/<YYMMDD>/` date folders.
- [x] Legacy `tul-verify-latest.*` aliases are no longer written after the canonical layout implementation.
- [x] Artifact metadata contains no legacy latest paths.

## Native context checkpoint

- [x] `tul use tul` writes an active project context file.
- [x] `tul current` reports active/default/current-directory context.
- [x] `tul projects` marks active/default projects.
- [x] `tul doctor tul` reports runtime context.
- [x] `tul use tul --default` safely updates global `default_project`.
- [x] No-arg `tul update` is available with guarded mutating-command inference.

## Native context checks

- [x] `tul use <project>` stores an active project.
- [x] `tul current` shows active/default/current-directory context.
- [x] Read-only commands can infer the project target when safe.
- [x] `tul verify fresh` is accepted as shorthand for `--fresh-clone`.
- [x] Mutating commands stop on active/cwd context conflict.
- [x] `tul update` can safely infer project and latest package.
- [x] Package manifest mismatch guidance explains incompatible zip targets.

## Package guidance checkpoint

- [x] `tul package latest` displays selected matching package and selection reason.
- [x] Incompatible package targets are shown when present.
- [x] Invalid archives without readable root `tul-package.yml` are ignored with a reason.
- [x] No-match errors provide next command options.

## Update-integrated verify gate

- [x] Update-integrated verify gate is installed.
- [x] Handoff compatibility hotfix is installed.
- [x] A normal docs-only smoke package proves `tul update` can apply, commit, push, run post-update `verify fresh`, write `tul-vf-latest.md`, and generate handoff in one command.
- [x] Normal `tul update` prints update report before verify/handoff.
- [x] Normal `tul update` shows commit, push verification, and rollback before the verify gate.
- [x] Normal `tul update` runs post-update `verify fresh` unless `--no-verify`, `--no-commit`, or `--no-push` applies.
- [x] Report, state, and handoff include verify gate result and artifact paths.
- [x] If the post-update verify gate fails, terminal output is still printed and the command exits non-zero.

## State output checkpoint

- [x] Default `tul state` is compact decision output.
- [x] Default `tul state` shows latest state and latest rollbackable commit separately.
- [x] `tul state --all --limit 5` preserves full state summaries.
- [x] `tul state --json` preserves machine-readable output.
- [x] Compact state output includes cleanup guidance for no-op/imported state clutter.
