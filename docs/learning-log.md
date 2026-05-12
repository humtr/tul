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

Follow-up: Prefer uploading the current canonical latest artifact `tul-vf-latest.md` over pasting full terminal logs.

## 2026-05-12 — Verify artifact names need mobile-visible uniqueness

Observation: Timestamped verify artifact names such as `tul-verify-fresh-20260512-114123-f9c07f038fcd.md` have a long common prefix. Mobile attachment UIs may hide the timestamp and commit suffix, making repeated uploads hard to distinguish.

Impact: Upload-based review reduces copy/paste, but poor artifact names can reintroduce ambiguity across runs.

Reflected in: `docs/workflows/verify.md`, `docs/status/current.md`, and `lib/tulcore/verify.py`.

Follow-up: Prefer `tul-vf-f-<yymmdd>-<hhmmss>-<head>.md` for timestamped fresh verification artifacts and `tul-vf-latest.md` for stable latest review.

## Stage 6 — native context should be incremental

Observation: no-arg commands reduce bridge work, but mutating commands can target the wrong repo if active project, current directory, and package manifest disagree.

Impact: native context must be introduced in steps: store active project first, then add read-only inference, then guarded mutating inference, then package mismatch guidance.

Reflected in: `docs/roadmap.md`, `docs/status/current.md`, `docs/checklists/loop-runtime.md`.

Follow-up: implement `tul_native_context_v1b` only after `tul use` and `tul current` are verified.

## Stage 6 — read-only native defaults should precede mutating defaults

Observation: No-arg commands reduce bridge work, but mutating commands such as `tul update` need stronger context-conflict and package-target guards than read-only commands.

Impact: Native context is staged: active project storage, read-only inference, mutating inference, then package mismatch guidance.

Reflected in: `docs/roadmap.md`, `docs/commands.md`, and native context v1b.

Follow-up: Implement no-arg `tul update` only with explicit conflict and package selection banners.


## Stage 6 — no-arg mutating commands need visible target inference

Observation: Moving from `tul update tul -l` to `tul update` reduces bridge work, but the command must show which project was inferred and why.

Impact: Native mutating commands require a target inference banner and must refuse execution when active project and current-directory project conflict.

Reflected in: `tul_native_context_v1c`, `docs/commands.md`, `docs/status/current.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: Add package manifest mismatch guidance so that incompatible downloaded zip files produce actionable choices instead of a generic no-match error.

## Stage 6.1d — Package target mismatch guidance

Observation: Native `tul update` is only safe if package discovery explains why a downloaded zip matches or does not match the inferred project.

Impact: Human bridge work shifts from guessing which zip was selected to reading explicit matching/incompatible/invalid package classifications.

Reflected in: `lib/tulcore/package.py`, `lib/tulcore/cli.py`, `docs/commands.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: Add release-gate and compact-state summaries so the normal loop becomes easier to judge at a glance.

## Stage 6.2 — update should produce its own verify artifact

Observation: After `tul update` succeeds, the user still had to run `tul verify fresh` and upload a separate artifact. This preserves bridge work and makes the final commit/push result and verification result feel like two separate rituals.

Impact: The normal update loop should produce the LLM-review artifact itself. The terminal output should show commit, push verification, rollback, then a concise fresh verification gate with the markdown artifact path.

Reflected in: `tul_update_verify_gate_v1`, `lib/tulcore/pipeline.py`, `lib/tulcore/verify.py`, `docs/workflows/update-pipeline.md`.

Follow-up: Keep full verify details in files, keep terminal output compact, and let users upload `tul-vf-latest.md` after a single `tul update`.


### Stage 6.1e — Update-integrated verify bootstrap boundary

Observation: The package that installs update-integrated verify cannot itself benefit from the newly installed update pipeline during the same running process. A manual `tul verify fresh` was needed once after installing the feature and its handoff hotfix.

Impact: Self-modifying update features need an explicit bootstrap note. The next ordinary package is the correct smoke test for the newly installed behavior.

Reflected in: `docs/status/current.md`, `docs/roadmap.md`, and `docs/decisions.md`.

Follow-up: Use `tul_parallel_entry_smoke_v1` as the first normal package after the hotfix. If it updates `tul-vf-latest.md` to the smoke commit automatically, parallel bundles may begin.

### Stage 6.1e — Verify artifact clutter

Observation: Keeping latest artifacts and timestamped artifacts in one directory makes the Termux log folder noisy. Writing both `vf` and `verify` latest aliases also creates duplicate canonical-looking files.

Impact: The artifact system should keep one canonical markdown latest file and one canonical JSON latest file at the log root, while timestamped run files move into date folders.

Reflected in: `docs/status/current.md`, `docs/roadmap.md`, and `docs/decisions.md`.

