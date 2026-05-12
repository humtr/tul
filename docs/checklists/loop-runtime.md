# Loop runtime checklist

Before accepting a package:

```bash
tul package latest tul
tul package check /sdcard/Download/<package>.zip --target tul
tul update tul -l
tul verify tul
tul verify tul --fresh-clone
# Upload instead of pasting long output:
# /sdcard/termux/import/tul/logs/verify/tul-verify-latest.md
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

## Planning harness checkpoint

- [ ] README links to the planning harness.
- [ ] `docs/manifest.md` exists and states vision/invariants.
- [ ] `docs/strategy.md` exists and defines capability map.
- [ ] `docs/roadmap.md` contains ready queue and bundle candidates.
- [ ] `docs/status/current.md` names current mode and next package.
- [ ] `docs/learning-log.md` records known execution lessons.
- [ ] `docs/decisions.md` records accepted planning decisions.
- [ ] `docs/protocols/planning-loop.md` defines top-down and bottom-up planning.

## Verify artifact checkpoint

- [ ] `tul verify tul` prints artifact paths.
- [ ] `tul verify tul --fresh-clone` writes markdown and JSON artifacts.
- [ ] Termux default artifact path is `/sdcard/termux/import/tul/logs/verify/`.
- [ ] The stable latest file can be uploaded instead of pasting terminal output.
- [ ] `--no-log` remains available for exceptional runs.

## Verify artifact filenames

- [ ] `tul verify tul --fresh-clone` writes a short timestamped markdown file.
- [ ] The short timestamped name exposes project, mode, timestamp, and commit hash near the beginning.
- [ ] `tul-vf-latest.md` is updated for latest-run upload.
- [ ] Legacy `tul-verify-latest.md` is still written during the compatibility window.


## Native context checkpoint

- [ ] `tul use tul` writes an active project context file.
- [ ] `tul current` reports active/default/current-directory context.
- [ ] `tul projects` marks active/default projects.
- [ ] `tul doctor tul` reports runtime context.
- [ ] `tul use tul --default` safely updates global `default_project`.
- [ ] No-arg `tul update` is still unavailable until guarded mutating-command inference is implemented.

## Native context checks

- [x] `tul use <project>` stores an active project.
- [x] `tul current` shows active/default/current-directory context.
- [x] read-only commands can infer the project target when safe.
- [x] `tul verify fresh` is accepted as shorthand for `--fresh-clone`.
- [ ] mutating commands stop on active/cwd context conflict.
- [ ] `tul update` can safely infer project and latest package.
- [ ] package manifest mismatch guidance explains incompatible zip targets.
