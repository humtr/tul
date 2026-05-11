"""Path helpers and safety checks."""
from __future__ import annotations

import os
from pathlib import Path, PurePosixPath, PureWindowsPath

from .errors import SafetyError


def expand_path(value: str | os.PathLike[str]) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(str(value))))


def mkdirp(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_absolute_or_drive_path(value: str) -> bool:
    text = str(value).replace("\\", "/")
    return (
        Path(value).is_absolute()
        or PureWindowsPath(value).is_absolute()
        or text.startswith("/")
        or text.startswith("~/")
        or (len(text) >= 2 and text[1] == ":")
    )


def normalize_repo_relative(value: str) -> str:
    if not value or str(value).strip() == "":
        raise SafetyError("empty relative path is not allowed")
    raw = str(value).replace("\\", "/")
    if is_absolute_or_drive_path(raw):
        raise SafetyError(f"absolute destination paths are forbidden: {value}")
    pure = PurePosixPath(raw)
    if any(part in ("", ".", "..") for part in pure.parts):
        if ".." in pure.parts:
            raise SafetyError(f"path traversal is forbidden: {value}")
        # Ignore benign '.' by normalizing through PurePosixPath.
    normalized = str(pure)
    if normalized == "." or normalized.startswith("../") or "/../" in normalized:
        raise SafetyError(f"path traversal is forbidden: {value}")
    return normalized


def safe_join(base: Path, relative: str) -> Path:
    rel = normalize_repo_relative(relative)
    candidate = (base / rel).resolve()
    ensure_inside(base, candidate)
    return candidate


def ensure_inside(base: Path, candidate: Path) -> None:
    base_resolved = base.resolve()
    candidate_resolved = candidate.resolve()
    try:
        common = os.path.commonpath([str(base_resolved), str(candidate_resolved)])
    except ValueError as exc:
        raise SafetyError(f"path escapes base: {candidate}") from exc
    if common != str(base_resolved):
        raise SafetyError(f"path escapes base: {candidate}")


def repo_relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()
