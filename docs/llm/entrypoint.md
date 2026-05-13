# LLM entrypoint

Start with the runtime evidence, then the durable repo docs.

## Read first

1. `tul-vf-latest.md` uploaded by the user.
2. `README.md`.
3. `docs/status/current.md`.
4. `docs/roadmap.md`.
5. `docs/manifest.md`.
6. `docs/llm/commands.md`.
7. `docs/protocols/command-grammar.md`.

When producing a code package or auditing command behavior, also inspect `tul-source-latest.zip`.

## Runtime facts

Treat `tul-vf-latest.md`, `tul show`, `tul show handoff`, and `tul show exports` snapshots as runtime facts.

Treat repo docs as durable guidance, not proof that a command was actually run.

## Normal user command

For normal operation, recommend:

```bash
tul run
```

Only split the loop when the user asks for inspection or when diagnosing a failure.
