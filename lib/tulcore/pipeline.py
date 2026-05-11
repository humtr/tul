"""Full update pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .apply import apply_copy
from .checks import run_checks
from .config import ProjectContext, platform_paths
from .errors import CheckError, GitError, ManifestError, PackageError, SafetyError, TulError
from .gitops import (
    ahead_behind,
    changed_files,
    commit,
    current_branch,
    diff_check,
    fetch,
    head,
    is_dirty,
    pull_ff_only,
    push_verify,
    stage_files,
)
from .handoff import generate_handoff
from .manifest import validate_manifest
from .package import import_package, select_package
from .paths import mkdirp
from .report import build_report, write_report
from .state import write_state
from .sweep import sweep_repo


@dataclass
class UpdateResult:
    report: str
    handoff: str
    work_dir: Path
    commit_hash: str | None
    push_verified: bool


def run_update(
    ctx: ProjectContext,
    *,
    package_path: str | None = None,
    no_commit: bool = False,
    no_push: bool = False,
    allow_dirty: bool = False,
) -> UpdateResult:
    repo = ctx.repo_path
    branch = current_branch(repo)
    expected_branch = ctx.expected_branch
    if expected_branch and branch != expected_branch:
        raise SafetyError(f"branch mismatch: expected {expected_branch}, current {branch}")

    if is_dirty(repo) and not allow_dirty:
        raise SafetyError(
            "working tree is dirty; refusing to apply a package over uncommitted changes.\n"
            "Use 'git status --short' and commit/stash/revert first, or pass --allow-dirty only for recovery."
        )

    if not is_dirty(repo):
        fetch(repo, branch)
        counts = ahead_behind(repo, branch)
        if counts:
            ahead, behind = counts
            if ahead and behind:
                raise GitError(f"local and origin/{branch} diverged: ahead={ahead}, behind={behind}")
            if behind:
                pull_ff_only(repo)

    source = select_package(
        ctx.global_config,
        explicit=package_path,
        project=ctx.project_id,
        repo=ctx.expected_repo,
        branch=expected_branch or branch,
    )
    imported = import_package(source, ctx.global_config)
    state_file = imported.work_dir / "state.json"
    write_state(state_file, phase="imported", package=str(source), sha256=imported.sha256)

    validate_manifest(imported.manifest, project=ctx.project_id, repo=ctx.expected_repo, branch=expected_branch or branch)
    write_state(state_file, phase="validated", manifest=imported.manifest.data)

    backup_dir = imported.work_dir / "backups"
    applied_files = apply_copy(
        imported.manifest,
        extracted_dir=imported.extracted_dir,
        repo_path=repo,
        backup_dir=backup_dir,
        log_path=imported.work_dir / "apply.log",
    )
    write_state(state_file, phase="applied", applied_files=applied_files)

    checks = run_checks(repo, ctx.repo_config, log_path=imported.work_dir / "check.log")
    write_state(state_file, phase="checked")

    moved = sweep_repo(repo, ctx.global_config)
    write_state(state_file, phase="swept", swept=moved)

    allowed = set(imported.manifest.commit_files)
    actual = set(changed_files(repo))
    unexpected = sorted(actual - allowed)
    if unexpected:
        raise SafetyError("changed files outside manifest commit.files:\n" + "\n".join(unexpected))

    commit_hash: str | None = None
    push_verified = False
    rollback_command: str | None = None
    if no_commit:
        write_state(state_file, phase="checked-no-commit")
    else:
        stage_files(repo, imported.manifest.commit_files)
        staged = set(changed_files(repo, staged=True))
        unexpected_staged = sorted(staged - allowed)
        if unexpected_staged:
            raise SafetyError("staged files outside manifest commit.files:\n" + "\n".join(unexpected_staged))
        diff_check(repo, staged=True)
        write_state(state_file, phase="staged", staged_files=sorted(staged))
        commit_hash = commit(repo, imported.manifest.commit_message)
        write_state(state_file, phase="committed", commit=commit_hash)
        rollback_command = f"git revert {commit_hash} && git push origin {branch}"
        if no_push:
            write_state(state_file, phase="committed-no-push")
        else:
            push_verify(repo, branch)
            push_verified = True
            write_state(state_file, phase="verified", local=head(repo), branch=branch)

    report = build_report(
        repo=repo,
        project=ctx.project_id,
        package_name=imported.manifest.name,
        commit_hash=commit_hash,
        push_verified=push_verified if commit_hash and not no_push else None,
        rollback_command=rollback_command,
        changed_files=imported.manifest.commit_files,
        checks=checks,
    )
    write_report(imported.work_dir / "report.md", report)
    handoff = generate_handoff(
        repo=repo,
        project=ctx.project_id,
        mode="post-update" if commit_hash else "update-no-commit",
        expected_repo=ctx.expected_repo,
        package_name=imported.manifest.name,
        commit_hash=commit_hash,
        push_verified=push_verified if commit_hash and not no_push else None,
        changed_files=imported.manifest.commit_files,
        validation=checks,
        rollback_command=rollback_command,
        state_file=state_file,
    )
    (imported.work_dir / "handoff.md").write_text(handoff, encoding="utf-8", newline="\n")
    write_state(state_file, phase="handoff-ready", report=str(imported.work_dir / "report.md"), handoff=str(imported.work_dir / "handoff.md"))
    return UpdateResult(report=report, handoff=handoff, work_dir=imported.work_dir, commit_hash=commit_hash, push_verified=push_verified)
