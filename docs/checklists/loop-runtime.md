# Loop runtime checklist

Before accepting a package:

```bash
tul package
tul package check /sdcard/Download/<package>.zip --target tul
tul update
# If the package modifies verify.py and the immediate post-update artifact still uses the old bootstrap layout:
tul verify fresh
# Upload instead of pasting long output:
# /sdcard/termux/import/tul/tul-vf-latest.md
```

Use explicit targets when context is ambiguous:

```bash
tul update tul -l
tul verify tul --fresh-clone
```

For package authoring:

```bash
tul package new NAME --target tul --message "Commit message"
tul package add NAME --target tul FILE [FILE...]
tul package show NAME
tul package zip NAME --out /sdcard/Download/NAME.zip --force
tul package check /sdcard/Download/NAME.zip --target tul
```

Before update, package check should catch:

- nested `tul-package.yml` or `README.md`;
- missing `files/` payload;
- generated/cache files in the archive;
- missing apply sources;
- duplicate destinations;
- `apply.files[*].to` and `commit.files` mismatches;
- target project/repo/branch mismatch when `--target` is supplied.

Invariants:

- `tul run` pushes by default.
- No-argument `tul package`, `tul update`, and `tul run` select from configured inbox roots only.
- No `git add -A` or `git add .` in the normal path.
- No force push.
- Repo policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- Import-root verify latest artifacts are `tul-vf-latest.md/json` only.
- Timestamped verify run artifacts live under `logs/verify/<YYMMDD>/` without a `runs/` layer.

## Planning harness checkpoint

- [x] README links to the planning harness or LLM entrypoint documents.
- [x] `docs/manifest.md` exists and states vision/invariants.
- [x] `docs/strategy.md` exists and defines capability map.
- [x] `docs/roadmap.md` contains ready queue and bundle candidates.
- [x] `docs/status/current.md` names current mode and next package.
- [x] `docs/learning-log.md` records known execution lessons.
- [x] `docs/decisions.md` records accepted planning decisions.
- [x] `docs/protocols/planning-loop.md` defines top-down and bottom-up planning.

## Verify artifact checkpoint

- [x] `tul verify tul` prints artifact paths.
- [x] `tul verify tul --fresh-clone` writes markdown and JSON artifacts.
- [x] `tul verify fresh` is accepted as shorthand for fresh-clone verification.
- [x] Termux default artifact path is `/sdcard/termux/import/tul/logs/verify/`.
- [x] The stable latest file can be uploaded instead of pasting terminal output.
- [x] `--no-log` remains available for exceptional runs.

## Verify artifact filenames

- [x] `/sdcard/termux/import/tul/tul-vf-latest.md` is the canonical latest markdown upload file.
- [x] `tul-vf-latest.json` is the canonical latest machine-readable file.
- [x] Fresh run artifacts use `tul-vf-f-YYMMDD-HHMMSS-<head7>.md/json`.
- [x] Local run artifacts use `tul-vf-l-YYMMDD-HHMMSS-<head7>.md/json`.
- [x] Timestamped run artifacts are stored under `logs/verify/<YYMMDD>/` date folders.
- [x] Legacy `tul-verify-latest.*` aliases are no longer written after the canonical layout implementation.
- [x] Artifact metadata contains no legacy latest paths.

## Native context checkpoint

- [x] `tul setup use tul` writes an active project context file.
- [x] `tul show config` reports active/default/current-directory context.
- [x] `tul show projects` marks active/default projects.
- [x] `tul doctor tul` reports runtime context.
- [x] `tul setup use tul --default` safely updates global `default_project`.
- [x] No-arg `tul run` is available with guarded mutating-command inference.

## Native context checks

- [x] `tul setup use <project>` stores an active project.
- [x] `tul show config` shows active/default/current-directory context.
- [x] Read-only commands can infer the project target when safe.
- [x] `tul verify fresh` is accepted as shorthand for `--fresh-clone`.
- [x] Mutating commands stop on active/cwd context conflict.
- [x] `tul run` can safely infer project and latest package.
- [x] Package manifest mismatch guidance explains incompatible zip targets.

## Package guidance checkpoint

- [x] `tul package` displays selected matching package and selection reason.
- [x] Incompatible package targets are shown when present.
- [x] Invalid archives without readable root `tul-package.yml` are ignored with a reason.
- [x] No-match errors provide next command options.

## Update-integrated verify gate

