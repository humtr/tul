from __future__ import annotations

from pathlib import Path

from .errors import TulError


def repo_rel(path: str) -> str:
    text = path.replace("\\", "/")
    p = Path(text)
    if p.is_absolute():
        raise TulError(f"absolute path forbidden: {path}")
    parts = [x for x in text.split("/") if x not in ("", ".")]
    if any(x == ".." for x in parts):
        raise TulError(f"path traversal forbidden: {path}")
    return "/".join(parts)


def safe_join(root: Path, rel: str) -> Path:
    clean = repo_rel(rel)
    target = (root / clean).resolve()
    root_resolved = root.resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise TulError(f"path escapes root: {rel}") from exc
    return target


def ensure_inside(root: Path, target: Path) -> Path:
    resolved = target.resolve()
    root_resolved = root.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise TulError(f"path escapes root: {target}") from exc
    return resolved
