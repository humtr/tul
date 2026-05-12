# Decisions

This file records accepted planning and design decisions. It is not a full change log; it explains why durable project rules changed.

## ADR-001 — README is compact entrypoint

Status: accepted

Context: README must be readable by new LLM sessions and users without becoming a complete planning ledger.

Decision: README links to the durable planning harness but does not contain the full manifest, strategy, roadmap, learning log, or decision log.

Consequences: Detailed planning lives in `docs/manifest.md`, `docs/strategy.md`, `docs/roadmap.md`, `docs/status/current.md`, `docs/learning-log.md`, and `docs/decisions.md`.

## ADR-002 — Runtime facts belong in handoff/report/state

Status: accepted

Context: Commit hashes, push verification, state paths, and rollback commands are known at runtime, often after a commit is created.

Decision: Runtime facts are printed by terminal handoff/report/state rather than committed into the same implementation commit.

Consequences: Repo docs carry durable contracts; handoff/report/state carry session facts.

## ADR-003 — `humtr/ai` onboarding is Stage X

Status: accepted

Context: `humtr/ai` is the first operational target, but tul's own loop still benefits from acceleration and hardening.

Decision: `/ai` onboarding is deferred to Stage X until tul's self-host loop reduces rather than multiplies bridge work.

Consequences: Current work focuses on tul self-host acceleration, verification, package discovery, state hygiene, native context, and harness portability.

## ADR-004 — `update -l` is preferred over long package paths for normal use

Status: accepted

Context: Repeated package path variables and long absolute paths keep the user in bridge-work mode.

Decision: Normal package application should use configured inbox roots and `tul update <project> -l`.

Consequences: `--package PATH` remains for exact targeting and recovery, but docs should prefer `-l` until native no-arg update is safe.

## ADR-005 — Planning harness separates manifest, strategy, roadmap, status, learning, and decisions

Status: accepted

Context: Stage 6 accelerates feature work and generates new lessons quickly. A single roadmap cannot safely carry vision, medium-term capability planning, short-term ready queue, current state, and decisions.

Decision: The project uses a repo-resident planning harness:

```text
manifest → strategy → roadmap → status → learning log → decisions
```

Consequences: New packages should update the appropriate planning layer, not blindly edit only `docs/roadmap.md`.

## ADR-006 — Native no-arg commands require context conflict guards

Status: accepted

Context: The desired UX is moving from `tul update tul -l` to `tul update`, but active project and current directory can conflict.

Decision: Native context must infer target only when safe. Mutating commands must stop on conflict and present choices. Read-only commands may warn and prefer current-directory context.

Consequences: Native context is split into steps: context storage, read-only inference, mutating inference, package mismatch guidance.

## ADR-007 — Manifest changes require a higher threshold than roadmap changes

Status: accepted

Context: Execution lessons are frequent. If every lesson changes the manifest, the project loses a stable purpose.

Decision: One-off friction goes to learning log and roadmap. Repeated capability pressure goes to strategy. Human authority, safety, or vision changes may change the manifest and should be recorded here.

Consequences: The manifest remains stable but corrigible.

## ADR-008 — Verification output should be file-backed

Status: accepted

Context: `tul verify --fresh-clone` produces long output that is useful but cumbersome to paste into a chat.

Decision: `tul verify` writes markdown and JSON artifacts by default. The terminal output remains visible, but the stable latest artifact can be uploaded for review.

Consequences: The human bridge shifts from log copying to file handoff. This supports the long-term goal of minimizing repetitive bridge labor while preserving inspectability.

## ADR-009 — Verify artifacts use short upload-friendly names

Status: accepted

Context: Verify artifacts replaced long terminal copy/paste, but long common filename prefixes made repeated uploads hard to distinguish in mobile attachment UIs. Stable `latest` filenames are useful for local automation, while unique timestamped filenames are better for uploaded review evidence.

