# tul commands for LLM sessions

Use the Stage 7 canonical command surface only:

```text
tul show
tul package
tul update
tul verify
tul export
tul run
tul clean
tul recover
tul setup
```

## Default recommendation

When the user asks how to apply the next package, recommend:

```bash
cd ~/prj/tul

tul run
```

Do not recommend a separate package preflight unless the user asks to inspect candidates first.

## Stepwise fallback

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

Use this only when diagnosing or explaining the loop.

## Artifact review

Ask the user to upload:

```text
/sdcard/termux/import/tul/tul-vf-latest.md
/sdcard/termux/import/tul/tul-source-latest.zip
/sdcard/termux/import/tul/tul-review-latest.zip
```

For a status-only question, `tul-vf-latest.md` is usually enough. For package generation or code-level audit, ask for the source zip too.

## Prohibited old command guidance

Do not suggest removed top-level commands such as state, status, handoff, archive, rollback, import, apply, publish, init, install, use, current, projects, or config. Use the canonical namespaces instead.
