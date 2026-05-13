> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# Evaluation matrix

Scoring scale: 1 = weak, 3 = acceptable, 5 = strong.

| Criterion | Option 1: README only | Option 2: README brief + handoff | Option 3: README comprehensive + handoff |
|---|---:|---:|---:|
| New LLM can find the starting point quickly | 4 | 5 | 4 |
| Current status discoverability | 4 | 5 | 5 |
| Low staleness risk | 1 | 5 | 2 |
| Separates runtime facts from durable docs | 1 | 5 | 3 |
| Keeps README maintainable | 1 | 5 | 2 |
| Compact handoff by default | 1 | 5 | 2 |
| Works when only README is visible | 5 | 4 | 5 |
| Works when only handoff is visible | 1 | 4 | 5 |
| Minimizes duplicate invariant text | 1 | 5 | 2 |
| Supports `/tul ...` command grammar | 2 | 5 | 5 |
| Suitable for repeated self-host loop | 2 | 5 | 3 |
| Total | 23 | 53 | 38 |

## Preliminary recommendation

Option 2 is the best production default.

Option 1 is too brittle because README becomes both durable instruction and volatile state surface.
Option 3 is robust for disconnected review but too verbose and duplication-heavy for default use.
Option 2 best matches the tul loop contract:

- README is the stable entrypoint.
- Dedicated docs hold status, roadmap, checklist, command grammar, and instructions.
- Runtime handoff carries runtime facts.
- `--full` remains available for high-context transfer.
