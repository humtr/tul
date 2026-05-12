"""Retired repo zip export helpers.

This module remains for historical compatibility with the Stage 6 source-zip
experiment. It is not wired into the default update loop and does not expose a
current `tul export source` CLI command. Future source-export work should add
explicit provenance, root-layout, and acceptance-gate checks before use.
"""
from __future__ import annotations

import hashlib
import os
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ProjectContext, platform_paths
from .paths import expand_path, mkdirp

EXCLUDED_DIR_NAMES = {".git", "__pycache__", ".pytest_cache", "node_modules", "dist", "build"}
EXCLUDED_ROOT_DIR_NAMES = {"logs", "work", "archive"}
EXCLUDED_SUFFIXES = {".pyc", ".zip", ".bak"}


@dataclass
class RepoZipExport:
    path: Path
    sha256: str
    size_bytes: int
    file_count: int
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": True,
            "path": str(self.path),
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "file_count": self.file_count,
            "created_at": self.created_at,
        }


def repo_zip_root(ctx: ProjectContext) -> Path:
    """Return the legacy directory for the retired repo zip export helper.

    This legacy helper derived the tul import root from `platform.work_root`.
    For the common Termux layout this produces:

    `/sdcard/termux/import/tul/tul-main.zip`
    """
    platform = ctx.global_config.get("platform") or {}
    if platform.get("repo_zip_root"):
        return expand_path(str(platform["repo_zip_root"]))
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if work_root:
        return Path(work_root).parent
    return ctx.repo_path.parent


def repo_zip_path(ctx: ProjectContext) -> Path:
    return repo_zip_root(ctx) / f"{ctx.project_id}-main.zip"


def export_repo_zip(ctx: ProjectContext, *, out_path: Path | None = None) -> RepoZipExport:
    """Write a legacy repo zip export for the current repo.

    This helper is retained but not exposed as a current CLI command. Do not
    treat its output as a tul-proven source export unless a future package adds
    explicit command wiring, provenance, and verification semantics.
    """
    repo = ctx.repo_path.resolve()
    target = out_path or repo_zip_path(ctx)
    mkdirp(target.parent)
    tmp = target.with_suffix(target.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()

    file_count = 0
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for dirpath, dirnames, filenames in os.walk(repo):
            current = Path(dirpath)
            rel_dir = current.relative_to(repo)
            kept_dirs: list[str] = []
            for dirname in dirnames:
                if dirname in EXCLUDED_DIR_NAMES:
                    continue
                if rel_dir == Path(".") and dirname in EXCLUDED_ROOT_DIR_NAMES:
                    continue
                kept_dirs.append(dirname)
            dirnames[:] = kept_dirs

            for filename in sorted(filenames):
                path = current / filename
                if path.is_symlink() or not path.is_file():
                    continue
                rel = path.relative_to(repo)
                if _excluded_file(rel):
                    continue
                archive.write(path, rel.as_posix())
                file_count += 1

    tmp.replace(target)
    digest = _sha256(target)
    return RepoZipExport(
        path=target,
        sha256=digest,
        size_bytes=target.stat().st_size,
        file_count=file_count,
        created_at=datetime.now().isoformat(timespec="seconds"),
    )


def _excluded_file(rel: Path) -> bool:
    if rel.suffix in EXCLUDED_SUFFIXES:
        return True
    parts = rel.parts
    if any(part in EXCLUDED_DIR_NAMES for part in parts[:-1]):
        return True
    if parts and parts[0] in EXCLUDED_ROOT_DIR_NAMES:
        return True
    return False


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
