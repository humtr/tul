# tul

`tul` means **Terminal Update Loop**.

It is a local, human-controlled automation toolkit for safely moving AI-generated work between ChatGPT/Codex/Gemini, local terminal environments, and GitHub repositories.

The project started from a Termux workflow, but its scope is broader:

- **Windows D:\work track**: Windows Terminal + Codex/Gemini + GitHub + local runtime management.
- **Android / Termux track**: mobile ChatGPT handoff + Termux import/update loop.
- **Shared core**: import, verify, report, clean, queue state, safe apply, safe commit assistance.

## Automation roadmap

See:

- [`docs/automation-roadmap.md`](docs/automation-roadmap.md)
- [`docs/windows-dwork-environment.md`](docs/windows-dwork-environment.md)

Target automation direction:

```text
v0.1: status / verify / report / clean / import
v0.2: active update state / confirmed apply
v0.3: .tul.yml project configuration / deploy hooks
v0.4: remote-check / safe commit helper
v0.5: watch / clipboard handoff
v1.0: stable multi-project update loop
```

## Safety defaults

`tul` should reduce repetitive work, not remove human control.

```text
Automate repetition.
Ask before risky execution.
Never delete when moving is safer.
Never commit or push by default.
Keep every update resumable and reportable.
```
