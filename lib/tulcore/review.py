"""Review bundle export helpers."""
from __future__ import annotations

import hashlib
import json
import os
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ProjectContext, platform_paths
from .gitops import git, head, recent_commits, status_porcelain
from .paths import expand_path, mkdirp
from .state import latest_state, write_state

REQUIRED_REVIEW_FILES = ("tul-vf-latest.md", "state.json", "handoff.md")


@dataclass
class ReviewBundleExport:
    path: Path
    sha256: str
    size_bytes: int
    file_count: int
    changed_file_count: int
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": True,
            "kind": "review",
            "path": str(self.path),
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "file_count": self.file_count,
            "changed_file_count": self.changed_file_count,
            "created_at": self.created_at,
        }


def export_root(ctx: ProjectContext) -> Path:
    platform = ctx.global_config.get("platform") or {}
    if platform.get("review_export_root"):
        return expand_path(str(platform["review_export_root"]))
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if work_root:
        return Path(work_root).parent
    return ctx.repo_path.parent


def review_bundle_path(ctx: ProjectContext) -> Path:
    return export_root(ctx) / f"{ctx.project_id}-review-latest.zip"


def latest_verify_markdown(ctx: ProjectContext) -> Path:
    paths = platform_paths(ctx.global_config)
    verify_root = paths.get("verify_log_root") or paths.get("log_root") or (ctx.repo_path.parent / "logs" / "verify")
    latest_root = Path(verify_root).parent.parent if Path(verify_root).name == "verify" else Path(verify_root).parent
    return latest_root / f"{ctx.project_id}-vf-latest.md"


def export_review_bundle(ctx: ProjectContext, *, out_path: Path | None = None, update_state: bool = True) -> ReviewBundleExport:
    repo = ctx.repo_path.resolve()
    target = out_path or review_bundle_path(ctx)
    mkdirp(target.parent)
    tmp = target.with_suffix(target.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()

    state_entry = _latest_state_entry(ctx)
    state_path = state_entry[0] if state_entry else None
    state_data = state_entry[1] if state_entry else {}
    report_path = _path_from_state(repo, state_data.get("report"))
    handoff_path = _path_from_state(repo, state_data.get("handoff"))
    verify_path = latest_verify_markdown(ctx)

    commit = str(state_data.get("commit") or "").strip() or head(repo)
    changed_files = _changed_files_for_review(repo, state_data, commit)
    diff_text = _diff_for_review(repo, commit, changed_files)

    file_count = 0
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        file_count += _write_text(z, "README.md", _review_readme(ctx, commit, changed_files))
        file_count += _write_text(z, "git-head.txt", head(repo) + "\n")
        file_count += _write_text(z, "git-log-latest.txt", "\n".join(recent_commits(repo, count=10)) + "\n")
        file_count += _write_text(z, "working-tree.txt", status_porcelain(repo) or "clean")
        file_count += _write_text(z, "changed-files.txt", "\n".join(changed_files) + ("\n" if changed_files else ""))
        file_count += _write_text(z, "diff.patch", diff_text)

        if verify_path.exists():
            file_count += _write_file(z, verify_path, "tul-vf-latest.md")
        else:
            file_count += _write_text(z, "tul-vf-latest.md", f"missing: {verify_path}\n")
        if state_path and state_path.exists():
            file_count += _write_file(z, state_path, "state.json")
        else:
            file_count += _write_text(z, "state.json", json.dumps({"missing": "latest state"}, indent=2) + "\n")
        if report_path and report_path.exists():
            file_count += _write_file(z, report_path, "report.md")
        else:
            file_count += _write_text(z, "report.md", "missing: latest report\n")
        if handoff_path and handoff_path.exists():
            file_count += _write_file(z, handoff_path, "handoff.md")
        else:
            file_count += _write_text(z, "handoff.md", "missing: latest handoff\n")

        for rel in changed_files:
            src = (repo / rel).resolve()
            if not _inside(repo, src) or not src.is_file() or src.is_symlink():
                continue
            file_count += _write_file(z, src, f"files/{rel}")

    tmp.replace(target)
    result = ReviewBundleExport(
        path=target,
        sha256=_sha256(target),
        size_bytes=target.stat().st_size,
        file_count=file_count,
        changed_file_count=len(changed_files),
        created_at=datetime.now().isoformat(timespec="seconds"),
    )

    if update_state and state_path:
        write_state(state_path, review_bundle_export=result.to_dict())
    return result


def format_review_export(result: ReviewBundleExport) -> str:
    return "\n".join([
        "# tul export review",
        "",
        "Review bundle export: PASS",
        f"Path: {result.path}",
        f"SHA256: {result.sha256}",
        f"Size bytes: {result.size_bytes}",
        f"Files: {result.file_count}",
        f"Changed files: {result.changed_file_count}",
    ])


def _latest_state_entry(ctx: ProjectContext) -> tuple[Path, dict[str, Any]] | None:
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if not work_root:
        return None
    return latest_state(Path(work_root), project=ctx.project_id)


def _path_from_state(repo: Path, value: object) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    if path.is_absolute():
        return path
    return repo / path


def _changed_files_for_review(repo: Path, state: dict[str, Any], commit: str) -> list[str]:
    state_files = state.get("changed_files")
    if isinstance(state_files, list) and state_files:
        return sorted({str(item).strip() for item in state_files if str(item).strip()})
    if commit:
        proc = git(repo, ["diff-tree", "--no-commit-id", "--name-only", "-r", commit], check=False)
        if proc.returncode == 0:
            files = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
            if files:
                return sorted(set(files))
    return []


def _diff_for_review(repo: Path, commit: str, changed_files: list[str]) -> str:
    if not commit:
        return ""
    # `git show` works for normal and merge commits and avoids needing to know
    # the parent hash in shell-independent code. Limit to changed files when
    # available to keep the review bundle small.
    args = ["show", "--format=", "--patch", "--full-index", commit]
    if changed_files:
        args.extend(["--", *changed_files])
    proc = git(repo, args, check=False)
    if proc.returncode == 0:
        return proc.stdout
    return proc.stdout + proc.stderr


def _review_readme(ctx: ProjectContext, commit: str, changed_files: list[str]) -> str:
    return "\n".join([
        "# tul review bundle",
        "",
        "Purpose: transport the latest runtime facts and changed-file evidence to an LLM review session.",
        "This is not a backup and not a canonical source archive.",
        "",
        f"Project: {ctx.project_id}",
        f"Repo: {ctx.repo_path}",
        f"HEAD: {commit}",
        f"Changed files: {len(changed_files)}",
        "",
        "Contents:",
        "- tul-vf-latest.md",
        "- state.json",
        "- report.md",
        "- handoff.md",
        "- git-head.txt",
        "- git-log-latest.txt",
        "- changed-files.txt",
        "- diff.patch",
        "- files/<changed files only>",
        "",
    ])


def _write_text(z: zipfile.ZipFile, name: str, text: str) -> int:
    z.writestr(name, text if text.endswith("\n") else text + "\n")
    return 1


def _write_file(z: zipfile.ZipFile, src: Path, name: str) -> int:
    z.write(src, name)
    return 1


def _inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
