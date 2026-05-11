"""Repository validation checks."""
from __future__ import annotations

import fnmatch
import subprocess
import shutil
from pathlib import Path

from .errors import CheckError
from .gitops import diff_check


def run_checks(repo: Path, repo_config: dict, *, log_path: Path | None = None) -> list[str]:
    outputs: list[str] = []
    check = repo_config.get("check") or {}
    commands = check.get("commands") or []
    for command in commands:
        proc = subprocess.run(
            str(command),
            cwd=str(repo),
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        block = f"$ {command}\n{proc.stdout}{proc.stderr}".rstrip()
        outputs.append(block)
        _cleanup_bytecode(repo)
        if proc.returncode != 0:
            _write_log(log_path, outputs)
            raise CheckError(block)
    _cleanup_bytecode(repo)
    if not any(str(cmd).strip() == "git diff --check" for cmd in commands):
        diff_check(repo)
        outputs.append("$ git diff --check\nOK")
    forbidden = check.get("forbidden") or []
    outputs.extend(run_forbidden_checks(repo, forbidden))
    _cleanup_bytecode(repo)
    _write_log(log_path, outputs)
    return outputs


def run_forbidden_checks(repo: Path, forbidden: list) -> list[str]:
    outputs: list[str] = []
    for item in forbidden:
        if not isinstance(item, dict):
            continue
        pattern = str(item.get("pattern") or "")
        if not pattern:
            continue
        roots = item.get("paths") or ["."]
        matches = []
        for raw_root in roots:
            root = repo / str(raw_root)
            if not root.exists():
                continue
            paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
            for path in paths:
                if ".git" in path.parts:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                except OSError:
                    continue
                if fnmatch.fnmatch(text, pattern) or pattern in text:
                    matches.append(path.relative_to(repo).as_posix())
        if matches:
            raise CheckError(f"forbidden pattern found: {pattern}\n" + "\n".join(matches))
        outputs.append(f"forbidden pattern OK: {pattern}")
    return outputs


def _write_log(path: Path | None, outputs: list[str]) -> None:
    if not path:
        return
    path.write_text("\n\n".join(outputs) + "\n", encoding="utf-8", newline="\n")


def _cleanup_bytecode(repo: Path) -> None:
    for cache in repo.rglob("__pycache__"):
        if ".git" in cache.parts:
            continue
        shutil.rmtree(cache, ignore_errors=True)
    for pyc in repo.rglob("*.pyc"):
        if ".git" in pyc.parts:
            continue
        try:
            pyc.unlink()
        except OSError:
            pass