Decision: Generate short timestamped names using `<project>-vf-<mode>-<yymmdd>-<hhmmss>-<head>`, where `mode` is `f` for fresh-clone verification and `l` for local verification. Also generate stable `tul-vf-latest.*` files. This naming decision is now combined with ADR-013, which removes legacy `tul-verify-latest.*` aliases.

Consequences: The user can upload one short, unique markdown artifact without long terminal paste. Stable review automation should use `tul-vf-latest.md/json`.

## ADR-010 — Native context is staged from read-only to mutating commands

Status: accepted

Context: Repeating project names and long flags preserves bridge work. However, changing commands such as `tul update` can damage the wrong repo if active project, current directory, and package manifest disagree.

Decision: Implement native context in stages. First store active context. Then allow no-arg read-only commands and `tul verify fresh`. Only later allow no-arg mutating commands with conflict guards and package-target mismatch guidance.

Consequences: Users get shorter safe commands early, while update/import/rollback defaults remain guarded until the model is proven.


## ADR-011 — No-arg mutating commands require explicit inference banners

Status: accepted

Context: The project is reducing repeated target and package flags. `tul update` is the desired native command, but silent inference would make it harder to audit which project is being changed.

Decision: No-arg mutating commands may infer the project only when context is unambiguous. They must print a target inference banner and must abort when active project and current-directory project conflict.

Consequences: `tul update`, `tul import`, and `tul rollback` can be short in the common case while preserving inspectability and user authority. Package-target mismatch guidance remains the next safety layer.

## ADR-008 — Package mismatch guidance belongs in discovery, not only update failure

Status: accepted

Context: With native `tul update`, users should not manually infer whether a downloaded package targets the active project.

Decision: Package discovery classifies matching, incompatible, and invalid archives. `tul package latest/list` expose the classification, and update failure messages include concrete next commands.

Consequences: Normal package selection remains safe and manifest-driven while reducing user-side file inspection.

## ADR-012 — Normal update includes a post-update fresh verification artifact

Status: accepted

Context: `tul update` already applies, checks, commits, pushes, verifies remote HEAD, reports rollback, and prints handoff. Requiring a separate `tul verify fresh` command after every successful update keeps the user as a log-transport bridge.

Decision: In the normal full-loop path, `tul update` runs a post-update fresh verification gate after publish/no-op handling. It writes the same markdown/json verify artifacts as `tul verify fresh`, prints a compact PASS/FAIL summary, and records artifact paths in report, state, and handoff. Debug paths such as `--no-commit` or `--no-push` do not run the automatic fresh gate because the remote may intentionally not reflect local changes. `--no-verify` remains available as an exception.

Consequences: The default self-host loop becomes one command shorter. The output order preserves user authority: update report first, commit/push/rollback visibility, fresh verification gate second, LLM handoff last.


## ADR-013 — Canonical verify artifact layout

Status: accepted

Context: Verify artifacts replaced long terminal copy/paste, but the verify log root became cluttered when latest files and timestamped run files lived together. The temporary compatibility aliases also created two apparent naming families: `vf` and `verify`.

Decision: Keep exactly one canonical latest markdown file and one canonical latest JSON file at the verify log root: `<project>-vf-latest.md` and `<project>-vf-latest.json`. Move timestamped run artifacts into date folders directly under the verify log root, for example `logs/verify/260512/<project>-vf-f-260512-152110-9dae1b4.md`. Do not continue generating `tul-verify-latest.*` after the layout implementation.

Consequences: The user can upload the stable latest markdown for normal review, while historical runs remain available without cluttering the root directory. The first implementation must acknowledge that a package modifying verify artifact generation cannot make the running update process use the new layout until the next command.

## ADR-014 — Parallel entry requires a normal update smoke after self-modifying update features

Status: accepted

Context: The update-integrated verify gate modifies the update pipeline itself. Its installation required one manual post-install verification because the old process could not use the new pipeline code while still running.

