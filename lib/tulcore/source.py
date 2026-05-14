"""Explicit source bundle export helpers.

A source export is a tul-generated full source-context artifact for package
creation and code-level diagnosis. It is not release-gate evidence, not a review
bundle, and not backup or rollback authority.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ProjectContext, platform_paths
from .errors import TulError
from .gitops import current_branch, git, head, remote_head, status_porcelain
from .paths import expand_path, mkdirp
from .state import latest_state, write_state
from .upload_aliases import head_alias_path, publish_source_upload_alias, remove_root_latest_artifacts

EXCLUDED_DIR_NAMES = {".git", "__pycache__", ".pytest_cache", "node_modules", "dist", "build"}
EXCLUDED_ROOT_DIR_NAMES = {"logs", "work", "archive"}
EXCLUDED_SUFFIXES = {".pyc", ".zip", ".bak"}
REQUIRED_SOURCE_ENTRIES = (
    "README.md",
    ".tul.yml",
    "bin/tul",
    "lib/tulcore/__init__.py",
    "source-manifest.json",
    "source-file-list.txt",
    "source-file-sha256s.txt",
)
ROOT_LAYOUT = "repo-files-at-zip-root"


@dataclass
class SourceBundleExport:
    path: Path
    sha256: str
    payload_sha256: str
    size_bytes: int
    file_count: int
    created_at: str
    rewritten: bool
    verified_after_replace: bool
    target_mtime: str
    target_mtime_epoch: float
    root_layout: str = ROOT_LAYOUT
    upload_aliases: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": True,
            "kind": "source",
            "path": str(self.path),
            "sha256": self.sha256,
            "payload_sha256": self.payload_sha256,
            "size_bytes": self.size_bytes,
            "file_count": self.file_count,
            "created_at": self.created_at,
            "rewritten": self.rewritten,
            "verified_after_replace": self.verified_after_replace,
            "target_mtime": self.target_mtime,
            "target_mtime_epoch": self.target_mtime_epoch,
            "root_layout": self.root_layout,
            "upload_aliases": self.upload_aliases,
        }


def export_root(ctx: ProjectContext) -> Path:
    platform = ctx.global_config.get("platform") or {}
    if platform.get("source_export_root"):
        return expand_path(str(platform["source_export_root"]))
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if work_root:
        return Path(work_root).parent
    return ctx.repo_path.parent


def source_bundle_path(ctx: ProjectContext) -> Path:
    return head_alias_path(ctx, kind="source", suffix=".zip")


def export_source_bundle(ctx: ProjectContext, *, out_path: Path | None = None, update_state: bool = True) -> SourceBundleExport:
    """Create an explicit full source-context export for the current repo."""
    repo = ctx.repo_path.resolve()
    target = out_path or source_bundle_path(ctx)
    mkdirp(target.parent)
    started_at = datetime.now().isoformat(timespec="seconds")
    started_epoch = time.time()
    tmp = target.with_name(f".{target.name}.{os.getpid()}.{int(started_epoch * 1000)}.tmp")
    if tmp.exists():
        tmp.unlink()

    rel_files = _source_files(repo)
    file_hashes = _file_hashes(repo, rel_files)
    payload_sha = _payload_sha256(file_hashes)
    branch = current_branch(repo)
    remote = remote_head(repo, branch) if branch else None
    dirty = bool(status_porcelain(repo).strip())

    manifest = {
        "kind": "source",
        "project": ctx.project_id,
        "repo": ctx.expected_repo or str(ctx.repo_path),
        "repo_path": str(ctx.repo_path),
        "branch": branch,
        "head": head(repo),
        "remote_head": remote,
        "working_tree": "dirty" if dirty else "clean",
        "created_at": started_at,
        "command": "tul export source",
        "root_layout": ROOT_LAYOUT,
        "file_count": len(rel_files),
        "size_bytes": None,
        "sha256": None,
        "payload_sha256": payload_sha,
        "final_zip_sha256_recorded_externally": True,
        "excluded_dirs": sorted(EXCLUDED_DIR_NAMES | EXCLUDED_ROOT_DIR_NAMES),
        "excluded_suffixes": sorted(EXCLUDED_SUFFIXES),
        "required_entries": list(REQUIRED_SOURCE_ENTRIES),
        "notes": [
            "Archive files are written at repository root, without a wrapper directory.",
            "Final archive sha256 is recorded in command output and state; the zip cannot self-embed its own final sha256 without changing that sha256.",
            "This is source context, not review evidence, release-gate evidence, backup, or rollback authority.",
        ],
    }

    try:
        with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for rel in rel_files:
                z.write(repo / rel, rel)
            _write_text(z, "source-file-list.txt", "\n".join(rel_files) + ("\n" if rel_files else ""))
            _write_text(z, "source-file-sha256s.txt", _format_file_hashes(file_hashes))
            _write_text(z, "source-manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        _verify_source_zip(tmp)
        _replace_source_zip(tmp, target)
        os.utime(target, None)
        _verify_source_zip(target)
        stat = target.stat()
        result = SourceBundleExport(
            path=target,
            sha256=_sha256(target),
            payload_sha256=payload_sha,
            size_bytes=stat.st_size,
            file_count=len(rel_files),
            created_at=started_at,
            rewritten=True,
            verified_after_replace=True,
            target_mtime=datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            target_mtime_epoch=stat.st_mtime,
        )
        result.upload_aliases = publish_source_upload_alias(ctx, target, head=manifest["head"]).to_dict()
        removed_latest = remove_root_latest_artifacts(ctx, kinds=("source",))
        if removed_latest:
            result.upload_aliases["removed_latest"] = removed_latest
    finally:
        if tmp.exists():
            tmp.unlink()

    if update_state:
        state_entry = _latest_state_entry(ctx)
        if state_entry:
            state_path, _ = state_entry
            write_state(state_path, source_bundle_export=result.to_dict())
    return result


def format_source_export(result: SourceBundleExport) -> str:
    lines = [
        "# tul export source",
        "",
        "Source bundle export: PASS",
        "Purpose: explicit full source context for package generation and code-level diagnosis.",
        "Not backup, not review evidence, and not release-gate evidence.",
        f"Path: {result.path}",
        f"SHA256: {result.sha256}",
        f"Payload SHA256: {result.payload_sha256}",
        f"Size bytes: {result.size_bytes}",
        f"Source files: {result.file_count}",
        f"Root layout: {result.root_layout}",
        f"Created at: {result.created_at}",
        f"Rewritten: {str(result.rewritten).lower()}",
        f"Verified after replace: {str(result.verified_after_replace).lower()}",
        f"Target mtime: {result.target_mtime}",
    ]
    aliases = result.upload_aliases or {}
    if aliases.get("root_alias"):
        lines.append(f"Upload alias: {aliases['root_alias']}")
    if aliases.get("dated_alias"):
        lines.append(f"Dated alias: {aliases['dated_alias']}")
    return "\n".join(lines)


def _latest_state_entry(ctx: ProjectContext) -> tuple[Path, dict[str, Any]] | None:
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if not work_root:
        return None
    return latest_state(Path(work_root), project=ctx.project_id)


def _source_files(repo: Path) -> list[str]:
    proc = git(repo, ["ls-files"], check=False)
    if proc.returncode != 0:
        raise TulError("source export requires a git worktree with tracked files")
    rels: list[str] = []
    for raw in proc.stdout.splitlines():
        rel = raw.strip()
        if not rel or _excluded_rel(Path(rel)):
            continue
        path = (repo / rel).resolve()
        if not _inside(repo, path) or not path.is_file() or path.is_symlink():
            continue
        rels.append(rel)
    rels = sorted(set(rels))
    missing = [entry for entry in ("README.md", ".tul.yml", "bin/tul", "lib/tulcore/__init__.py") if entry not in rels]
    if missing:
        raise TulError("source export missing required tracked files: " + ", ".join(missing))
    if any(rel in {"source-manifest.json", "source-file-list.txt", "source-file-sha256s.txt"} for rel in rels):
        raise TulError("source export metadata entry would collide with a tracked repo file")
    return rels


def _excluded_rel(rel: Path) -> bool:
    parts = rel.parts
    if not parts:
        return True
    if rel.suffix in EXCLUDED_SUFFIXES:
        return True
    if parts[0] in EXCLUDED_ROOT_DIR_NAMES:
        return True
    if any(part in EXCLUDED_DIR_NAMES for part in parts):
        return True
    return False


def _file_hashes(repo: Path, rel_files: list[str]) -> list[tuple[str, str, int]]:
    items: list[tuple[str, str, int]] = []
    for rel in rel_files:
        path = repo / rel
        items.append((rel, _sha256(path), path.stat().st_size))
    return items


def _payload_sha256(file_hashes: list[tuple[str, str, int]]) -> str:
    h = hashlib.sha256()
    for rel, digest, size in file_hashes:
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(str(size).encode("ascii"))
        h.update(b"\0")
        h.update(digest.encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def _format_file_hashes(file_hashes: list[tuple[str, str, int]]) -> str:
    return "".join(f"{digest}  {rel}  {size}\n" for rel, digest, size in file_hashes)


def _write_text(z: zipfile.ZipFile, name: str, text: str) -> None:
    info = zipfile.ZipInfo(name)
    info.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(info, text.encode("utf-8"))


def _verify_source_zip(path: Path) -> None:
    if not path.exists() or path.stat().st_size <= 0:
        raise TulError(f"source export missing or empty after write: {path}")
    try:
        with zipfile.ZipFile(path) as z:
            bad = z.testzip()
            if bad:
                raise TulError(f"source export zip corrupt entry: {bad}")
            names = set(z.namelist())
            missing = [entry for entry in REQUIRED_SOURCE_ENTRIES if entry not in names]
            if missing:
                raise TulError("source export missing required entries: " + ", ".join(missing))
            for name in names:
                _validate_entry_name(name)
            manifest = json.loads(z.read("source-manifest.json").decode("utf-8"))
            if manifest.get("kind") != "source":
                raise TulError("source export manifest kind is not source")
            if manifest.get("root_layout") != ROOT_LAYOUT:
                raise TulError("source export manifest root_layout is invalid")
            if not manifest.get("payload_sha256"):
                raise TulError("source export manifest missing payload_sha256")
    except zipfile.BadZipFile as exc:
        raise TulError(f"source export is not a readable zip: {path}") from exc


def _validate_entry_name(name: str) -> None:
    path = Path(name)
    parts = path.parts
    if not parts or name.startswith("/") or ".." in parts:
        raise TulError(f"unsafe source export entry: {name}")
    if parts[0] in EXCLUDED_ROOT_DIR_NAMES:
        raise TulError(f"source export contains runtime root entry: {name}")
    if any(part in EXCLUDED_DIR_NAMES for part in parts):
        raise TulError(f"source export contains excluded directory entry: {name}")
    if Path(name).suffix in EXCLUDED_SUFFIXES:
        raise TulError(f"source export contains excluded file suffix: {name}")


def _replace_source_zip(tmp: Path, target: Path) -> None:
    tmp.replace(target)


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
