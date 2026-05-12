# Planning Harness Checklist

Use this checklist when changing the planning system, roadmap, manifest, or cross-project harness templates.

## Structure

- [x] README links to manifest, strategy, roadmap, status, learning log, and decisions.
- [x] README remains compact and does not become the full planning ledger.
- [x] `docs/manifest.md` states vision, invariants, human role, and change rules.
- [x] `docs/strategy.md` defines the medium-term capability map.
- [x] `docs/roadmap.md` contains a ready queue and bundle candidates.
- [x] `docs/status/current.md` names the current mode, latest known version, and next package.
- [x] `docs/learning-log.md` records bottom-up lessons.
- [x] `docs/decisions.md` records accepted decisions with rationale.
- [x] `docs/protocols/planning-loop.md` defines top-down and bottom-up loops.
- [x] `templates/project-harness/*` exists for future target repos.
- [x] `docs/workflows/stage7-bounded-parallel-planning.md` defines Stage 7 package classification and conflict rules.

## Planning behavior

- [x] Ready queue items are derived from strategy capability pressure.
- [x] Bundle candidates are coherent and bounded.
- [x] After a package lands, status/current is updated if the current mode or next package changes.
- [x] Lessons are added when actual execution changes our understanding.
- [x] Repeated lessons can update strategy.
- [x] Manifest changes use the escalation rules and decisions log.
- [x] Stage X deferred targets remain visible.
- [x] Stage 7 separates parallel planning from sequential gated application.
- [x] Coordination docs have an owner package before generation.

## Safety

- [x] Planning changes do not weaken update full-loop semantics.
- [x] Planning changes do not suggest broad staging or force push.
- [x] Planning changes keep project-specific policy out of engine code.
- [x] Planning changes preserve the distinction between durable docs and runtime facts.
- [x] Planning changes preserve source/review/backup artifact distinctions.
- [x] Planning changes serialize runtime behavior changes behind explicit acceptance gates.

## Stage 7 first-package gate

- [x] Stage 6 baseline is stated using the latest verified HEAD.
- [x] Stage 6 closure and Stage 7 active mode are separated.
- [x] Short-term, mid-term, and long-term plans are present.
- [x] Bundle candidate matrix is present.
- [x] Conflict/serialization rules are present.
- [x] Runtime implementation is excluded from the planning consolidation package.


## Stage 7 source-spec/gates gate

- [x] Source context and source export are separate terms.
- [x] Future `tul export source` has a pre-implementation specification.
- [x] Green/Yellow/Orange/Red gate templates are copy-ready.
- [x] Source export implementation remains serialized after the spec/gates baseline.
