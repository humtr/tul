"""Runtime lock for artifact-writing tul commands."""
from __future__ import annotations

import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from .config import ProjectContext, platform_paths
from .errors import TulError
from .paths import mkdirp


def runtime_lock_path(ctx: ProjectContext) -> Path:
    paths = platform_paths(ctx.global_config)
    work_root = Path(paths.get("work_root") or (ctx.repo_path / ".tul-work"))
    return mkdirp(work_root) / f"{ctx.project_id}.runtime.lock"


@contextmanager
def runtime_lock(ctx: ProjectContext, command: str) -> Iterator[Path]:
    path = runtime_lock_path(ctx)
    payload = {
        "project": ctx.project_id,
        "repo": str(ctx.repo_path),
        "command": command,
        "pid": os.getpid(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise TulError(f"another tul runtime operation is active: {path}") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        yield path
    finally:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
