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

Follow-up: Use file/blob view or `tul verify fresh` for line/syntax confidence.

### Stage 2–3 — Repo-wide download constraints differ from per-file review

Observation: A tool environment may fail to clone/download a full repo while still being able to inspect individual web files.

Impact: Do not conflate full clone limitations with inability to review repo files.

Reflected in: LLM entrypoint and source-separation practice.

Follow-up: Prefer repo-resident entrypoints and fresh clone verification when possible.

### Stage 2.1 — Launcher drift

Observation: The PATH `tul` launcher can drift from repo `bin/tul`.

Impact: Users may run a stale command even after updating the repo.

Reflected in: `tul setup install`, `tul doctor`, launcher diagnostics.

Follow-up: Native commands should assume `tul doctor` can identify launcher drift.

### Stage 1.5 — No-op updates

Observation: Reapplying an already published package should not be a failure.

Impact: `nothing to commit` should produce a no-op outcome, not a failed state.

Reflected in: no-op state handling and report wording.

Follow-up: State output should remain compact even as no-op states accumulate.

### Stage 3.1 — Latest state is not latest rollbackable state

Observation: `tul update dry` can create a latest state without a commit.

Impact: `tul recover rollback` must select the latest rollbackable state, not blindly the latest state.

Reflected in: recovery state selection.

Follow-up: `tul show` should clearly distinguish latest state, latest published state, and latest rollbackable state.

### Stage 0–5 — Package root layout matters

Observation: A zip with `tul-package.yml` nested under an extra directory fails manifest discovery.

Impact: Package authoring must validate archive root layout before distribution.

Reflected in: package check, package zip, authoring helper.

Follow-up: Package check diagnostics should remain explicit.

### Stage 5 — Normal use should avoid long package paths

Observation: Repeated `PKG=/path/to/file.zip` commands preserve too much bridge work.

Impact: Normal use should prefer `tul update tul -l` or later `tul run` once native context is safe.

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

Follow-up: implement `tul_native_context_v1b` only after `tul setup use` and `tul show config` are verified.

## Stage 6 — read-only native defaults should precede mutating defaults

Observation: No-arg commands reduce bridge work, but mutating commands such as `tul run` need stronger context-conflict and package-target guards than read-only commands.

Impact: Native context is staged: active project storage, read-only inference, mutating inference, then package mismatch guidance.

Reflected in: `docs/roadmap.md`, `docs/commands.md`, and native context v1b.

Follow-up: Implement no-arg `tul run` only with explicit conflict and package selection banners.


## Stage 6 — no-arg mutating commands need visible target inference

Observation: Moving from `tul update tul -l` to `tul run` reduces bridge work, but the command must show which project was inferred and why.

Impact: Native mutating commands require a target inference banner and must refuse execution when active project and current-directory project conflict.

Reflected in: `tul_native_context_v1c`, `docs/commands.md`, `docs/status/current.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: Add package manifest mismatch guidance so that incompatible downloaded zip files produce actionable choices instead of a generic no-match error.

## Stage 6.1d — Package target mismatch guidance

Observation: Native `tul run` is only safe if package discovery explains why a downloaded zip matches or does not match the inferred project.

Impact: Human bridge work shifts from guessing which zip was selected to reading explicit matching/incompatible/invalid package classifications.

Reflected in: `lib/tulcore/package.py`, `lib/tulcore/cli.py`, `docs/commands.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: Add release-gate and compact-state summaries so the normal loop becomes easier to judge at a glance.

## Stage 6.2 — update should produce its own verify artifact

Observation: After `tul run` succeeds, the user still had to run `tul verify fresh` and upload a separate artifact. This preserves bridge work and makes the final commit/push result and verification result feel like two separate rituals.

Impact: The normal update loop should produce the LLM-review artifact itself. The terminal output should show commit, push verification, rollback, then a concise fresh verification gate with the markdown artifact path.

