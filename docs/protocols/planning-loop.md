# Planning Loop Protocol

This protocol explains how tul turns feature work into a recursive planning system.

## Purpose

Stage 6 and later should not rely on a static roadmap. The project needs a loop that can incorporate fast implementation, execution lessons, strategic capability pressure, and long-term vision without losing safety.

## Top-down loop

```text
Vision
→ Strategy capability map
→ Roadmap ready queue
→ Bundle scope
→ Package implementation
→ tul update
```

Use this when deciding what to build next.

## Bottom-up loop

```text
Update result
→ State/report/handoff
→ Learning log
→ Roadmap adjustment
→ Strategy adjustment
→ Manifest adjustment if needed
```

Use this after each meaningful update, no-op discovery, failure, rollback, or UX friction.

## Escalation rules

| Finding | First destination | Possible escalation |
|---|---|---|
| One-off friction | Learning log | Roadmap ready queue |
| Repeated UX friction | Strategy | Manifest if it changes authority/safety |
| New implementation candidate | Roadmap | Strategy if it implies a capability gap |
| Commit/push/runtime fact | State/report/handoff | Not durable docs unless it changes planning |
| Major design decision | Decisions | Manifest when durable rule changes |
| Target repo deferral | Roadmap/decisions | Manifest if it changes project purpose |

## After each package

Ask:

1. Did the update publish, no-op, fail, or only import?
2. Did verification pass locally and through fresh clone?
3. What surprised us?
4. Which capability changed?
5. Does the ready queue change?
6. Does strategy change?
7. Does the manifest change?
8. Does a decision need to be recorded?
9. What is the next safest package boundary?

## LLM behavior

When receiving a handoff, the LLM should:

1. Treat terminal facts as runtime evidence.
2. Read README, manifest, status, strategy, roadmap, learning log, and decisions before proposing a package.
3. Separate user-stated goals, terminal-verified facts, assistant interpretation, accepted decisions, and uncertainty.
4. Propose a bounded package scope that advances the current capability pressure.
5. Preserve non-negotiable runtime invariants.
