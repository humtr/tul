from __future__ import annotations

import shutil
from pathlib import Path

from .config import GlobalConfig


PATTERNS = [
    ".tul-*-backup-*",
    ".tul-apply-backup-*",
    ".tul-loop-runtime-core-backup-*",
    "*.stage*.bak",
    "*_stage*.diff",
]


def sweep(repo: Path, cfg: GlobalConfig, project: str) -> Path | None:
    import datetime as dt

    dest = cfg.backup_root() / project / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    moved = []
    for pat in PATTERNS:
        for item in repo.glob(pat):
            if item.exists():
                dest.mkdir(parents=True, exist_ok=True)
                target = dest / item.name
                shutil.move(str(item), str(target))
                moved.append(target)
    if moved:
        print(f"Moved {len(moved)} artifact(s) to {dest}")
        for item in moved:
            print(f"  {item}")
        return dest
    print("No repo-local tul artifacts to sweep.")
    return None