Reflected in: `tul_update_verify_gate_v1`, `lib/tulcore/pipeline.py`, `lib/tulcore/verify.py`, `docs/workflows/update-pipeline.md`.

Follow-up: Keep full verify details in files, keep terminal output compact, and let users upload `tul-vf-latest.md` after a single `tul run`.


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

Observation: The normal `tul run` loop can now apply a package, publish the result, run post-update `verify fresh`, write `tul-vf-latest.md/json`, and produce a handoff in one command.

Impact: Stage 6 can move from single smoke packages into bounded parallel bundles, as long as each bundle stays small and independently verifiable.

Reflected in: `docs/status/current.md`, `docs/roadmap.md`, `docs/checklists/loop-runtime.md`.

Follow-up: Keep using `tul package` and `tul run` as the default loop; reserve split commands for diagnostics and recovery.

### Stage 6.3 — verify layout should separate latest from historical runs

Observation: Storing latest artifacts and timestamped run artifacts together at the verify log root creates clutter. Writing both `vf` and legacy `verify` latest aliases makes the canonical handoff path ambiguous.

Impact: Latest artifacts should stay stable at the root while timestamped runs move into YYMMDD folders. Legacy latest aliases should stop being generated and should not appear in artifact metadata.

Reflected in: `lib/tulcore/verify.py`, `docs/workflows/verify.md`, `docs/decisions.md`.

Follow-up: After applying a package that modifies `verify.py`, run `tul verify fresh` once if the immediate post-update artifact still reflects the old bootstrap code.

### Stage 6.3 — default state output should be a decision view

Observation: Full state dumps are useful for diagnosis but too long for routine post-update decisions, especially when no-op or imported states accumulate.

Impact: Default `tul show` should show latest state, latest rollbackable commit, artifacts, and cleanup guidance. Full history remains available behind `--all` and JSON remains available behind `--json`.

Reflected in: `lib/tulcore/state.py`, `lib/tulcore/cli.py`, `docs/checklists/loop-runtime.md`.

Follow-up: Continue improving archive recommendations after observing actual no-op/imported-state clutter.

### Stage 6.4 — Package diagnostics should fail before update

Observation: Once the update/verify/state loop is compact, the next bridge bottleneck is package authoring failure interpretation. A bad package should fail at `tul package check` with a clear distinction between root layout errors, manifest target mismatches, missing payload files, and `commit.files` drift.

Impact: Users and LLM sessions should spend less time guessing whether an archive was nested incorrectly, targeted the wrong repo, or listed the wrong file set.

Reflected in: `lib/tulcore/authoring.py`, `lib/tulcore/package.py`, `docs/workflows/package-authoring.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: Use synthetic broken packages when package-check behavior changes. Keep cleanup and Windows parity as separate bundles.

### Stage 6.5 — State cleanup should be dry-run first

Observation: Compact `tul show` made work-state accumulation visible, but the previous cleanup suggestion pointed directly at an archive move command. Because state directories are rollback and diagnosis evidence, cleanup needs an inspectable plan before any move.

Impact: Archive cleanup should start with `tul clean states --noop --dry-run --keep N`, showing inventory counts, selected source directories, archive destinations, and protected reference states. Actual moves remain explicit and separate.

Reflected in: `lib/tulcore/state.py`, `lib/tulcore/cli.py`, `docs/workflows/state-cleanup.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: After observing dry-run output over repeated bundles, decide whether imported/failed cleanup guidance needs a separate bundle. Keep actual deletion and archive pruning out of this dry-run bundle.

### Stage 6.6 — Handoff discoverability is a runtime/document boundary problem

Observation: Once update, verify, state, package diagnostics, and archive dry-run were stable, the remaining bridge friction was not another runtime mutation. The fresh LLM session needed a clearer path for deciding whether `tul-vf-latest.md`, `tul show`, or a repo zip was required.

Impact: Repo-resident docs should make the evidence economy explicit. A successful update review usually needs only the latest verify artifact. State-sensitive bundles need pasted `tul show` output. New package generation or code-level diagnosis needs the current repo zip.

