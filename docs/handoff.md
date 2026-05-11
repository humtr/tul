# tul handoff

`tul handoff <project|path>` prints a structured prompt for the next LLM or coding session.

Modes:

- `initial-review`: after clone/init or when no update was just performed
- `post-update`: after a successful update package

A handoff should include repo, branch, HEAD, remote HEAD if available, working tree status, invariants, rollback command when available, and an explicit request for remote verification.
