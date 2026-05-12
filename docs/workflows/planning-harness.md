# Planning Harness Workflow

The planning harness is used when tul development starts moving faster than a static roadmap can track.

## Normal planning loop

1. Read `docs/status/current.md`.
2. Read `docs/strategy.md` for capability pressure.
3. Read `docs/roadmap.md` for ready queue and bundle candidates.
4. Read recent `docs/learning-log.md` entries.
5. Check `docs/decisions.md` for accepted constraints.
6. Pick a bounded package scope.
7. Apply through the normal tul loop.
8. Record any new lessons or decisions.

## Command loop

Current explicit command loop:

```bash
tul package latest tul
tul update tul -l
tul verify tul --fresh-clone
tul handoff tul
```

Future native context may reduce the command loop, but that must be implemented behind context conflict guards.

## When to update each document

| Document | Update when |
|---|---|
| `README.md` | entrypoints change |
| `docs/manifest.md` | vision, authority, safety, or invariants change |
| `docs/strategy.md` | capability maturity or pressure changes |
| `docs/roadmap.md` | ready queue or bundle candidates change |
| `docs/status/current.md` | current stage, next package, or verified loop changes |
| `docs/learning-log.md` | an execution lesson is learned |
| `docs/decisions.md` | a durable decision is accepted |

## Bundle discipline

Stage 6 bundles should normally contain 3–5 coherent items. A bundle can be larger only if changes are documentation-only or mechanically linked.
