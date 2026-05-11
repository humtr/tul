# loop-runtime track

This track implements `tul` as a config-driven, manifest-driven, cross-platform self-hosting loop runtime.

Current invariants:

- `tul update <project>` is the full-loop command.
- Commit and push are included by default after validation.
- `--no-commit` and `--no-push` are explicit recovery/debug exceptions.
- Remote HEAD verification is required for successful update when push is enabled.
- Default staging must use `git add -- <explicit files>` only.
- `git add -A`, `git add .`, and force push are forbidden in the normal path.
- Project-specific policy belongs in `.tul.yml`.
- Environment paths belong in global config.
- LLM-to-terminal packages converge on `tul-package.yml` plus `files/`.
- Successful update must write report/state/handoff and print the LLM handoff.

`runtime_restructure_v1` splits precheck, publish, and state responsibilities while preserving update semantics.
