# tul post-update review prompt

You are receiving a post-update handoff from `tul update`.

Tasks:

1. Verify remote HEAD equals the expected pushed HEAD if remote access is available.
2. Read the state/report paths if available locally; otherwise use the handoff facts.
3. Read changed files and relevant repo documents.
4. Check invariants:
   - push-by-default was preserved
   - no broad staging was introduced
   - no force push was introduced
   - project policy remains in `.tul.yml`
   - environment paths remain in global config
5. Identify defects, regressions, and next package boundary.
6. Provide short/medium/long roadmap updates.

Output:

- remote verification
- changed-files review
- invariant regression check
- defects/risks
- next package recommendation
- source separation
