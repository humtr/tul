# tul command grammar

This document defines LLM-side command phrases for the loop. These are prompts a user may give to an LLM, not necessarily terminal commands.

## Grammar

```text
/tul next <project>
/tul review <project>
/tul package <project>
/tul roadmap <project>
/tul verify <project>
/tul init-review <project>
```

## Meanings

### `/tul next <project>`

Inspect the repo and propose the next package boundary.

### `/tul review <project>`

Review the latest pushed commit and handoff output.

### `/tul package <project>`

Create a cross-platform tul package for the agreed next scope.

### `/tul roadmap <project>`

Review or update durable roadmap/status/checklist documents.

### `/tul verify <project>`

Verify that the repo state matches the handoff, protocol, roadmap, checklist, and invariants.

### `/tul init-review <project>`

Perform first review after clone or init.

## Output requirements

Responses should separate:

- user-stated goals
- terminal-verified facts
- repo/source-backed facts
- assistant interpretation
- unresolved uncertainty
