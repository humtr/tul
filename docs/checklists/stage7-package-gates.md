# Stage 7 package gates

Use this checklist before generating or applying a Stage 7 package.

## Shared required declaration

Every package proposal must state:

```text
Bundle name:
Goal:
Baseline HEAD:
Baseline artifact:
Source context used:
Expected changed files:
Intentionally excluded files:
Parallel class:
Serialize because:
Acceptance criteria:
Rollback expectation:
```

## Green gate

Use Green only for isolated documentation, template, or wording work that does not own current status or runtime behavior.

Required checks:

- [ ] latest `tul-vf-latest.md` is PASS;
- [ ] package uses current runtime baseline;
- [ ] changed files are isolated and listed;
- [ ] no runtime files are changed;
- [ ] no command is described as runnable unless it currently exists;
- [ ] package inspect/check pass;
- [ ] update closes with release gate PASS.

## Yellow gate

Use Yellow for coordination documents, artifact vocabulary, roadmap/status text, cross-document checklists, or spec-only packages that affect future implementation boundaries.

Required checks:

- [ ] all Green checks pass;
- [ ] coordination files touched by the package are owned by this one package;
- [ ] current status and roadmap do not compete with another pending package;
- [ ] artifact roles are named consistently;
- [ ] future commands are marked as future, not runnable;
- [ ] implementation files are excluded except version metadata or non-behavior comments/docstrings;
- [ ] next ready queue is updated or deliberately left stable.

## Orange gate

Use Orange for new CLI commands, export behavior, verify/check behavior, docs drift checks, package-hygiene logic, state/report/handoff schema changes, or any runtime behavior change that remains bounded.

Required checks:

- [ ] all relevant Yellow checks pass;
- [ ] spec or acceptance gate is already accepted;
- [ ] behavior-changing files are listed explicitly;
- [ ] smoke tests cover the changed command;
- [ ] failure modes and rollback path are documented;
- [ ] release gate and fresh clone close the package.

## Red gate

Use Red for default update behavior changes, automatic exports, rollback/archive policy expansion, broad cleanup, external target onboarding, cross-repo changes, or any package with significant destructive or coordination risk.

Required checks:

- [ ] a separate dry-run or design package has closed first;
- [ ] user approval is explicit for the risky behavior;
- [ ] acceptance criteria include negative tests or refusal cases;
- [ ] rollback and recovery are concrete;
- [ ] no unrelated work is included.

## Source-export implementation gate

For an Orange `tul export source` implementation package, confirm:

- [x] `docs/workflows/source-export-spec.md` exists;
- [x] `docs/workflows/source-context-and-export.md` distinguishes implemented explicit source export from manual source context;
- [x] the package does not also change unrelated planning status beyond implementation bookkeeping;
- [x] default output path is explicit;
- [x] root-layout and exclusion checks are included;
- [x] state wording uses source-export terminology only.

## Export integrity hardening gate

`tul export status` is the warning-only inspection surface for source/review export freshness and small docs drift checks. It may be run manually or captured in verify snapshots. After the post-update export automation package closes, normal `tul update` should leave source/review artifacts current; stale/missing/invalid artifacts remain warnings, not release-gate failures.
