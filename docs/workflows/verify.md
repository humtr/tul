# tul verify workflow

`tul verify` is a development-acceleration command. It reduces the repeated manual checks used during tul self-hosting.

Default local verification:

```bash
tul verify tul
```

Fresh-clone verification:

```bash
tul verify tul --fresh-clone
```

The command checks:

- repo exists
- branch detection
- `git fetch origin <branch>`
- local HEAD and `origin/<branch>`
- working tree clean
- `python -m py_compile bin/tul`
- `python -m py_compile lib/tulcore/*.py`
- `git diff --check`
- required LLM entrypoint/status/roadmap/checklist/protocol documents
- README entrypoint terms

Fresh clones are created under:

```text
~/tmp/tul-verify-fresh/<project>-<timestamp>
```

This command does not replace `tul update`. It verifies the repo after update or before generating the next package.
