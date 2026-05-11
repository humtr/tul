"""Publish policy for tul update.

This module owns explicit staging, commit, push, remote HEAD verification,
and rollback hint generation. Low-level git commands remain in gitops.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .errors import SafetyError
from .gitops import changed_files, commit, diff_check, head, push_verify, stage_files
from .state import set_phase


@dataclass(frozen=True)
class PublishResult:
    commit_hash: str | None
    push_verified: bool
    rollback_command: str | None
    staged_files: list[str]
    no_commit: bool = False
    no_push: bool = False


def verify_changed_files(repo: Path, allowed_files: list[str]) -> list[str]:
    """Return changed files after enforcing manifest commit.files allowlist."""
    allowed = set(allowed_files)
    actual = set(changed_files(repo))
    unexpected = sorted(actual - allowed)
    if unexpected:
        raise SafetyError("changed files outside manifest commit.files:\n" + "\n".join(unexpected))
    return sorted(actual)


def verify_staged_files(repo: Path, allowed_files: list[str]) -> list[str]:
    allowed = set(allowed_files)
    staged = set(changed_files(repo, staged=True))
    unexpected = sorted(staged - allowed)
    if unexpected:
        raise SafetyError("staged files outside manifest commit.files:\n" + "\n".join(unexpected))
    return sorted(staged)


def publish_manifest_changes(
    *,
    repo: Path,
    branch: str,
    files: list[str],
    message: str,
    no_commit: bool = False,
    no_push: bool = False,
    state_file: Path | None = None,
) -> PublishResult:
    """Stage explicit manifest files, commit, and push/verify by default."""
    verify_changed_files(repo, files)
    if no_commit:
        if state_file:
            set_phase(state_file, "checked-no-commit")
        return PublishResult(
            commit_hash=None,
            push_verified=False,
            rollback_command=None,
            staged_files=[],
            no_commit=True,
            no_push=no_push,
        )

    stage_files(repo, files)
    staged = verify_staged_files(repo, files)
    diff_check(repo, staged=True)
    if state_file:
        set_phase(state_file, "staged", staged_files=staged)

    commit_hash = commit(repo, message)
    rollback_command = f"git revert {commit_hash} && git push origin {branch}"
    if state_file:
        set_phase(state_file, "committed", commit=commit_hash, rollback_command=rollback_command)

    push_verified = False
    if no_push:
        if state_file:
            set_phase(state_file, "committed-no-push")
    else:
        local, remote = push_verify(repo, branch)
        push_verified = True
        if state_file:
            set_phase(state_file, "verified", local=local or head(repo), remote=remote, branch=branch)

    return PublishResult(
        commit_hash=commit_hash,
        push_verified=push_verified,
        rollback_command=rollback_command,
        staged_files=staged,
        no_commit=False,
        no_push=no_push,
    )