Reflected in: `docs/llm/post-update-review.md`, `docs/llm/entrypoint.md`, `docs/handoff.md`, `docs/protocols/llm-handoff-protocol.md`, and `lib/tulcore/handoff.py`.

Follow-up: If fresh LLM sessions still miss bundle boundaries, add a parallel-readiness gate document rather than expanding terminal handoff output.

### Stage 6.7 — Parallel work still needs a gate

Observation: After several bounded bundles passed, it became tempting to treat Stage 6 as generally parallel. But repeated packages still update coordination files such as status, roadmap, learning log, decisions, checklist, and sometimes shared runtime files.

Impact: Parallel planning is useful, but package generation must classify file overlap and serialize work when runtime files or acceptance gates conflict.

Reflected in: `docs/workflows/parallel-readiness.md`, `docs/llm/post-update-review.md`, `docs/checklists/loop-runtime.md`, and `lib/tulcore/handoff.py`.

Follow-up: Use the Green/Yellow/Orange/Red classification before producing the next package. Keep Windows parity and state cleanup policy expansion separate unless the readiness gate says their touched files and gates are independent.


### Stage 6.8 — Latest artifact should be the upload bundle

Observation: Keeping `tul-main.zip` at the tul update dry root while `tul-vf-latest.md` lived under `logs/verify/` forced repeated directory switching during uploads. Requiring separate pasted `tul show` and `tul show handoff` output added more bridge work.

Impact: Stable latest artifacts should live beside `tul-main.zip`, while timestamped run artifacts remain under `logs/verify/YYMMDD/`. The latest markdown should include compact state and handoff snapshots so normal post-update review uses one uploaded markdown file.

Reflected in: `lib/tulcore/verify.py`, `lib/tulcore/pipeline.py`, `docs/workflows/verify.md`, `docs/llm/post-update-review.md`, and `docs/checklists/loop-runtime.md`.

Follow-up: After applying this bundle, verify that `/sdcard/termux/import/tul/tul-vf-latest.md` exists, contains `## Runtime snapshots`, and that `tul show` points to the import-root latest file.


## 2026-05-12 — State verify path alignment

Observation: Bundle G correctly moved the stable latest verify artifacts to the tul update dry root and embedded runtime snapshots, but the handoff-ready state created during the bootstrap update could still contain the former `logs/verify/tul-vf-latest.md` pointer.

Decision: Treat compact `tul show` as a decision view. When the stored path is recognizably the stale latest pointer under `logs/verify/`, display the canonical import-root latest path instead. Do not rewrite or hide timestamped run artifacts.

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

Follow-up: Verify the explicit command, then decide whether successful `tul run` should call review export automatically.

## 2026-05-12 — Review export evidence must refresh runtime facts

Observation: J3 proved the review bundle file can be created, but the uploaded latest verify artifact can remain stale unless the export command refreshes runtime snapshots after recording state.

Action: J4 keeps review export explicit while recording its metadata in state/report/handoff and refreshing `tul-vf-latest.md` runtime snapshots. Automatic update-side export remains deferred.


## 2026-05-13 — Archive execution must be narrower than archive inspection

Observation: The dry-run archive flow made cleanup candidates visible, but actual movement needs a narrower safety contract than inspection. Latest state and latest rollbackable state are runtime evidence, not ordinary clutter.

Lesson: Allow broad selectors for dry-run diagnosis, but keep first actual cleanup bounded to no-op states. Move mode should refuse default/latest, imported, failed, mixed, and broad selections until those policies have their own acceptance gates.

Action: K1 protects latest/latest-rollbackable references in the archive engine, limits actual moves to `--noop`, and records moved-count evidence in the latest remaining state.

## K2 package inbox hygiene lesson