Follow-up: Implement canonical verify log layout in the first bounded parallel bundle.

### Stage 6.2 smoke — update-integrated verify gate passed

Observation: The normal `tul update` loop can now apply a package, publish the result, run post-update `verify fresh`, write `tul-vf-latest.md/json`, and produce a handoff in one command.

Impact: Stage 6 can move from single smoke packages into bounded parallel bundles, as long as each bundle stays small and independently verifiable.

Reflected in: `docs/status/current.md`, `docs/roadmap.md`, `docs/checklists/loop-runtime.md`.

Follow-up: Keep using `tul package latest` and `tul update` as the default loop; reserve split commands for diagnostics and recovery.

### Stage 6.3 — verify layout should separate latest from historical runs

Observation: Storing latest artifacts and timestamped run artifacts together at the verify log root creates clutter. Writing both `vf` and legacy `verify` latest aliases makes the canonical handoff path ambiguous.

Impact: Latest artifacts should stay stable at the root while timestamped runs move into YYMMDD folders. Legacy latest aliases should stop being generated and should not appear in artifact metadata.

Reflected in: `lib/tulcore/verify.py`, `docs/workflows/verify.md`, `docs/decisions.md`.

Follow-up: After applying a package that modifies `verify.py`, run `tul verify fresh` once if the immediate post-update artifact still reflects the old bootstrap code.

### Stage 6.3 — default state output should be a decision view

Observation: Full state dumps are useful for diagnosis but too long for routine post-update decisions, especially when no-op or imported states accumulate.

Impact: Default `tul state` should show latest state, latest rollbackable commit, artifacts, and cleanup guidance. Full history remains available behind `--all` and JSON remains available behind `--json`.

Reflected in: `lib/tulcore/state.py`, `lib/tulcore/cli.py`, `docs/checklists/loop-runtime.md`.

Follow-up: Continue improving archive recommendations after observing actual no-op/imported-state clutter.

### Stage 6.4 — Package diagnostics should fail before update

Observation: Once the update/verify/state loop is compact, the next bridge bottleneck is package authoring failure interpretation. A bad package should fail at `tul package check` with a clear distinction between root layout errors, manifest target mismatches, missing payload files, and `commit.files` drift.

Impact: Users and LLM sessions should spend less time guessing whether an archive was nested incorrectly, targeted the wrong repo, or listed the wrong file set.

Reflected in: `lib/tulcore/authoring.py`, `lib/tulcore/package.py`, `docs/workflows/package-authoring.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: Use synthetic broken packages when package-check behavior changes. Keep cleanup and Windows parity as separate bundles.

### Stage 6.5 — State cleanup should be dry-run first

Observation: Compact `tul state` made work-state accumulation visible, but the previous cleanup suggestion pointed directly at an archive move command. Because state directories are rollback and diagnosis evidence, cleanup needs an inspectable plan before any move.

Impact: Archive cleanup should start with `tul archive --noop --dry-run --keep N`, showing inventory counts, selected source directories, archive destinations, and protected reference states. Actual moves remain explicit and separate.

Reflected in: `lib/tulcore/state.py`, `lib/tulcore/cli.py`, `docs/workflows/state-cleanup.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: After observing dry-run output over repeated bundles, decide whether imported/failed cleanup guidance needs a separate bundle. Keep actual deletion and archive pruning out of this dry-run bundle.

### Stage 6.6 — Handoff discoverability is a runtime/document boundary problem

Observation: Once update, verify, state, package diagnostics, and archive dry-run were stable, the remaining bridge friction was not another runtime mutation. The fresh LLM session needed a clearer path for deciding whether `tul-vf-latest.md`, `tul state`, or a repo zip was required.

Impact: Repo-resident docs should make the evidence economy explicit. A successful update review usually needs only the latest verify artifact. State-sensitive bundles need pasted `tul state` output. New package generation or code-level diagnosis needs the current repo zip.

Reflected in: `docs/llm/post-update-review.md`, `docs/llm/entrypoint.md`, `docs/handoff.md`, `docs/protocols/llm-handoff-protocol.md`, and `lib/tulcore/handoff.py`.

Follow-up: If fresh LLM sessions still miss bundle boundaries, add a parallel-readiness gate document rather than expanding terminal handoff output.

### Stage 6.7 — Parallel work still needs a gate

Observation: After several bounded bundles passed, it became tempting to treat Stage 6 as generally parallel. But repeated packages still update coordination files such as status, roadmap, learning log, decisions, checklist, and sometimes shared runtime files.

Impact: Parallel planning is useful, but package generation must classify file overlap and serialize work when runtime files or acceptance gates conflict.

