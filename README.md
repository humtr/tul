# tul

`tul` means **Terminal Update Loop**.

`tul` is a local, human-controlled automation toolkit for safely moving AI-generated work across this loop:

```text
LLM / assistant
→ user
→ terminal environment
→ local repo / runtime
→ report back to LLM / assistant
```

The LLM side may be ChatGPT, Codex, Gemini, or another assistant.
The terminal side may be Windows, Termux, WSL, or another local shell environment.

The project started from a Termux workflow, but its scope is broader:

- **Windows `D:\work` track**: Windows Terminal + Codex/Gemini + GitHub + local runtime management.
- **Android / Termux track**: mobile ChatGPT handoff + Termux import/update loop.
- **Shared core**: import, verify, report, clean, queue state, safe apply, safe deploy, and safe commit assistance.

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

## Windows intake convention

On Windows, downloaded AI artifacts normally enter through:

```text
D:\work\files\downloads
```

`tul` should stage package-local work under:

```text
D:\work\files\downloads\.tul\work
```

`D:\work\var\tmp` remains available for large scratch work, but it is not the ordinary download handoff path.

## Safety defaults

`tul` should reduce repetitive work, not remove human control.

```text
Automate repetition.
Ask before risky execution.
Never delete when moving is safer.
Never commit or push by default.
Keep every update resumable and reportable.
```

## First-class loop

`tul` treats the human as the explicit approval and execution boundary.

```text
LLM proposes
→ user reviews/chooses
→ terminal applies/verifies
→ tul reports
→ LLM reviews next step
```

This keeps the loop flexible across Windows and Termux without relying on ChatGPT web crawling or browser automation.