- [x] Update-integrated verify gate is installed.
- [x] Handoff compatibility hotfix is installed.
- [x] A normal docs-only smoke package proves `tul run` can apply, commit, push, run post-update `verify fresh`, write `tul-vf-latest.md`, and generate handoff in one command.
- [x] Normal `tul run` prints update report before verify/handoff.
- [x] Normal `tul run` shows commit, push verification, and rollback before the verify gate.
- [x] Normal `tul run` runs post-update `verify fresh` unless `--no-verify`, `--no-commit`, or `--no-push` applies.
- [x] Report, state, and handoff include verify gate result and artifact paths.
- [x] If the post-update verify gate fails, terminal output is still printed and the command exits non-zero.

## State output checkpoint

- [x] Default `tul show` is compact decision output.
- [x] Default `tul show` shows latest state and latest rollbackable commit separately.
- [x] `tul show history 5` preserves full state summaries.
- [x] `tul show --json` preserves machine-readable output.
- [x] Compact state output includes cleanup guidance for no-op/imported state clutter.

## Package authoring diagnostics checkpoint

- [x] `tul package check` reports nested-root package layout clearly.
- [x] `tul package check` validates that apply sources are under `files/`.
- [x] `tul package check` validates that payload files are referenced by `apply.files`.
- [x] `tul package check` validates that apply destinations and `commit.files` align.
- [x] `tul package check --target tul` keeps apply-plan validation for compatible packages.
- [x] No-match package guidance suggests both inspect and check commands.

## Archive cleanup dry-run checkpoint

- [x] `tul show` cleanup guidance points to dry-run before moving files.
- [x] `tul clean states` accepts omitted target through guarded native context.
- [x] `tul clean states` prints inventory counts.
- [x] Archive dry-run output shows source and archive destination directories.
- [x] Archive dry-run output identifies latest and latest rollbackable reference states.
- [x] Actual state moves require re-running without `--dry-run`.
- [x] Actual archive moves require an explicit selector.
- [x] K1 actual archive moves are limited to `--noop` selections.
- [x] Latest state and latest rollbackable state are protected from archive movement.
- [x] Actual archive moves record `archive_last_run` in the latest remaining state.

## Handoff discoverability checkpoint

- [x] README points fresh LLM sessions to `docs/llm/entrypoint.md`.
- [x] README and entrypoint point post-update reviewers to `docs/llm/post-update-review.md`.
- [x] Compact handoff includes `docs/llm/post-update-review.md` in read-next pointers.
- [x] Handoff protocol separates runtime facts from durable repo guidance.
- [x] Post-update review guidance states when `tul-vf-latest.md` is sufficient.
- [x] Post-update review guidance states when `tul show` is needed.
- [x] Post-update review guidance states when source context is needed.

## Parallel readiness checkpoint

- [x] `docs/workflows/parallel-readiness.md` defines single-bundle readiness conditions.
- [x] The readiness guide defines Green/Yellow/Orange/Red bundle classes.
- [x] The readiness guide requires touched-file overlap checks before package generation.
- [x] Runtime-file overlap forces serialization.
- [x] Verify/update/pipeline/rollback/archive move/push behavior changes force serialization.
- [x] Post-update review guidance requires next-bundle readiness classification.
- [x] Compact handoff points fresh sessions to the parallel-readiness guide.
- [x] Packages are still applied one at a time through `tul run` and closed with `tul-vf-latest.md`.


## Import-root latest snapshot checkpoint

- [x] Stable latest verify markdown/json live in the tul update dry root, possibly beside manually supplied source-context archives.
- [x] Timestamped run artifacts remain under `logs/verify/YYMMDD/`.
- [x] Latest markdown includes `## Runtime snapshots`.
- [x] Latest markdown includes compact `tul show`.
- [x] Latest markdown includes compact `tul show handoff`.
- [x] `tul run` rewrites the markdown artifact after final handoff-ready state is recorded.
- [x] Legacy `tul-verify-latest.*` aliases remain absent.


## State verify path alignment

- [x] `tul show` shows `/sdcard/termux/import/tul/tul-vf-latest.md` as the verify artifact when a latest verify artifact is available.
- [x] `tul-vf-latest.md` runtime snapshot `### tul show` shows the same import-root latest path.
- [x] Timestamped run artifacts remain under `/sdcard/termux/import/tul/logs/verify/YYMMDD/`.
- [x] No legacy `tul-verify-latest.*` artifacts are generated.

## Source/review export checkpoint

- [x] Automatic `tul-main.zip` source export is not considered closed.
- [x] Legacy source zip paths are not displayed as successful artifacts in compact state.
- [x] `tul export review` creates a compact diff-oriented review bundle.
- [x] `tul export source` creates an explicit full source export with root-layout checks.
- [x] Source export is proven before automatic post-update export.

