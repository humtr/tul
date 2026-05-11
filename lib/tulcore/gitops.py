from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence

from .errors import TulError


def run(args: Sequence[str], cwd: Path | None = None, check: bool = True, capture: bool = False):
    return subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        text=True,
        check=check,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def out(args: Sequence[str], cwd: Path | None = None, check: bool = True) -> str:
    cp = run(args, cwd=cwd, check=check, capture=True)
    return cp.stdout.strip()


def git(repo: Path, *args: str, check: bool = True, capture: bool = False):
    return run(["git", *args], cwd=repo, check=check, capture=capture)


def gout(repo: Path, *args: str, check: bool = True) -> str:
    return out(["git", *args], cwd=repo, check=check)


def repo_root(path: str | Path) -> Path:
    p = Path(str(path)).expanduser()
    if not p.exists():
        raise TulError(f"path does not exist: {p}")
    return Path(out(["git", "-C", str(p), "rev-parse", "--show-toplevel"]))


def is_repo(path: Path) -> bool:
    return run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], check=False, capture=True).returncode == 0


def branch(repo: Path) -> str:
    return gout(repo, "branch", "--show-current")


def head(repo: Path, short: bool = False) -> str:
    if short:
        return gout(repo, "rev-parse", "--short", "HEAD")
    return gout(repo, "rev-parse", "HEAD")


def upstream(repo: Path) -> str | None:
    cp = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False, capture=True)
    return cp.stdout.strip() if cp.returncode == 0 and cp.stdout.strip() else None


def remote_url(repo: Path) -> str | None:
    cp = git(repo, "remote", "get-url", "origin", check=False, capture=True)
    return cp.stdout.strip() if cp.returncode == 0 and cp.stdout.strip() else None


def status(repo: Path) -> list[str]:
    return [x for x in gout(repo, "status", "--porcelain").splitlines() if x.strip()]


def changed(repo: Path) -> list[str]:
    return [x.replace("\\", "/") for x in gout(repo, "diff", "--name-only").splitlines() if x.strip()]


def staged(repo: Path) -> list[str]:
    return [x.replace("\\", "/") for x in gout(repo, "diff", "--cached", "--name-only").splitlines() if x.strip()]


def untracked(repo: Path) -> list[str]:
    return [x.replace("\\", "/") for x in gout(repo, "ls-files", "--others", "--exclude-standard").splitlines() if x.strip()]


def compare_upstream(repo: Path) -> tuple[int, int] | None:
    up = upstream(repo)
    if not up:
        return None
    a, b = gout(repo, "rev-list", "--left-right", "--count", f"HEAD...{up}").split()
    return int(a), int(b)


def sync(repo: Path) -> str:
    if status(repo):
        raise TulError("sync aborted: working tree is dirty")
    git(repo, "fetch", "origin")
    up = upstream(repo)
    if not up:
        return "no upstream configured"
    comp = compare_upstream(repo)
    if comp is None:
        return "no upstream comparison available"
    ahead, behind = comp
    if ahead == 0 and behind == 0:
        return f"already up to date with {up}"
    if ahead == 0 and behind > 0:
        git(repo, "pull", "--ff-only")
        return f"pulled {behind} commit(s) from {up}"
    if ahead > 0 and behind == 0:
        return f"local branch ahead of {up} by {ahead} commit(s)"
    raise TulError(f"branch diverged from {up}: ahead {ahead}, behind {behind}")


def recent(repo: Path, n: int = 5) -> str:
    return git(repo, "log", "--oneline", "--decorate", f"-{n}", check=False, capture=True).stdout.strip()


def last_commit_files(repo: Path) -> list[str]:
    cp = git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD", check=False, capture=True)
    return [x for x in cp.stdout.splitlines() if x.strip()]


def push_verify(repo: Path) -> tuple[str, str]:
    b = branch(repo)
    git(repo, "push", "origin", b)
    git(repo, "fetch", "origin", b)
    local = gout(repo, "rev-parse", "HEAD")
    remote = gout(repo, "rev-parse", f"origin/{b}")
    if local != remote:
        raise TulError(f"push verification failed: local HEAD != origin/{b}")
    return local, remote
