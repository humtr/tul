# Planning Harness Checklist

Use this checklist when changing the planning system, roadmap, manifest, or cross-project harness templates.

## Structure

- [ ] README links to manifest, strategy, roadmap, status, learning log, and decisions.
- [ ] README remains compact and does not become the full planning ledger.
- [ ] `docs/manifest.md` states vision, invariants, human role, and change rules.
- [ ] `docs/strategy.md` defines the medium-term capability map.
- [ ] `docs/roadmap.md` contains a ready queue and bundle candidates.
- [ ] `docs/status/current.md` names the current mode, latest known version, and next package.
- [ ] `docs/learning-log.md` records bottom-up lessons.
- [ ] `docs/decisions.md` records accepted decisions with rationale.
- [ ] `docs/protocols/planning-loop.md` defines top-down and bottom-up loops.
- [ ] `templates/project-harness/*` exists for future target repos.

## Planning behavior

- [ ] Ready queue items are derived from strategy capability pressure.
- [ ] Bundle candidates are coherent and bounded.
- [ ] After a package lands, status/current is updated if the current mode or next package changes.
- [ ] Lessons are added when actual execution changes our understanding.
- [ ] Repeated lessons can update strategy.
- [ ] Manifest changes use the escalation rules and decisions log.
- [ ] Stage X deferred targets remain visible.

## Safety

- [ ] Planning changes do not weaken update full-loop semantics.
- [ ] Planning changes do not suggest broad staging or force push.
- [ ] Planning changes keep project-specific policy out of engine code.
- [ ] Planning changes preserve the distinction between durable docs and runtime facts.
