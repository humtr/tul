# Recommendation

Adopt Option 2 for the production LLM loop contract.

## Why

Option 2 best preserves the separation needed by tul:

- README is a stable first-contact surface.
- Durable documents carry status, roadmap, checklist, command grammar, and project instructions.
- Runtime handoff carries commit hash, push verification, rollback command, state path, and report path.
- The default handoff stays compact.
- Full protocol remains available through `tul handoff --full`.
- Project instructions remain available through `tul instructions` or `tul handoff --instructions`.

## Production package after this experiment

Package name:

```text
tul_llm_loop_contract_v1.zip
```

Production changes:

```text
README.md
docs/llm/entrypoint.md
docs/llm/commands.md
docs/llm/project-instructions.md
docs/status/current.md
docs/roadmap.md
docs/checklists/loop-runtime.md
docs/protocols/command-grammar.md
docs/protocols/llm-handoff-protocol.md
docs/tracks/loop-runtime.md
docs/handoff.md
templates/project-instructions.md
templates/llm-initial-review-prompt.md
templates/llm-post-update-review-prompt.md
lib/tulcore/handoff.py
lib/tulcore/cli.py
```

## Non-goals

Do not implement apply safety changes in the same package.
Do not change push-by-default semantics.
Do not create a handoff-only commit after every update.
