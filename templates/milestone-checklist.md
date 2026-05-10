# tul Milestone Checklist

Use this checklist before cutting a milestone.

The checklist is platform-neutral unless a line explicitly says Windows or Termux.

---

## v0.1 — status / sync / check / report / import

- [ ] `bin/tul help`
- [ ] `bin/tul status <repo>`
- [ ] `bin/tul sync <repo>`
- [ ] `bin/tul check <repo>`
- [ ] `bin/tul report <repo>`
- [ ] `bin/tul import latest`
- [ ] project id detection works
- [ ] assistant-ready report format exists
- [ ] safe staging area exists
- [ ] no automatic apply yet
- [ ] no `git add -A`

Windows-specific:

- [ ] D Work paths are recognized
- [ ] `D:\work\files\downloads` is recognized as the ordinary download intake folder
- [ ] `D:\work\files\downloads\.tul\work` can be used as package-local staging
- [ ] `D:\work\var\tmp` remains available for large scratch or non-download temp work
- [ ] `D:\work\var\cache` is not treated as repo content
- [ ] `D:\work\home` is not mutated during repo work

Termux-specific:

- [ ] `/sdcard/Download` scan is limited and safe
- [ ] `/sdcard/termux/import/tul/work` queue exists
- [ ] no broad `/sdcard` scan

---

## v0.2 — update full-loop skeleton

- [ ] `tul update <repo>`
- [ ] update imports latest package
- [ ] update detects target package
- [ ] update applies with confirmation when needed
- [ ] update runs check after apply
- [ ] update runs sweep
- [ ] update runs report
- [ ] update stops before commit if commit files/message are missing
- [ ] split commands are available for debugging

---

## v0.3 — update commit path

- [ ] `tul update <repo> --files ... --message ...`
- [ ] package manifest can provide commit files/message
- [ ] explicit file list required when manifest is absent
- [ ] no `git add -A`
- [ ] staged diff check
- [ ] staged file allowlist check
- [ ] commit hash is recorded
- [ ] rollback hint is prepared

---

## v0.4 — update push/remote verification

- [ ] `tul update <repo>` pushes by default after successful commit
- [ ] `--no-push` exists for debugging/manual intervention
- [ ] update fetches after push
- [ ] update verifies local HEAD == origin/<branch>
- [ ] update prints `git revert <commit>` rollback instructions
- [ ] update does not force-push
- [ ] another platform can run `tul sync <repo>` and continue

---

## v0.5 — split commands and recovery

- [ ] `tul import [latest|path]`
- [ ] `tul apply <repo>`
- [ ] `tul check <repo>`
- [ ] `tul sweep <repo>`
- [ ] `tul publish <repo>`
- [ ] `tul rollback <repo>`
- [ ] `publish` replaces the vague `finish` concept
- [ ] `sweep` moves artifacts instead of deleting them
- [ ] rollback uses revert + push by default

Windows-specific:

- [ ] clipboard staging works from D Work Terminal where feasible
- [ ] watch mode can monitor `D:\work\files\downloads` and stage packages under `.tul\work`

Termux-specific:

- [ ] `termux-clipboard-get` integration is optional
- [ ] `termux-clipboard-set` can receive reports where available

---

## v1.0 — stable multi-project update loop

- [ ] stable package manifest
- [ ] stable queue/state format
- [ ] rollback hook support
- [ ] multi-project examples
- [ ] Windows D Work example
- [ ] Android Termux example
- [ ] `humtr/ai` regression example
- [ ] assistant-ready reports
- [ ] recovery documentation
