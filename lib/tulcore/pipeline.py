from __future__ import annotations

from pathlib import Path

from .apply import apply_copy
from .checks import run_checks
from .config import GlobalConfig, load_global, load_repo, slug_from_remote
from .errors import TulError
from .gitops import (
    branch,
    changed,
    git,
    head,
    push_verify,
    remote_url,
    repo_root,
    staged,
    status,
    sync,
    untracked,
)
from .handoff import UpdateResult, build as build_handoff
from .manifest import validate
from .package import import_package, select
from .report import report_text
from .state import update as state_update, write as state_write
from .sweep import sweep


def resolve(target: str, cfg: GlobalConfig | None = None) -> Path:
    cfg = cfg or load_global()
    p = Path(target).expanduser()
    if target == "." or p.exists():
        return repo_root(p)
    entry = cfg.projects.get(target)
    if isinstance(entry, dict) and entry.get("path"):
        return repo_root(Path(str(entry["path"])).expanduser())
    raise TulError(f"unknown project/path: {target}. Run `tul init {target}` first.")


def project(repo: Path, repo_cfg: dict) -> str:
    return str(repo_cfg.get("name") or repo.name)


def repo_slug(repo: Path, repo_cfg: dict) -> str | None:
    if repo_cfg.get("repo"):
        return str(repo_cfg["repo"])
    url = remote_url(repo)
    return slug_from_remote(url) if url else None


def enforce_branch(repo: Path, repo_cfg: dict) -> None:
    expected = repo_cfg.get("branch")
    if expected and branch(repo) != expected:
        raise TulError(f"branch mismatch: current={branch(repo)}, expected={expected}")


def ensure_allowed(repo: Path, allowed: list[str]) -> None:
    allowed_set = {x.replace("\\", "/") for x in allowed}
    actual = set(changed(repo)) | set(untracked(repo))
    extra = sorted(x for x in actual if x not in allowed_set)
    if extra:
        print("Unexpected changed files:")
        for x in extra:
            print(f"  {x}")
        raise TulError("changed files outside manifest commit.files")


def commit_stage(repo: Path, files: list[str], message: str) -> str:
    ensure_allowed(repo, files)
    git(repo, "add", "--", *files)
    git(repo, "diff", "--cached", "--check")
    st = set(staged(repo))
    extra = sorted(x for x in st if x not in {f.replace("\\", "/") for f in files})
    if extra:
        raise TulError(f"unexpected staged files: {extra}")
    if not st:
        raise TulError("no staged changes to commit")
    git(repo, "commit", "-m", message)
    return head(repo)


def run_update(target: str, package_arg: str, no_commit: bool, no_push: bool) -> None:
    cfg = load_global()
    repo = resolve(target, cfg)
    repo_cfg = load_repo(repo)
    proj = project(repo, repo_cfg)
    enforce_branch(repo, repo_cfg)

    if not status(repo):
        try:
            print(sync(repo))
        except Exception as exc:
            print(f"WARNING: sync precheck skipped: {exc}")
    else:
        print("Pre-sync skipped because working tree is dirty.")

    pkg_path = select(cfg, proj, package_arg)
    imported = import_package(cfg, pkg_path)
    state_update(imported.work_dir, state="imported", project=proj)

    validate(imported.manifest, proj, repo_slug(repo, repo_cfg), branch(repo))
    backup = apply_copy(repo, imported.extract_dir, imported.manifest)
    state_update(imported.work_dir, state="applied", backup=str(backup))

    run_checks(repo, repo_cfg)
    sweep(repo, cfg, proj)
    run_checks(repo, repo_cfg)

    if no_commit:
        result = UpdateResult(mode="post-update", push_verified=False, package=str(imported.source))
        handoff = build_handoff(repo, proj, repo_cfg, result)
        print(handoff)
        state_write(imported.work_dir, "handoff.md", handoff)
        return

    commit_hash = commit_stage(repo, imported.manifest.commit_files(), imported.manifest.message())
    state_update(imported.work_dir, state="committed", commit=commit_hash)

    result = UpdateResult(mode="post-update", commit=commit_hash, push_verified=False, package=str(imported.source))

    if not no_push:
        local, _ = push_verify(repo)
        result.push_verified = True
        result.rollback = f"git revert {local[:7]} && git push origin {branch(repo)}"
        state_update(imported.work_dir, state="verified", remote_head=local)

    rpt = report_text(repo, proj, repo_cfg)
    handoff = build_handoff(repo, proj, repo_cfg, result)
    state_write(imported.work_dir, "report.md", rpt)
    state_write(imported.work_dir, "handoff.md", handoff)

    print("")
    print("Rollback if needed:")
    print(f"  {result.rollback or 'not available because push was skipped'}")
    print("")
    print(handoff)


def run_publish(target: str, files: list[str], message: str, no_push: bool) -> None:
    cfg = load_global()
    repo = resolve(target, cfg)
    repo_cfg = load_repo(repo)
    proj = project(repo, repo_cfg)
    enforce_branch(repo, repo_cfg)
    run_checks(repo, repo_cfg)
    sweep(repo, cfg, proj)
    run_checks(repo, repo_cfg)
    commit_hash = commit_stage(repo, files, message)
    result = UpdateResult(mode="post-update", commit=commit_hash, push_verified=False)
    if not no_push:
        local, _ = push_verify(repo)
        result.push_verified = True
        result.rollback = f"git revert {local[:7]} && git push origin {branch(repo)}"
    print(build_handoff(repo, proj, repo_cfg, result))
