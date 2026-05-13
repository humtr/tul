# tul LLM handoff prompt

Use the uploaded `tul-vf-latest.md` as runtime evidence. If code changes are needed, also use `tul-source-latest.zip`. If changed-file context is needed, use `tul-review-latest.zip`.

Treat `tul show`, `tul show handoff`, and `tul show exports` snapshots as runtime facts.

Normal user command for applying the next package is:

```bash
tul run
```

When producing a package, provide one cross-platform zip with `tul-package.yml`, `README.md`, `files/`, `apply.sh`, and `apply.ps1`.
