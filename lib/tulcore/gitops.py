"""Git command wrappers."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable

from .errors import GitError


def run(cmd: list[str] | str, cwd: Path | None = None, *, shell: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        shell=shell,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode != 0:
        command = cmd if isinstance(cmd, str) else " ".join(cmd)
        raise GitError(
            f"command failed ({proc.returncode}): {command}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
    return proc


def git(repo: Path, args: Iterable[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], repo, check=check)


def repo_root(path: Path) -> Path:
    proc = git(path, ["rev-parse", "--show-toplevel"])
    return Path(proc.stdout.strip()).resolve()


def current_branch(repo: Path) -> str:
    return git(repo, ["branch", "--show-current"]).stdout.strip()


def head(repo: Path) -> str:
    return git(repo, ["rev-parse", "HEAD"]).stdout.strip()


def short_head(repo: Path) -> str:
    return git(repo, ["rev-parse", "--short", "HEAD"]).stdout.strip()


def status_porcelain(repo: Path) -> str:
    return git(repo, ["status", "--porcelain"], check=False).stdout.rstrip()


def is_dirty(repo: Path) -> bool:
    return bool(status_porcelain(repo).strip())


def remote_url(repo: Path) -> str | None:
    proc = git(repo, ["config", "--get", "remote.origin.url"], check=False)
    value = proc.stdout.strip()
    return value or None


def fetch(repo: Path, branch: str | None = None) -> None:
    if branch:
        git(repo, ["fetch", "origin", branch])
    else:
        git(repo, ["fetch", "--all", "--prune"])


def remote_head(repo: Path, branch: str) -> str | None:
    proc = git(repo, ["rev-parse", f"origin/{branch}"], check=False)
    value = proc.stdout.strip()
    return value if proc.returncode == 0 and value else None


def ahead_behind(repo: Path, branch: str) -> tuple[int, int] | None:
    proc = git(repo, ["rev-list", "--left-right", "--count", f"HEAD...origin/{branch}"], check=False)
    if proc.returncode != 0:
        return None
    parts = proc.stdout.strip().split()
    if len(parts) != 2:
        return None
    return int(parts[0]), int(parts[1])


def pull_ff_only(repo: Path) -> None:
    git(repo, ["pull", "--ff-only"])


def recent_commits(repo: Path, count: int = 5) -> list[str]:
    proc = git(repo, ["log", f"-{count}", "--oneline"], check=False)
    return [line for line in proc.stdout.splitlines() if line.strip()]


def changed_files(repo: Path, *, staged: bool = False) -> list[str]:
    args = ["diff", "--name-only"]
    if staged:
        args.insert(1, "--cached")
    lines = git(repo, args, check=False).stdout.splitlines()
    if not staged:
        untracked = git(repo, ["ls-files", "--others", "--exclude-standard"], check=False).stdout.splitlines()
        lines.extend(untracked)
    return sorted(set(line.strip() for line in lines if line.strip()))


def stage_files(repo: Path, files: list[str]) -> None:
    if not files:
        raise GitError("no files provided for staging")
    forbidden = {"-A", ".", "--all"}
    if any(item in forbidden for item in files):
        raise GitError("broad staging is forbidden; use explicit files only")
    git(repo, ["add", "--", *files])


def commit(repo: Path, message: str) -> str:
    if not message.strip():
        raise GitError("commit message is empty")
    git(repo, ["commit", "-m", message])
    return head(repo)


def push_verify(repo: Path, branch: str) -> tuple[str, str]:
    git(repo, ["push", "origin", branch])
    fetch(repo, branch)
    local = head(repo)
    remote = remote_head(repo, branch)
    if local != remote:
        raise GitError(f"remote HEAD verification failed: local={local}, origin/{branch}={remote}")
    return local, remote or ""


def diff_check(repo: Path, *, staged: bool = False) -> str:
    args = ["diff", "--check"]
    if staged:
        args.insert(1, "--cached")
    proc = git(repo, args, check=False)
    if proc.returncode != 0:
        raise GitError(proc.stdout + proc.stderr)
    return proc.stdout


def clone(slug: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{slug}.git"
    run(["git", "clone", url, str(dest)])
