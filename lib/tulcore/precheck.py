"""Repository preflight checks for the tul update loop."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import ProjectContext
from .errors import GitError, SafetyError
from .gitops import ahead_behind, current_branch, fetch, is_dirty, pull_ff_only


@dataclass(frozen=True)
class PrecheckResult:
    repo: Path
    branch: str
    expected_branch: str | None
    dirty: bool
    ahead: int | None = None
    behind: int | None = None
    pulled: bool = False

    @property
    def remote_checked(self) -> bool:
        return self.ahead is not None and self.behind is not None


def run_precheck(ctx: ProjectContext, *, allow_dirty: bool = False) -> PrecheckResult:
    """Validate that the repo is safe to update, then fast-forward if needed."""
    repo = ctx.repo_path
    branch = current_branch(repo)
    expected_branch = ctx.expected_branch
    if expected_branch and branch != expected_branch:
        raise SafetyError(f"branch mismatch: expected {expected_branch}, current {branch}")

    dirty = is_dirty(repo)
    if dirty and not allow_dirty:
        raise SafetyError(
            "working tree is dirty; refusing to apply a package over uncommitted changes.\n"
            "Use 'git status --short' and commit/stash/revert first, or pass --allow-dirty only for recovery."
        )

    fetch(repo, branch)
    counts = ahead_behind(repo, branch)
    pulled = False
    ahead: int | None = None
    behind: int | None = None
    if counts:
        ahead, behind = counts
        if ahead and behind:
            raise GitError(f"local and origin/{branch} diverged: ahead={ahead}, behind={behind}")
        if behind:
            if dirty:
                raise SafetyError(
                    f"origin/{branch} is ahead by {behind}, but working tree is dirty; refusing pull."
                )
            pull_ff_only(repo)
            pulled = True
            counts = ahead_behind(repo, branch)
            if counts:
                ahead, behind = counts

    return PrecheckResult(
        repo=repo,
        branch=branch,
        expected_branch=expected_branch,
        dirty=dirty,
        ahead=ahead,
        behind=behind,
        pulled=pulled,
    )
