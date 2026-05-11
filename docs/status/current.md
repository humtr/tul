# Current status

Last verified stage: **Stage 1.5 — no-op/state cleanup**

Latest user-verified fresh clone state:

```text
42c77b0 Handle no-op updates and archive state
86fa990 Restructure tul update runtime boundaries
d79f288 Hotfix tul runtime syntax and newlines
c809069 Introduce tul loop runtime core
9fb3e05 Add branch guard to tul CLI
```

Fresh clone checks passed:

```text
python -m py_compile bin/tul
python -m py_compile lib/tulcore/*.py
```

Current next stage: **Stage 2 — LLM loop contract / repo-resident guidance**

## Known state

- `tul update` is the default full-loop command.
- `precheck.py`, `publish.py`, and `state.py` exist.
- Repeated/already-applied packages should exit as `noop` instead of attempting an empty commit.
- `archive` can archive the latest local tul work state.

## Known remaining debt

- Default handoff should be compact and point to repo docs.
- Full protocol should be available via `tul handoff --full`.
- Copy-ready project instructions should be available via `tul instructions`.
- Directory copy safety still needs an apply safety audit.
- `tul init` should eventually generate/repair global config and aliases.
