> Historical note: This document predates the Stage 7 command surface redesign. Command examples may use legacy forms. Current canonical commands are `tul show`, `tul package`, `tul update`, `tul verify`, `tul export`, `tul run`, `tul clean`, `tul recover`, and `tul setup`.

# Test protocol

This experiment should be validated through an actual commit/push so that a new LLM session can inspect the repo state without relying on prior chat context.

## Step 1 — Apply package

```bash
cd ~/prj/tul
PKG="/sdcard/Download/tul_entrypoint_strategy_test_v1.zip"
python bin/tul update tul --package "$PKG"
```

## Step 2 — Verify commit/push

```bash
cd ~/prj/tul
git fetch origin main
git rev-parse HEAD
git rev-parse origin/main
git status --short
```

Expected:

- local HEAD equals `origin/main`;
- working tree is clean;
- latest commit message is `Add LLM entrypoint strategy test`.

## Step 3 — Fresh clone review

```bash
cd ~
mkdir -p ~/tmp
rm -rf ~/tmp/tul-entrypoint-test

git clone https://github.com/humtr/tul.git ~/tmp/tul-entrypoint-test
cd ~/tmp/tul-entrypoint-test

git log --oneline --decorate -5
wc -l docs/experiments/entrypoint-strategy/README.md \
  docs/experiments/entrypoint-strategy/options/README-option-1.md \
  docs/experiments/entrypoint-strategy/options/README-option-2.md \
  docs/experiments/entrypoint-strategy/options/README-option-3.md \
  docs/experiments/entrypoint-strategy/evaluation-matrix.md
python -m py_compile bin/tul
python -m py_compile lib/tulcore/*.py
```

## Step 4 — Blind review prompts

Ask a new LLM session three questions with only one option file at a time:

1. What is the current tul stage?
2. What is the next package boundary?
3. Which facts are runtime facts and which are durable repo guidance?

Then compare answers against `evaluation-matrix.md`.

## Step 5 — Decision

If the test confirms the matrix, implement Option 2 in the production Stage 2 package:

- README brief entrypoint.
- `docs/llm/entrypoint.md` and durable docs.
- compact handoff default.
- `tul handoff --full`.
- `tul handoff --instructions`.
- `tul instructions`.
