# update pipeline

`update` is the package application and publishing step. It is not the whole user-facing loop.

## Canonical split

```text
update = apply package -> checks -> commit -> push -> remote HEAD check
run    = update when needed -> export -> verify fresh -> show
```

## Normal user path

```bash
tul run
```

## Stepwise path

```bash
tul package
tul update
tul export
tul verify fresh
tul show
```

## Update responsibilities

`update` should:

- select an explicit package or the newest compatible package;
- validate package target and payload;
- apply only listed files;
- run pre-publish checks;
- stage only listed commit files;
- commit with package commit metadata;
- push by default;
- verify local HEAD equals remote HEAD after push;
- write update state/report/handoff records.

`update` should not be the canonical place for source/review export or uploadable fresh verification. `run` orchestrates those steps.

## Safety invariants

- no `git add -A`;
- no `git add .`;
- no force push;
- no broad cleanup;
- package policy remains in package manifests and `.tul.yml`;
- environment paths remain in global config.
