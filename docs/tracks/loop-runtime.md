# loop-runtime track

Current track goal:

Implement a config-driven, manifest-driven, cross-platform self-hosting loop runtime where `tul update <project>` applies a standardized package, checks, sweeps, commits, pushes, verifies remote HEAD, prints rollback instructions, and outputs an LLM-ready handoff automatically.

Current hotfix priority:

- restore valid newlines and Python syntax
- make `python -m py_compile bin/tul` pass
- make `python -m py_compile lib/tulcore/*.py` pass
- make `tul status`, `tul check`, and `tul handoff` smoke tests possible
