#!/usr/bin/env python3
"""Print a simple static evaluation of README/handoff entrypoint strategies."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "experiments" / "entrypoint-strategy"
OPTIONS = [
    ("Option 1", BASE / "options" / "README-option-1.md"),
    ("Option 2", BASE / "options" / "README-option-2.md"),
    ("Option 3", BASE / "options" / "README-option-3.md"),
]

REQUIRED_TERMS = [
    "tul update",
    "--no-push",
    "git add -A",
    "force push",
    "tul-package.yml",
    "runtime",
    "roadmap",
]


def score_text(text: str) -> tuple[int, list[str]]:
    missing = [term for term in REQUIRED_TERMS if term not in text]
    return len(REQUIRED_TERMS) - len(missing), missing


def main() -> int:
    print("tul entrypoint strategy static check")
    print(f"base: {BASE}")
    for name, path in OPTIONS:
        text = path.read_text(encoding="utf-8")
        score, missing = score_text(text)
        print(f"\n{name}: {path}")
        print(f"  lines: {len(text.splitlines())}")
        print(f"  required-term score: {score}/{len(REQUIRED_TERMS)}")
        if missing:
            print(f"  missing: {', '.join(missing)}")
        else:
            print("  missing: none")
    print("\nSee docs/experiments/entrypoint-strategy/evaluation-matrix.md for qualitative scoring.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
