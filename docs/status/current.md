# current status

Status: Stage 7 is closed. The current verified baseline has the compact command surface, `tul run` as the normal user loop, source/review exports, command-surface smoke checks, active-doc command cleanup, and conservative `clean` / `recover` / `setup` auxiliary defaults in place.

Baseline entering Stage 8:

```text
HEAD: 6d4869a3a7a6d4266a5c8a3f2e5dd9fdebd75b2a
Remote HEAD: 6d4869a3a7a6d4266a5c8a3f2e5dd9fdebd75b2a
Latest package: tul-stage7-closure-checkpoint-bundle-v1
Release gate: PASS
Steps: 33 pass, 0 fail
Fresh clone: PASS
Source bundle: current
Review bundle: current
Docs drift: clean
Warnings: none
```

## Active model

- Canonical user loop: `tul run`.
- Canonical command surface: `show / package / update / verify / export / run / clean / recover / setup`.
- Runtime verification evidence: `tul-vf-latest.md`.
- Source transport artifact: `tul-source-latest.zip`.
- Changed-file review artifact: `tul-review-latest.zip`.
- Recovery authority: Git remote + commit hash + recovery state.

## Stage 7 closed checkpoints

- planning consolidation
- terminology audit
- source spec and gates
- explicit source export implementation
- export integrity hardening
- post-update export automation
- command-surface redesign around `tul run`
- command-surface status sync
- run default finalization
- README package-contract gate fix
- run smoke gate
- command residue cleanup
- clean / recover / setup UX tightening
- Stage 7 closure checkpoint

## Current Stage 8 work

1. Compact active documentation ownership.
2. Keep README, status, manifest, roadmap, commands, and package spec as the active durable docs.
3. Preserve rationale in decisions and lessons in learning-log.
4. Keep runtime-referenced compatibility docs until handoff/verify pointers are narrowed in a later package.
5. Defer Windows environment doc relocation until its ownership is decided.

## Next queue

1. Apply the document-tree compaction package.
2. Run `tul run` or `tul verify fresh` to re-establish the release gate.
3. In a follow-up package, narrow runtime handoff/read-next and required-doc pointers.
4. Remove compatibility docs only after the runtime pointers no longer require them.