Reflected in: `docs/workflows/parallel-readiness.md`, `docs/llm/post-update-review.md`, `docs/checklists/loop-runtime.md`, and `lib/tulcore/handoff.py`.

Follow-up: Use the Green/Yellow/Orange/Red classification before producing the next package. Keep Windows parity and state cleanup policy expansion separate unless the readiness gate says their touched files and gates are independent.


### Stage 6.8 — Latest artifact should be the upload bundle

Observation: Keeping `tul-main.zip` at the tul import root while `tul-vf-latest.md` lived under `logs/verify/` forced repeated directory switching during uploads. Requiring separate pasted `tul state` and `tul handoff` output added more bridge work.

Impact: Stable latest artifacts should live beside `tul-main.zip`, while timestamped run artifacts remain under `logs/verify/YYMMDD/`. The latest markdown should include compact state and handoff snapshots so normal post-update review uses one uploaded markdown file.

Reflected in: `lib/tulcore/verify.py`, `lib/tulcore/pipeline.py`, `docs/workflows/verify.md`, `docs/llm/post-update-review.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: After applying this bundle, verify that `/sdcard/termux/import/tul/tul-vf-latest.md` exists, contains `## Runtime snapshots`, and that `tul state` points to the import-root latest file.


## 2026-05-12 — State verify path alignment

Observation: Bundle G correctly moved the stable latest verify artifacts to the tul import root and embedded runtime snapshots, but the handoff-ready state created during the bootstrap update could still contain the former `logs/verify/tul-vf-latest.md` pointer.

Decision: Treat compact `tul state` as a decision view. When the stored path is recognizably the stale latest pointer under `logs/verify/`, display the canonical import-root latest path instead. Do not rewrite or hide timestamped run artifacts.

Follow-up: Consider a separate export bundle that writes `/sdcard/termux/import/tul/tul-main.zip` after successful updates when the next step requires a repo zip.


## Repo zip export after update

Observation: After latest verify moved to the import root and began carrying state/handoff snapshots, the remaining repetitive bridge step was manually creating `tul-main.zip` before the next package-generation turn. The user still had to run a separate zip command even though tul already knew when an update had succeeded.

Impact: A successful full update is the right moment to refresh a stable repo zip pointer. This makes the next handoff pair predictable: `tul-vf-latest.md` for runtime facts and `tul-main.zip` for code/package generation. The export should stay outside release-gate semantics: if export fails after commit/push/verify passed, record the export failure rather than changing the release result.

## 2026-05-12 — Repo zip export needs bootstrap-aware timing

Observation: The Bundle I commit verified successfully and installed `repozip.py`, but `tul-main.zip` was not written during that same update because the update process was still running the previous pipeline implementation.

Impact: Runtime changes that add post-update side effects must be checked for bootstrap behavior. A follow-up update can use the newly installed pipeline, but report, handoff, state, and verify snapshots should record export status in a single coherent order.

Action: Move repo zip export before report/handoff generation and final state snapshot rewrite. Treat export failure as visible runtime metadata, not as a release-gate failure after verify has passed.


## 2026-05-12 — Repo zip export exposed artifact-role mixing

Observation: A stable `tul-main.zip` path reduced upload friction in theory, but it blurred the difference between verify evidence, review handoff, source transfer, and backup. A path in state is not enough to prove that a zip was freshly generated, has no wrapper directory, or matches the verified HEAD.

Lesson: Do not fix artifact confusion by adding more checks around the wrong abstraction. First name the artifact roles, then implement small commands around those roles.

Action: Freeze an artifact semantics checkpoint. Treat `tul-vf-latest.md` as release-gate evidence, design a future `tul-review-latest.zip` for compact diff-oriented upload, and make full source export explicit rather than automatic backup-like behavior.


## 2026-05-12 — Remove misleading source zip state

Observation: Showing `repo zip: /sdcard/termux/import/tul/tul-main.zip` in compact state made a transitional path look like a proven source artifact. This repeated the original artifact-role mixing problem instead of resolving it.

Lesson: Runtime state should display facts with clear evidence boundaries. If an export is not a closed capability, compact state should suppress the path or mark it unresolved rather than treating it as an artifact.

Action: Remove hidden source zip export from the default update pipeline and suppress legacy `repo_zip_export` paths in state/report/handoff surfaces. Keep review/source export as future explicit commands.


## Stage 6 — explicit review export should precede automatic export

Observation: Hidden source zip export blurred review transport, source context, and backup semantics. The safer next step is an explicit `tul export review` command that creates a small diff-oriented bundle before any automatic post-update export is reconsidered.

Impact: Review bundle export is separated from verify and from the default update loop. The command writes `tul-review-latest.zip` as a transport artifact, not a backup.

Follow-up: Verify the explicit command, then decide whether successful `tul update` should call review export automatically.
