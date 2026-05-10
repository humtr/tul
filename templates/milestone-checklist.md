# tul Milestone Checklist

Use this checklist before cutting a milestone.

## v0.1

- [ ] `bin/tul help`
- [ ] `bin/tul status <repo>`
- [ ] `bin/tul verify <repo>`
- [ ] `bin/tul report <repo>`
- [ ] `bin/tul clean <repo>`
- [ ] `bin/tul import latest`
- [ ] `/sdcard/Download` scan is limited and safe
- [ ] `/sdcard/termux/import/tul` queue exists
- [ ] no automatic apply
- [ ] no automatic commit/push

## v0.2

- [ ] `tul update <repo>`
- [ ] `tul resume <repo>`
- [ ] `active.json`
- [ ] manifest package support
- [ ] legacy apply script detection
- [ ] apply confirmation prompt
- [ ] verify after apply
- [ ] report after apply

## v0.3

- [ ] `.tul.yml`
- [ ] custom verify commands
- [ ] forbidden grep rules
- [ ] clean patterns
- [ ] deploy command
- [ ] no project-specific hardcoding

## v0.4

- [ ] `tul remote-check <repo>`
- [ ] `tul commit <repo> --files ... --message ...`
- [ ] explicit file list required
- [ ] verify before commit
- [ ] untracked warnings

## v0.5

- [ ] `tul watch <repo>`
- [ ] `tul paste <repo>`
- [ ] clipboard code block extraction
- [ ] import/download polling
- [ ] no automatic execution from clipboard

## v1.0

- [ ] stable package manifest
- [ ] stable queue/state format
- [ ] rollback hook support
- [ ] multi-project examples
- [ ] assistant-ready reports
- [ ] recovery documentation
