# Learning Log

This log records bottom-up lessons from actual update, verify, package, and handoff work. Not every lesson changes the manifest. Most lessons should first affect the ready queue or strategy.

## Entry format

```text
Date/stage:
Observation:
Impact:
Reflected in:
Follow-up:
```

## Lessons

### Stage 2–3 — Raw view and verification boundaries

Observation: GitHub raw view or previews can make files appear malformed or one-line even when blob view or fresh clone is healthy.

Impact: Do not infer repository corruption from raw-view oddities alone.

Reflected in: README, LLM entrypoint, verify/fresh clone workflow.

Follow-up: Use file/blob view or `tul verify <project> --fresh-clone` for line/syntax confidence.

### Stage 2–3 — Repo-wide download constraints differ from per-file review

Observation: A tool environment may fail to clone/download a full repo while still being able to inspect individual web files.

Impact: Do not conflate full clone limitations with inability to review repo files.

Reflected in: LLM entrypoint and source-separation practice.

Follow-up: Prefer repo-resident entrypoints and fresh clone verification when possible.

### Stage 2.1 — Launcher drift

Observation: The PATH `tul` launcher can drift from repo `bin/tul`.

Impact: Users may run a stale command even after updating the repo.

Reflected in: `tul install`, `tul doctor`, launcher diagnostics.

Follow-up: Native commands should assume `tul doctor` can identify launcher drift.

### Stage 1.5 — No-op updates

Observation: Reapplying an already published package should not be a failure.

Impact: `nothing to commit` should produce a no-op outcome, not a failed state.

Reflected in: no-op state handling and report wording.

Follow-up: State output should remain compact even as no-op states accumulate.

### Stage 3.1 — Latest state is not latest rollbackable state

Observation: `tul import` can create a latest state without a commit.

Impact: `tul rollback` must select the latest rollbackable state, not blindly the latest state.

Reflected in: recovery state selection.

Follow-up: `tul state` should clearly distinguish latest state, latest published state, and latest rollbackable state.

### Stage 0–5 — Package root layout matters

Observation: A zip with `tul-package.yml` nested under an extra directory fails manifest discovery.

Impact: Package authoring must validate archive root layout before distribution.

Reflected in: package check, package zip, authoring helper.

Follow-up: Package check diagnostics should remain explicit.

### Stage 5 — Normal use should avoid long package paths

Observation: Repeated `PKG=/path/to/file.zip` commands preserve too much bridge work.

Impact: Normal use should prefer `tul update tul -l` or later `tul update` once native context is safe.

Reflected in: package discovery polish, roadmap, command docs.

Follow-up: Native project context should safely remove repeated target and `-l` flags.

### Stage 5–6 — Roadmap alone is not enough

Observation: Feature acceleration consumes short-term tasks quickly and creates new lessons that can affect medium-term strategy and long-term vision.

Impact: A static roadmap cannot carry the planning load.

Reflected in: planning harness.

Follow-up: Introduce manifest/strategy/roadmap/status/learning/decisions separation.

## Stage 6 — Verify output should be an artifact

Observation: Fresh-clone verification output is too long to paste repeatedly.

Impact: The user becomes a log transport layer, which works against the human-bridge minimization vision.

Reflected in: `tul verify` should persist markdown/json artifacts under the platform log root. On Termux, the expected path is `/sdcard/termux/import/tul/logs/verify/`.

Follow-up: Prefer uploading `tul-verify-latest.md` over pasting full terminal logs.