Decision: Before starting larger parallel bundles, run one docs-only smoke package with normal `tul update`. The smoke passes only if commit, push, post-update fresh verify, latest artifact update, and handoff generation all succeed in one command.

Consequences: Parallel work starts from a proven one-command loop rather than from an assumed loop. The smoke package is intentionally docs-only to isolate runtime behavior from unrelated code changes.

## ADR-015 — Default state output is compact; full history is explicit

Status: accepted

Context: Update state files are essential for rollback, diagnosis, and handoff review, but the default state output became too verbose for the normal self-host loop. No-op and imported states can also be newer than the latest rollbackable commit.

Decision: `tul state` defaults to a compact decision view showing the latest state, latest rollbackable commit, key artifacts, cleanup suggestion, and explicit commands for full history. `tul state --all` preserves the long state summaries, and `tul state --json` preserves machine-readable state output.

Consequences: Routine inspection becomes shorter without losing diagnostic depth. Rollbackability remains visible even when the newest state is a no-op, imported, failed, or otherwise non-rollbackable state.

## ADR-016 — Package check is the pre-update authoring gate

Status: accepted

Context: The self-host loop now has a release gate and compact state output. The next high-friction point is package authoring: nested zip roots, missing payload files, and mismatched `apply.files`/`commit.files` can otherwise surface too late during update.

Decision: Treat `tul package check` as the pre-update authoring gate. It should validate archive root layout, payload hygiene, manifest target compatibility, apply source coverage, unique destinations, and exact alignment between `apply.files[*].to` and `commit.files`. Failure output should include a concise failure summary and actionable next steps.

Consequences: Package authors get faster feedback before mutating a repo. Update remains the runtime execution loop, while package check becomes the safer place to catch authoring mistakes. Broader cleanup automation and Windows parity remain separate bundles.

## ADR-017 — Archive cleanup is dry-run first

Status: accepted

Context: Work state directories accumulate during self-host testing. They are clutter, but they also contain reports, handoffs, state files, and rollback evidence. A compact state view can suggest cleanup, but it should not encourage an unreviewed move as the first action.

Decision: State cleanup guidance starts with `tul archive --noop --dry-run --keep N`. Archive output should show inventory, selected cleanup class, keep count, source and destination directories, and latest/latest-rollbackable reference states. Omitted project targets may use guarded native context, matching other mutating commands. Actual moves require an explicit rerun without `--dry-run`.

Consequences: Users can reduce work-state clutter without losing inspection authority. Cleanup remains reversible in the sense that state directories are moved to the configured archive root rather than deleted. Automatic deletion and archive pruning are deferred.

## ADR-018 — Handoff discoverability uses repo pointers, not larger terminal dumps

Status: accepted

Context: Compact handoff and verify artifacts reduce bridge work, but a fresh LLM session can still ask for too much evidence or start from the wrong document. Expanding terminal handoff into a large prompt would reintroduce clutter and make every update harder to read.

Decision: Keep handoff compact and add a repo-resident post-update review guide. Compact handoff, README, the LLM entrypoint, and the handoff protocol should all point to the same review path. `tul-vf-latest.md` is the normal release-gate evidence; `tul state` is requested only for state-sensitive behavior; a current repo zip is requested when producing the next package or diagnosing code-level failures.

Consequences: Fresh LLM sessions can review successful updates with less user bridge work while still finding the correct repo documents when implementation is needed. Future discoverability improvements should add or refine repo pointers before increasing terminal output size.

## Stage 6.7 — Parallel readiness gate before more bundles

Decision: Before proposing or generating the next implementation package, a fresh session should apply the parallel-readiness gate.

Rationale: Stage 6 allows bounded parallel planning, but repeated packages share coordination docs and sometimes runtime files. Without a gate, two small packages can still conflict or make acceptance evidence ambiguous.

Accepted rule:

