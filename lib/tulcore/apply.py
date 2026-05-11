"""Safe copy application for manifest packages."""
from __future__ import annotations

import shutil
from pathlib import Path

from .errors import SafetyError
from .manifest import Manifest
from .paths import mkdirp, repo_relative, safe_join


def apply_copy(manifest: Manifest, *, extracted_dir: Path, repo_path: Path, backup_dir: Path, log_path: Path) -> list[str]:
    operations = manifest.apply.get("files") or []
    changed: list[str] = []
    mkdirp(backup_dir)
    logs: list[str] = []
    for item in operations:
        src_rel = str(item["from"])
        dst_rel = str(item["to"])
        src = safe_join(extracted_dir, src_rel)
        dst = safe_join(repo_path, dst_rel)
        if not src.exists():
            raise SafetyError(f"manifest source does not exist: {src_rel}")
        if src.is_dir():
            for child in sorted(p for p in src.rglob("*") if p.is_file()):
                child_rel = child.relative_to(src).as_posix()
                target = safe_join(dst, child_rel)
                _copy_one(child, target, repo_path=repo_path, backup_dir=backup_dir, logs=logs)
                changed.append(repo_relative(repo_path, target))
        else:
            _copy_one(src, dst, repo_path=repo_path, backup_dir=backup_dir, logs=logs)
            changed.append(repo_relative(repo_path, dst))
    log_path.write_text("\n".join(logs) + "\n", encoding="utf-8", newline="\n")
    return sorted(set(changed))


def _copy_one(src: Path, dst: Path, *, repo_path: Path, backup_dir: Path, logs: list[str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        rel = dst.relative_to(repo_path).as_posix()
        backup = backup_dir / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dst, backup)
        logs.append(f"backup {rel} -> {backup}")
    shutil.copy2(src, dst)
    logs.append(f"copy {src} -> {dst}")
