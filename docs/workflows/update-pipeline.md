# update pipeline

`tul update <project>` remains the default full-loop command.

The runtime boundary is now split into policy modules:

1. `precheck.py` resolves whether the repo may be updated.
   - enforce branch guard
   - refuse dirty working tree unless explicit recovery mode is used
   - fetch origin
   - detect ahead/behind/diverged state
   - fast-forward with `pull --ff-only` when safe
2. `package.py` discovers, imports, hashes, and safely extracts the package.
3. `manifest.py` validates `tul-package.yml` target, copy mode, and commit metadata.
4. `apply.py` performs safe copy only and writes `apply.log`.
5. `checks.py` runs repo-configured checks and forbidden-pattern checks.
6. `sweep.py` moves repo-local tul backup directories out of the repo.
7. `publish.py` owns changed-file allowlist checks, explicit staging, commit, push, remote HEAD verification, rollback hint generation, and no-op detection.
8. `state.py` records phase transitions, failures, no-op outcomes, and archive metadata.
9. `report.py` and `handoff.py` render the human/LLM outputs.

Successful update still requires remote HEAD verification when commit/push is enabled.
`--no-commit` and `--no-push` are recovery/debug exceptions, not the default workflow.

If applying a package produces no repository changes, update must not attempt an empty commit. It should record `outcome: noop`, produce a report/handoff, and exit successfully.