## Artifact semantics checkpoint

- [x] `tul-vf-latest.md` is the canonical post-update release-gate artifact.
- [x] Runtime snapshots in latest verify markdown reduce the need to paste `tul show` and `tul show handoff`.
- [x] Timestamped verify runs remain under `logs/verify/YYMMDD/`.
- [x] Zip artifacts are transport artifacts, not backups.
- [x] Automatic `tul-main.zip` export is not considered closed.
- [x] Misleading source zip state output is removed or clearly marked as unresolved.
- [x] `tul export review` creates a compact diff-oriented review bundle.
- [x] `tul export source` creates an explicit full source export with root-layout checks.
- [x] Source export is proven before automatic post-update export.


## Review bundle export checkpoint

- [x] `tul export review` creates `/sdcard/termux/import/tul/tul-review-latest.zip`.
- [x] Review bundle contains `tul-vf-latest.md`, `state.json`, `report.md`, `handoff.md`, `changed-files.txt`, and `diff.patch`.
- [x] Review bundle includes copies of changed files only under `files/`.
- [x] Review bundle is documented as a transport artifact, not a backup.
- [x] Review export remains separate from verify and update until explicit command behavior is verified.
- [x] Review export metadata is visible in `tul show` after `tul export review`.
- [x] Review export refreshes `tul-vf-latest.md` runtime snapshots after explicit export.

## Package inbox hygiene checkpoint

- [x] `tul clean packages` exists as a dry-run command.
- [x] Invalid archives are identified with reasons.
- [x] Older duplicate matching packages are selected while the newest matching archive per package name is kept.
- [x] `tul clean packages run` moves selected archives instead of deleting them.
- [x] Incompatible package quarantine remains deferred.

## Package hygiene checklist

- Run `tul clean packages` before moving package archives.
- Use `tul clean packages run` only for valid matching tul packages outside the project inbox.
- Use `tul clean packages run` only after confirming project-inbox cleanup candidates.
- Do not quarantine unrelated shared Download files.

## Stage 6 stabilization checkpoint

- [x] J1 artifact semantics checkpoint is closed.
- [x] J2 misleading source zip state output is suppressed or marked unresolved.
- [x] J3 explicit review bundle export is available.
- [x] J4 review export rewrite and state integration are verified.
- [x] K1 archive execution safety is verified with no-op archive moves only.
- [x] K2 package inbox ingest policy is verified.
- [x] Shared Download invalid archives are report-only by default.
- [x] Valid matching tul packages can be ingested into the project inbox.
- [x] Project-inbox quarantine remains explicit and move-based.
- [x] Stage 6 is closed as the verified stabilization baseline before Stage 7 planning.


## Stage 7 planning consolidation checkpoint

- [x] Latest verified baseline is recorded as `5086c982ae5d52c586049d4fb21c8e7d4ada006d`.
- [x] Stage 6 stabilization checkpoint is treated as closed when the latest verify artifact is PASS.
- [x] Stage 7 active mode is `parallel planning, sequential gated update`.
- [x] Short-term, mid-term, and long-term plans are represented in roadmap/status.
- [x] Bundle candidates are classified as Green, Yellow, Orange, or Red.
- [x] Coordination files are identified and serialized.
- [x] Runtime behavior changes are excluded from the planning consolidation package.
- [x] Review bundle and source bundle semantics remain separated.
- [x] GitHub-generated `tul-main.zip` can be source context but not backup or tul-proven source export.
- [x] `tul export source` has an accepted implementation spec and implementation; post-update automation is warning-only.
- [ ] Any automatic review/source export is approved in a separate package.


## Stage 7 Green/Yellow source-spec gates checkpoint

- [x] Stage 7 planning consolidation is closed before implementation work.
- [x] Stage 7 terminology audit is closed before implementation work.
- [x] `docs/workflows/source-export-spec.md` defines the source-export contract before runtime implementation.
- [x] `docs/checklists/stage7-package-gates.md` defines Green/Yellow/Orange/Red gate requirements.
- [x] `tul export source` is runnable only after the Orange implementation package closes.
- [x] Explicit `tul export source` implementation closes against the accepted spec.
- [ ] Automatic post-update source export remains Red class and unapproved.

## Export integrity checkpoint

`tul show exports` is the warning-only inspection surface for source/review export freshness and small docs drift checks. It may be run manually or captured in verify snapshots. After the post-update export automation package closes, normal `tul run` should leave source/review artifacts current; stale/missing/invalid artifacts remain warnings, not release-gate failures.
