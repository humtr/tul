# tul Manifest

This document is the durable manifesto for `humtr/tul`. README is the entrypoint. Runtime facts belong in terminal output, reports, handoffs, and state files. This manifest records the purpose, invariants, and planning rules that should survive across ChatGPT sessions, coding agents, and local terminal environments.

## 1. Vision

`tul` means **Terminal Update Loop**.

`tul` exists to minimize the human-in-the-loop bridge in LLM-assisted development while preserving human authority over intent, approval, execution, review, and rollback.

The goal is not to remove the user. The goal is to move the user from repetitive bridge work into decision authority:

| Current bridge labor | Intended human role |
|---|---|
| Copy paths and commands | Approve scope and risk |
| Manually inspect git state | Review concise release gates |
| Remember package names | Let tul discover matching packages |
| Paste long validation blocks | Run native verification commands |
| Explain context to new sessions | Point them at repo-resident handoff/docs |
| Recover from opaque failures | Use state, rollback, archive, and reports |

Long-term, the user should mostly approve direction, run a small number of native commands, read concise results, and decide whether to continue or rollback.

## 2. Human role transformation

The intended loop is:

```text
LLM proposes package boundary
→ user approves direction
→ LLM or package helper produces package
→ user places package in an inbox root
→ tul update <project> -l
→ tul applies/checks/sweeps/commits/pushes/verifies
→ tul prints rollback guidance and compact handoff
→ tul verify <project> --fresh-clone confirms the release gate
→ next LLM reads repo docs + handoff and continues
```

The near-term command loop remains explicit:

```bash
tul package latest tul
tul update tul -l
tul verify tul --fresh-clone
tul handoff tul
```

A future native context layer may reduce this to:

```bash
tul use tul
tul update
tul verify fresh
tul handoff
```

That future layer must be context-aware and safety-preserving.

## 3. Non-negotiable runtime invariants

- `tul update <project>` is the full-loop command.
- Commit and push are included by default after validation.
- `--no-commit` and `--no-push` are exceptions for debugging or recovery.
- Remote HEAD verification is part of a successful pushed update.
- Successful published updates print rollback guidance.
- Successful updates print an LLM-ready handoff.
- Do not use `git add -A` or `git add .` in the normal update path.
- Do not force push in the normal path.
- Project policy belongs in `.tul.yml`.
- Environment paths and aliases belong in global config.
- LLM packages should be cross-platform archives with `tul-package.yml + files/ + README.md`.
- Split commands exist for recovery, inspection, and debugging; they must not replace the default full loop.

## 4. Terminal Update Loop contract

The runtime loop should remain deterministic and inspectable:

```text
resolve target
→ sync precheck
→ discover/import package
→ validate manifest
→ build apply plan
→ safe apply
→ checks
→ sweep backups
→ verify changed files
→ explicit stage only
→ staged checks
→ commit
→ push
→ remote HEAD verification
→ rollback hint
→ report
→ compact handoff
```

The normal package target must match the repo target:

```yaml
target:
  project: tul
  repo: humtr/tul
  branch: main
```

If a future command infers a target, the inference must be explained and must stop when a mutating command is ambiguous.

## 5. Planning harness contract

Stage 6 introduces a planning harness. The purpose is to let tul accelerate feature work without losing strategic coherence.

The harness layers are:

```text
manifest      = vision, invariants, authority, change rules
strategy      = medium-term capability map
roadmap       = short-term ready queue and bundle candidates
status        = current checkpoint and next package
learning-log  = bottom-up lessons from actual runs
decisions     = accepted decisions and rationale
```

Top-down planning:

```text
Vision → Strategy → Roadmap → Package Scope → Update
```

Bottom-up improvement:

```text
Update Result → Learning Log → Roadmap → Strategy → Manifest if necessary
```

This is a recursive planning system, not a static roadmap.

## 6. Portable project harness

`tul` is both a tool and a project-management harness. The harness should be portable to future repositories such as `humtr/ai`.

A future target project should be able to carry the same planning skeleton:

```text
README.md
docs/manifest.md
docs/strategy.md
docs/roadmap.md
docs/status/current.md
docs/learning-log.md
docs/decisions.md
docs/checklists/project-loop.md
docs/llm/entrypoint.md
.tul.yml
```

Project-specific policy stays in that project. The harness shape is shared; the project content is not.

## 7. Stage X target onboarding

`humtr/ai` onboarding is intentionally deferred as **Stage X**.

The condition for Stage X is not a calendar date. Stage X should start when tul's own self-host loop is stable enough that onboarding another repo does not multiply bridge work.

Candidate entrance criteria:

- `tul update tul -l` is stable.
- `tul verify tul --fresh-clone` is a trusted release gate.
- Package discovery and authoring are usable without long path-pasting.
- State/archive/rollback output is concise enough for repeated use.
- Native project context is implemented or at least clearly specified.
- Windows/Termux parity has been tested enough to avoid environment-specific drift.

## 8. Manifest change rules

Not every lesson should change the manifest. Escalation rules:

| Observation type | Normal destination |
|---|---|
| One-off execution friction | `docs/learning-log.md`, then possibly `docs/roadmap.md` |
| Repeated UX or safety friction | `docs/strategy.md` capability pressure |
| Package boundary adjustment | `docs/roadmap.md` |
| Major accepted design decision | `docs/decisions.md` |
| Human authority, safety invariant, or long-term purpose changes | `docs/manifest.md` |

Manifest changes should be justified in `docs/decisions.md`.

## 9. Implementation checklist

### Core loop

- [x] Full-loop update command exists.
- [x] Commit/push are default in published updates.
- [x] Remote HEAD verification exists.
- [x] No-op updates are not failures.
- [x] Rollback guidance is printed.
- [x] Compact handoff exists.
- [x] Fresh clone verification exists.
- [ ] Native no-arg context exists.
- [ ] `tul verify fresh` shorthand exists.
- [ ] Mutating no-arg commands have context conflict guards.

### Package contract

- [x] `tul-package.yml + files/ + README.md` package format exists.
- [x] Latest matching package selection exists.
- [x] Package inspect/check/scaffold/add/zip/summary exist.
- [x] Apply plan is generated before copy.
- [x] Directory copy is guarded.
- [ ] Incompatible package candidates are explained clearly.
- [ ] Duplicate package name/hash guidance is strong.

### Planning harness

- [x] README is compact entrypoint.
- [ ] Manifest/strategy/roadmap/status/learning/decisions harness is present.
- [ ] Ready queue is maintained.
- [ ] Capability map guides short-term extraction.
- [ ] Update lessons are recorded.
- [ ] Decisions are recorded with rationale.

### Human bridge minimization

- [x] Package path can be replaced by `-l` in normal use.
- [x] Fresh clone checks can be run by `tul verify tul --fresh-clone`.
- [x] Package authoring helpers reduce manual zip work.
- [ ] Project names can be omitted safely through active context.
- [ ] State output is compact and decision-oriented.
- [ ] Handoff suggests next package boundary effectively.
