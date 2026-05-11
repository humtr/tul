from __future__ import annotations

import glob
import shlex
from pathlib import Path

from .errors import TulError
from .gitops import git, run


def _expand(repo: Path, args: list[str]) -> list[str]:
    out = []
    for arg in args:
        if any(ch in arg for ch in "*?["):
            matches = sorted(glob.glob(str(repo / arg)))
            out.extend(matches if matches else [arg])
        else:
            out.append(arg)
    return out


def run_one(repo: Path, command: str) -> None:
    print(f"== {command} ==")
    args = _expand(repo, shlex.split(command))
    run(args, cwd=repo, check=True)


def run_forbidden(repo: Path, item: dict) -> None:
    pattern = item.get("pattern")
    paths = item.get("paths") or []
    if not pattern:
        return
    cp = git(repo, "grep", "-n", str(pattern), "--", *[str(p) for p in paths], check=False, capture=True)
    if cp.returncode == 0:
        print(cp.stdout)
        raise TulError(f"forbidden pattern found: {pattern}")


def run_checks(repo: Path, repo_config: dict) -> None:
    check = repo_config.get("check") or {}
    for cmd in check.get("commands") or []:
        run_one(repo, str(cmd))
    for item in check.get("forbidden") or []:
        if isinstance(item, dict):
            run_forbidden(repo, item)
    run_one(repo, "git diff --check")
