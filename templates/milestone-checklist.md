# tul Milestone Checklist

Use this checklist before cutting a milestone.

The checklist is platform-neutral unless a line explicitly says Windows or Termux.

---

## v0.1 — status / verify / report / clean / import

- [ ] `bin/tul help`
- [ ] `bin/tul status <repo>`
- [ ] `bin/tul verify <repo>`
- [ ] `bin/tul report <repo>`
- [ ] `bin/tul clean <repo>`
- [ ] `bin/tul import latest`
- [ ] project id detection works
- [ ] assistant-ready report format exists
- [ ] safe staging area exists
- [ ] no automatic apply
- [ ] no automatic commit/push

Windows-specific:

- [ ] D Work paths are recognized
- [ ] `D:\work\var\tmp` can be used as intake/staging
- [ ] `D:\work\var\cache` is not treated as repo content
- [ ] `D:\work\home` is not mutated during repo work

Termux-specific:

- [ ] `/sdcard/Download` scan is limited and safe
- [ ] `/sdcard/termux/import/tul` queue exists
- [ ] no broad `/sdcard` scan

---

## v0.2 — active update state / confirmed apply

- [ ] `tul update <repo>`
- [ ] `tul resume <repo>`
- [ ] `active.json`
- [ ] manifest package support
- [ ] legacy apply script detection
- [ ] apply confirmation prompt
- [ ] verify after apply
- [ ] report after apply
- [ ] failed update can be resumed or archived

---

## v0.3 — .tul.yml project configuration / deploy hooks

- [ ] `.tul.yml`
- [ ] custom verify commands
- [ ] forbidden grep rules
- [ ] clean patterns
- [ ] deploy command
- [ ] no project-specific hardcoding
- [ ] Windows and Termux paths can be represented without hardcoding one platform

---

## v0.4 — remote-check / safe commit helper

- [ ] `tul remote-check <repo>`
- [ ] `tul commit <repo> --files ... --message ...`
- [ ] explicit file list required
- [ ] verify before commit
- [ ] untracked warnings
- [ ] no `git add -A` by default
- [ ] no automatic push

---

## v0.5 — watch / clipboard handoff

- [ ] `tul watch <inbox>`
- [ ] `tul paste <repo>`
- [ ] clipboard code block extraction
- [ ] import/download polling
- [ ] no automatic execution from clipboard
- [ ] platform-specific clipboard integrations are optional

Windows-specific:

- [ ] clipboard staging works from D Work Terminal where feasible
- [ ] watch mode can monitor an explicit D:\work intake folder

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
- [ ] assistant-ready reports
- [ ] recovery documentation