- Generate packages from the latest verified HEAD and current repo zip.
- Declare expected changed files, excluded files, acceptance criteria, and a Green/Yellow/Orange/Red class.
- Serialize whenever candidate bundles share runtime files or change verify/update/pipeline/rollback/archive move/push behavior.
- Apply packages one at a time through `tul update` and close each with `tul-vf-latest.md`.

Reflected in: `docs/workflows/parallel-readiness.md`, `docs/llm/post-update-review.md`, `docs/checklists/loop-runtime.md`, and compact handoff read-next pointers.


## ADR-019 — Latest verify artifact is the single upload artifact

Status: accepted

Context: Timestamped verify artifacts already preserve historical runs by date and commit hash. The stable latest artifact is operationally a current pointer for review and upload, not the archival record. Keeping it under `logs/verify/` made the user select files from different directories than `tul-main.zip`, and separate `tul state` / `tul handoff` pastes kept bridge work high.

Decision: Write stable `tul-vf-latest.md/json` directly under the tul import root beside `tul-main.zip`. Keep timestamped run artifacts under `logs/verify/YYMMDD/`. Include compact `tul state` and `tul handoff` snapshots in the latest markdown. During `tul update`, rewrite the verify markdown after final handoff-ready state is recorded so snapshots reflect the just-published package.

Consequences: A normal successful post-update review can use one uploaded markdown file. Historical verify runs remain available by date/hash. Legacy `tul-verify-latest.*` aliases remain forbidden.


## ADR-017 — Compact state normalizes stale latest verify pointers

Status: accepted

Context: The canonical latest verify markdown/json pair now lives under the tul import root. During the bootstrap update that introduced this layout, the handoff-ready state may still record the former `logs/verify/<project>-vf-latest.md` location. That stale pointer is confusing because the latest upload artifact itself is already correct.

Decision: Compact `tul state` should display the current import-root latest verify path when a stored state value is recognizably the stale `logs/verify/<project>-vf-latest.md` pointer. Timestamped run artifacts remain unchanged and are still shown by verify artifact metadata.

Consequences: The user can rely on `tul-vf-latest.md` and `tul-main.zip` living side by side in the import root, while historical run artifacts remain under `logs/verify/YYMMDD/`. This is a display alignment rule, not a history rewrite.


## ADR-020 — Successful updates refresh a stable repo zip

Status: superseded by ADR-022 and ADR-023

Context: The latest verify markdown now lives beside `tul-main.zip` and includes compact state/handoff snapshots. Package generation still needs a current repo zip, and asking the user to manually recreate it after every successful update keeps one avoidable human bridge step in the loop.

Decision: After a successful full `tul update` with commit, push, and fresh verify passing, tul writes a stable repo zip export to `/sdcard/termux/import/tul/tul-main.zip`. The export is a latest pointer, not history. It excludes Git metadata, caches, build outputs, dependency directories, existing zip files, backup files, and transient roots. Export status is recorded in the handoff-ready state.

Consequences: The next package-generation session normally needs only the side-by-side pair `tul-vf-latest.md` and `tul-main.zip`. If repo zip export fails after the release gate passed, the failure is visible in state/runtime snapshots but does not retroactively make the release gate fail.

## ADR-021 — Repo zip export is post-verify metadata, recorded before final handoff

Status: superseded by ADR-022 and ADR-023

Context: Repo zip export is a convenience artifact for the next LLM package-generation turn. It should be refreshed after successful verification, but a failure to write the zip after commit/push/verify should not retroactively change the release gate.

Decision: Run repo zip export after fresh verify passes and before report, handoff, final handoff-ready state, and runtime snapshot rewrite. Record either the export path or the failure reason in state/report/handoff.

Consequences: The next uploaded pair should be `tul-vf-latest.md` and `tul-main.zip`. If zip export fails, the latest verify artifact remains valid for release review while visibly reporting that code-level package generation still requires a manual repo zip.


## ADR-022 — Export artifacts are not backups and source export is unresolved