Package discovery warning noise should be reduced by moving stale transport artifacts out of inbox roots rather than broadening selection rules. The safe pattern is dry-run first, quarantine second, never delete by default. Duplicate matching packages are safe to rank by package name and mtime; incompatible packages require a separate policy because they may be valid for other projects.

## 2026-05-13 — Package hygiene external-root correction

A dry-run showed that treating every invalid zip in `/sdcard/Download` as a quarantine candidate is too broad. The policy now treats shared external invalid archives as report-only and moves only valid matching tul packages into the project inbox.

## 2026-05-13 — K track closes the immediate cleanup risk

Observation: After review bundle export stabilized, the main remaining bridge friction was not another export feature but inbox/work-state clutter. Work states were safely reduced by no-op archive moves, and package downloads were moved into the project inbox without touching unrelated Download files.

Lesson: Cleanup features should distinguish ownership boundaries. The tul project inbox is tul-owned; shared Download roots are only scan roots. Move/quarantine policy should be stricter than report policy.

Action: Treat K1 and K2 as the Stage 6 stabilization cleanup baseline, then shift to Stage 7 planning rather than adding more K cleanup features by default.


## 2026-05-13 — Planning consolidation can be large if runtime behavior is excluded

Observation: After Stage 6 stabilization, the risk is not package size alone. The higher risk is mixing planning-doc ownership with runtime implementation behavior in one update. A large planning commit can be safer than several overlapping micro-packages when the same coordination files would otherwise be edited repeatedly.

Lesson: Stage 7 should permit one large Yellow planning consolidation package to align manifest, strategy, roadmap, status, checklists, decisions, learning log, and workflow docs. The package must explicitly exclude runtime behavior changes.

Action: Use `parallel planning, sequential gated update` as the Stage 7 control rule. Plan many candidates, but generate and apply one package per verified baseline.

## 2026-05-13 — Source baseline and runtime baseline are different concepts

Observation: A GitHub-generated `tul-main.zip` can be the best available source context for reading code and writing a package. But `tul-vf-latest.md` is the runtime evidence for HEAD, release gate, working tree, and fresh clone status.

Lesson: Do not collapse source context, review evidence, backup, and runtime truth into one artifact. A manual source archive can be useful without becoming canonical recovery authority.

Action: Keep `tul-main.zip` usable as source context while documenting that backup/recovery authority remains Git remote plus commit hashes and rollback state, and that future `tul export source` needs its own provenance evidence.


## 2026-05-13 — Terminology drift can make future commands look implemented

Observation: After the Stage 7 planning package, `tul export source` was still only a proposed future command, but several planning and workflow documents could be read as if it were already runnable. The user explicitly reported that the argument did not exist.

Lesson: Planning documents may name future commands, but they must label implementation status at the point of use. Source context, source export, review bundle, runtime baseline, and backup authority must remain separate terms.

Action: Add a terminology audit package before source-export implementation. Update docs and help/docstrings so `tul export review` is the only current export command and `tul export source` is a future command that must not be suggested until implemented and verified.


## 2026-05-13 — Green/Yellow before Orange

User direction: resolve Green/Yellow work before implementing runtime behavior.

Lesson: When a future command name is already being discussed, a spec-only package should make the command contract and non-runnable boundary explicit before code is written. This reduces later bridge work and prevents an assistant from suggesting unimplemented commands.

Applied rule: accept source-export spec and package gates before any `tul export source` implementation package.

## 2026-05-13 — Source export implementation boundary

The safe implementation boundary is explicit source export only. The package can include command wiring, artifact verification, state display, and documentation updates, but not automatic post-update source export. This keeps the user bridge reduction incremental and preserves release-gate clarity.

## Stage 7 export integrity lesson

`tul show exports` is the warning-only inspection surface for source/review export freshness and small docs drift checks. It may be run manually or captured in verify snapshots. After the post-update export automation package closes, normal `tul run` should leave source/review artifacts current; stale/missing/invalid artifacts remain warnings, not release-gate failures.


## 2026-05-13 — Post-update exports reduce bridge work only if warning-only

