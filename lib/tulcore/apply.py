from __future__ import annotations

import shutil
from pathlib import Path

from .manifest import Manifest
from .paths import safe_join


def apply_copy(repo: Path, extract_dir: Path, manifest: Manifest) -> Path:
    import datetime as dt

    backup = repo / f".tul-apply-backup-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    backup.mkdir(parents=True, exist_ok=True)

    for item in manifest.apply_files():
        src = safe_join(extract_dir, item["from"])
        dst = safe_join(repo, item["to"])

        if not src.exists():
            raise FileNotFoundError(src)

        if dst.exists():
            bdst = safe_join(backup, item["to"])
            bdst.parent.mkdir(parents=True, exist_ok=True)
            if dst.is_dir():
                shutil.copytree(dst, bdst, dirs_exist_ok=True)
            else:
                shutil.copy2(dst, bdst)

        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    return backup