Status: accepted

Context: Bundle I attempted to reduce user bridge work by writing `/sdcard/termux/import/tul/tul-main.zip` after successful updates. In practice this mixed at least four concepts: release-gate evidence, handoff evidence, review/diff transfer, and full source transfer. It also made a zip path in state look like proof of a fresh source export even when root layout and freshness were not proven.

Decision: Separate artifact roles. `tul-vf-latest.md` is the canonical release-gate and runtime snapshot artifact. Timestamped verify artifacts are run history. Git remote and commit hashes are the backup/recovery authority. Review bundles and source bundles are transport artifacts and must be implemented separately. Automatic `tul-main.zip` export is not a closed capability and should not be treated as canonical backup or proven source evidence.

Consequences: ADR-020 and ADR-021 are superseded for future implementation. The next work should remove misleading source zip state, then implement `tul export review`, then implement explicit `tul export source` with root-layout/freshness evidence. Only after the review/source split is stable should automatic post-update export be reconsidered.


## ADR-023 — Suppress legacy repo zip paths until explicit exports exist

Status: accepted

Context: After ADR-022, compact state could still show `repo zip: /path` from legacy `repo_zip_export` fields. That output made an unresolved source-export path look like a successful artifact.

Decision: Remove hidden repo/source zip export from the default update pipeline. Suppress legacy repo zip paths in compact and detailed state. Report and handoff output should not present `tul-main.zip` as a successful update artifact. Future export work must be role-specific: `tul export review` for compact diff evidence and `tul export source` for explicit full source context.

Consequences: A normal post-update review returns to a single primary artifact: `tul-vf-latest.md`. Code-level package generation may still require manually provided source context until explicit export commands are implemented.

## ADR-024: Explicit review export records evidence but remains outside update

Decision: `tul export review` should remain an explicit command for now, but a successful export must leave visible evidence in state/report/handoff and refresh the latest verify markdown runtime snapshots.

Rationale: J3 proved the transport artifact shape. J4 closes observability without re-coupling export to verify or the default update loop.

Consequences: Automatic post-update review export remains a later decision. Full source export remains a separate explicit command.


## ADR-025 — Archive move mode is noop-only until broader cleanup policies are accepted

Status: accepted

Context: Archive dry-run output can safely inspect no-op, imported, failed, latest, and broad selections. Actual movement is different: state directories are runtime evidence for rollback, debugging, and handoff. The first execution-safety bundle should reduce clutter without weakening rollback or diagnosis authority.

Decision: Actual `tul archive` move mode requires an explicit selector and is limited to `--noop` selections. Default/latest archive without a selector is refused in move mode. Imported, failed, mixed, and `--all` archive selectors remain dry-run-only until separate policy bundles authorize them. The archive engine skips latest and latest rollbackable reference states even when selected. Successful moves record an `archive_last_run` summary in the latest remaining state.

Consequences: Users can safely run `tul archive --noop --keep 3` after reviewing `tul archive --noop --dry-run --keep 3`. Broader cleanup remains possible to inspect, but cannot silently move important state evidence.

## Decision: package inbox hygiene uses quarantine, not deletion

Accepted for K2. `tul package hygiene` defaults to dry-run and selects only invalid archives plus older duplicate matching package archives. `--quarantine` moves selected files under a package-quarantine root. It does not delete files and does not quarantine incompatible packages by default.

## Decision: shared Download is not tul-owned storage

Tul may scan shared Download roots for valid matching package archives, but it must not quarantine unrelated invalid zips from those roots. Package hygiene uses ingest for valid matching tul packages and reserves quarantine for project-owned inbox cleanup.

## 2026-05-13 — Stage 6 stabilization checkpoint

Decision: Close the J artifact-semantics track and K cleanup track as the Stage 6 stabilization baseline.

Accepted facts:

- `tul-vf-latest.md` is the canonical post-update evidence artifact.
- `tul export review` is the explicit compact review transport path.
- `tul-main.zip` is not backup evidence and is not accepted as automatic source export.
- Actual archive cleanup is currently limited to no-op state moves after dry-run inspection.
- Package hygiene ingests valid tul packages from shared roots and treats unrelated shared invalid zip files as report-only.

Next planning step: start Stage 7 around manifest, short-term/mid-term/long-term planning, and bounded parallel candidate management.


## ADR-026 — Stage 7 uses planning consolidation before implementation

Status: accepted

Context: Stage 6 closed with a verified stabilization checkpoint, explicit review bundle export, cleanup safety, and package inbox hygiene. The next pressure is not another immediate runtime change but coordination: manifest, strategy, roadmap, status, checklists, learning log, decisions, artifact semantics, and parallel-readiness must agree before several candidate workstreams are planned.

Decision: Open Stage 7 with one large planning consolidation package. The package may touch many coordination documents in one commit, but it must exclude runtime behavior changes. Stage 7 permits parallel planning and comparison of candidate bundles, while actual package application remains sequential through `tul update` and closes with `tul-vf-latest.md`.

Consequences: The first Stage 7 package is Yellow because it owns coordination docs. Subsequent packages must classify themselves as Green, Yellow, Orange, or Red and serialize whenever they share coordination files, runtime files, artifact semantics, or acceptance gates.

## ADR-027 — GitHub source archives may be source context but not tul runtime artifacts

Status: accepted

Context: A `tul-main.zip` downloaded from GitHub is a valid source archive for reading repo contents, but it has different provenance and root layout semantics from a future tul-generated `tul export source` artifact.

Decision: A GitHub-generated `tul-main.zip` can be used as manual source baseline/context for package generation when it plausibly corresponds to the verified HEAD. It must not be treated as backup, rollback authority, review bundle, or a tul-proven explicit source export. Future `tul export source` must record root layout, freshness, HEAD provenance, sha256, bytes, file count, and exclusions.

Consequences: Package-generation sessions can use GitHub source zips without pretending they are runtime evidence. Runtime truth remains `tul-vf-latest.md`; recovery authority remains Git remote plus commit hashes and rollback state.


## ADR-028 — Source context and source export are separate terms

Status: accepted

Context: After Stage 7 planning consolidation, the user pointed out that `tul export source` was not a valid current command. A repo-wide terminology audit also found that `repo zip`, `source zip`, `source bundle`, `source context`, and `source export` could still be read as interchangeable.

Decision: Use `source context` for currently available file contents used in package generation or code-level diagnosis. Use `source export` only for a future tul-generated artifact with explicit provenance and root-layout evidence. `tul export source` is proposed, not implemented. A GitHub-generated `tul-main.zip` can be manual source context, but it is not review evidence, backup authority, or a tul-proven source export.

Consequences: Documentation and help text must not ask the user to run `tul export source` until an implementation package has closed. Future source-export work must serialize after terminology/spec baselines and must prove command wiring, output path, root layout, HEAD provenance, sha256, bytes, file count, and exclusions.


## ADR-029 — Source export spec and package gates precede implementation

Status: accepted

Context: After terminology audit closed, the remaining Green/Yellow work was to prevent the next Orange implementation from reintroducing ambiguity. `tul export source` is still not a runnable command, but its future command contract, zip layout, provenance, exclusions, and validation gate need to be fixed before implementation.

Decision: Accept `docs/workflows/source-export-spec.md` as the pre-implementation source-export contract and `docs/checklists/stage7-package-gates.md` as the copy-ready Stage 7 package gate checklist. Source-export implementation remains Orange class and must serialize after this spec/gate baseline. Automatic post-update source export remains Red class and unapproved.

Consequences: Future source-export packages have less room to blur source context, source export, review bundle, and backup authority. Fresh LLM sessions must not ask the user to run `tul export source` until an implementation package closes with release-gate evidence.