Observation: After `tul show exports` landed, a normal update could legitimately leave source/review artifacts stale. That made the warning surface useful but still required another manual bridge step.

Lesson: Automatic artifact refresh is safe only after the core update has already committed, pushed, and passed fresh verification. Export failures must be recorded but not allowed to rewrite release-gate or rollback semantics.

Action: Add a post-update export phase that refreshes source and review bundles, records outcomes in state/report/handoff, refreshes latest verify runtime snapshots, and keeps failures warning-only.

## 2026-05-13 — Command names must describe user-visible action

Observation: the removed export-status command form violated the command grammar because `export` implies file creation while that form only printed diagnostics.

Lesson: CLI namespaces should be action-oriented and user-visible. Internal concepts such as export integrity, source context, handoff, state, and recovery-debug should not appear as scattered top-level commands.

Applied rule: Use `show` for read-only output, `export` for file creation, `update` for repo publishing, and `run` for the full Terminal Update Loop.


### Stage 7 — Command-surface redesign can bootstrap-fail old gates

Observation: The package that replaces command grammar may be applied by the previous command implementation and previous verify gate. The first post-update verify snapshot can therefore fail against old README entrypoint terms even when the committed code, fresh clone, and later new verifier are healthy.

Impact: For command-surface redesigns, distinguish bootstrap gate drift from runtime failure. The deciding check is a subsequent `tul verify fresh` executed after the new command surface is installed.

Reflected in: `docs/status/current.md`, `docs/roadmap.md`, and `docs/manifest.md`.

Follow-up: Keep command grammar changes and verify-gate term changes in the same package. After applying such a package, run `tul verify fresh` once with the installed command surface before judging the baseline.

## 2026-05-13 — `tul run` should be the single normal loop

Observation: After command-surface redesign, asking users to run `tul package` before every normal application still preserves unnecessary bridge work. `tul package` is useful as optional preflight, but normal operation should be `tul run`.

Decision: `tul run` should handle both cases: if a compatible package exists, run update/export/fresh-verify/show; if no compatible package exists, refresh export/fresh-verify/show for the current HEAD.

Impact: User-facing docs and templates must avoid pre-redesign commands and should present `tul run` as the default command.

## 2026-05-13 — Stage 7 run smoke gate

The README package-contract hotfix closed the narrow release-gate failure after run default finalization. The next stability gap is command-surface drift: the runtime can compile and still accidentally reintroduce old top-level commands or status-only commands under `export`. The gate should smoke-test parser/help behavior that does not require project configuration.


### 2026-05-13 — Command residue cleanup protects the new surface

Observation: After `tul run` became the normal user loop, active docs and templates still needed cleanup so fresh LLM sessions would not reintroduce older command grammar.

Impact: Templates are higher risk than historical docs because they can be copied directly into new sessions or package prompts. Historical docs may keep old command examples if they are clearly marked.

Reflected in: active command docs, LLM handoff templates, milestone checklist, and historical banners on pre-Stage 7 docs.

Follow-up: Add a warning-first release-gate scan that excludes historical documents and checks active docs/templates for removed command forms.


## 2026-05-13 — Auxiliary commands need conservative defaults

Observation: After `tul run` became the normal loop, the remaining user-facing commands are mostly inspection or support surfaces. If `clean`, `recover`, or `setup` mutate by default, they undermine the simplified command model.

Decision: Keep `tul clean`, `tul recover`, and `tul setup` safe to run without arguments. Require explicit subcommands for guarded moves, rollback command printing, or setup changes.

Follow-up: Close Stage 7 after the auxiliary UX package passes fresh verification and source/review artifacts remain current.

## 2026-05-13 — Stage 7 closure checkpoint

Observation: Stage 7 stabilized after the command surface was reduced, `tul run` became the normal user loop, source/review exports became current after normal runs, and command-surface smoke checks entered the release gate.

