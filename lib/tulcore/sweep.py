"""Move repo-local tul backup directories out of the repo."""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from .config import platform_paths
from .paths import mkdirp


def sweep_repo(repo: Path, global_config: dict) -> list[str]:
    paths = platform_paths(global_config)
    backup_root = mkdirp(paths.get("backup_root") or (Path.home() / ".cache" / "tul" / "backups"))
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    moved: list[str] = []
    for item in sorted(repo.glob(".tul-*-backup-*")):
        dest_dir = mkdirp(backup_root / repo.name / stamp)
        dest = dest_dir / item.name
        counter = 1
        while dest.exists():
            dest = dest_dir / f"{item.name}-{counter}"
            counter += 1
        shutil.move(str(item), str(dest))
        moved.append(f"{item} -> {dest}")
    return moved
