# roadmap

## Current baseline

The latest verified pre-redesign baseline is `57c80c403a651ea30319916ddc81b19a14384e6a`.

## Immediate queue

1. `tul-stage7-command-surface-redesign-bundle-v1`
   - add canonical command surface
   - remove legacy top-level command exposure
   - split `update` from full-loop `run`
   - move export inspection to `show exports`
   - make `verify` quick/local by default and `verify fresh` artifact-writing

2. Post-redesign verification follow-up
   - verify `tul package`
   - verify `tul run dry`
   - verify `tul show exports`
   - verify `tul verify` and `tul verify fresh`
   - verify upload artifacts are current after `tul run`

## Deferred

- broader cleanup behavior changes
- release-gate failure on export freshness warnings
- external repository onboarding