Lesson: Reducing user bridge work required separating concepts instead of adding more flags: `run` orchestrates the loop, `update` publishes packages, `verify fresh` writes uploadable verification evidence, `export` creates files, and `show` reports state.

Action: Close Stage 7 with a documentation checkpoint and move Stage 8 toward gate hardening, smoke-test harnesses, retired-module review, and eventually guarded cross-repo onboarding.

### 2026-05-14 — Delete only after runtime pointers move

Observation: Stage 8 document compaction cannot safely delete compatibility docs while `tul show handoff` and `tul verify` still point at them.

Impact: Delete-first compaction would convert a documentation cleanup into a release-gate failure.

Reflected in: `tul-doc-tree-compaction-stage2-pointer-compaction-v1` updates `lib/tulcore/handoff.py`, `lib/tulcore/verify.py`, and active docs before any obsolete file deletion.

Follow-up: Run 2B as a separate narrow deletion step after 2A passes fresh verification.

### 2026-05-14 — Review export must be current-HEAD evidence

Observation: After a narrow manual `git rm` cleanup, `tul export review` could write a new review bundle whose manifest still used the latest tul package state commit. `tul show exports` then correctly reported the freshly written review bundle as stale.

Impact: Source export, verify, and Git remote state could all be current while the review bundle remained tied to an older package state. This made artifact review ambiguous after legitimate manual commits.

Reflected in: `tul-stage9a-review-current-head-export-v1` changes review export to use current Git HEAD as review evidence and records the latest state commit only as context.

Follow-up: Later state-model work may distinguish package-run state from manual cleanup commits more explicitly, but review freshness should no longer depend on the latest package state matching HEAD.

## Stage 9C — Split seams only after tests exist

Observation: Large modules are easier to refactor safely once command surface, handoff, verify docs, and export integrity contracts have executable tests.

Impact: Structural changes should first extract seams around existing behavior rather than rewrite command handlers or state rendering wholesale.

Reflected in: `lib/tulcore/cli_parser.py`, `lib/tulcore/verify_checks.py`, export integrity tests, and the small `state.py` project-matching helper.

Follow-up: Use the same acceptance gate before any larger `cli.py`, `verify.py`, or `state.py` decomposition.

## Lesson: one-run loops need executable acceptance, not only syntax checks

The Stage 9C helper regression showed that `py_compile` can pass while `show`, `export`, or `verify` command handlers fail at runtime. Macro Stage A moves CLI runtime smoke and regression tests into the verify gate so `tul run` can serve as the normal one-command loop for applying, exporting, verifying, and saving artifacts.
## Lesson: final-screen evidence matters

Long verify logs are useful as artifacts but poor as terminal decision surfaces. `tul run` should finish with a short PASS/CHECK block and explicit upload paths.

Reference package: `tul-macro-stage-a-run-final-upload-v4`.

## Lesson: upload friction is a state-surface problem

A technically correct release gate is still too hard to use if the user has to search long logs or multiple folders to decide what to upload. Macro Stage A v5 treats the final terminal screen and the import root as explicit human-facing surfaces: the last block says PASS/CHECK, and the import root keeps only the current commit-named upload aliases plus stable latest files.

## 2026-05-14 — Head-tagged upload root beats latest aliases

When the user manually uploads artifacts, `latest` filenames are a liability because repeated uploads can bind to stale files in another session. Commit-tagged filenames are clearer. The import root should therefore be a human upload surface containing only the current head-tagged source, review, and verify markdown files; dated logs remain the archive.

## 2026-05-14 — Head tags are the artifact authority

Observation: Keeping both head-tagged artifacts and latest-named artifacts preserves ambiguity. The user-facing workflow needs one visible truth, not a canonical file plus a fallback pointer.

Lesson: During active development, head-tagged artifacts should be the artifact authority. `latest` names are not needed for manual upload and should not remain as compatibility surface in the import root.

Action: Macro Stage A v7 makes source, review, and verify upload artifacts head-tag canonical and keeps verify JSON in dated logs only.
