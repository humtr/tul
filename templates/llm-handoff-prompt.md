# tul LLM handoff prompt

Use the uploaded `tul-vf-latest.md` as runtime evidence. If code or full file context is needed, also use `tul-source-latest.zip`. If changed-file context is needed and current, use `tul-review-latest.zip`.

Treat `tul show`, `tul show handoff`, and `tul show exports` snapshots as runtime facts.

## Read next

```text
README.md
docs/status/current.md
docs/manifest.md
docs/roadmap.md
docs/commands.md
docs/package-spec.md
```

`docs/decisions.md` and `docs/learning-log.md` are historical support documents, not default read-next documents.

## Ownership boundary

```text
README.md                  entrypoint only
docs/status/current.md      current state only
docs/manifest.md            invariants and ownership map
docs/roadmap.md             future queue only
docs/commands.md            command semantics only
docs/package-spec.md        package contract only
```

## Normal user command

```bash
tul run
```

## Package rule

Produce a package only when the user explicitly asks for one. Use one cross-platform zip with:

```text
tul-package.yml
README.md
files/
```

The package contract is `tul-package.yml + files/ + README.md`.

Do not rely on prior chat context when uploaded artifacts and repo files answer the question.
