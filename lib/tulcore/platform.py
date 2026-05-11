from __future__ import annotations

import os
from pathlib import Path


def is_windows() -> bool:
    return os.name == "nt"


def is_termux() -> bool:
    return Path("/data/data/com.termux/files/home").exists()


def name() -> str:
    if is_windows():
        return "windows"
    if is_termux():
        return "termux"
    return "posix"


def config_path() -> Path:
    if os.environ.get("TUL_CONFIG"):
        return Path(os.environ["TUL_CONFIG"]).expanduser()
    return Path.home() / ".config" / "tul" / "config.yml"


def default_project_root() -> Path:
    if os.environ.get("TUL_PROJECT_ROOT"):
        return Path(os.environ["TUL_PROJECT_ROOT"]).expanduser()
    return Path.home() / "prj"


def default_inbox_roots() -> list[Path]:
    if os.environ.get("TUL_INBOX"):
        return [Path(x).expanduser() for x in os.environ["TUL_INBOX"].split(os.pathsep) if x]
    if is_termux():
        return [
            Path("/sdcard/Download"),
            Path("/sdcard/termux/import"),
            Path("/sdcard/termux/import/tul/inbox"),
        ]
    return [Path.home() / "Downloads"]


def default_work_root() -> Path:
    if os.environ.get("TUL_WORK_ROOT"):
        return Path(os.environ["TUL_WORK_ROOT"]).expanduser()
    if is_termux():
        return Path("/sdcard/termux/import/tul/work")
    return Path.home() / ".cache" / "tul" / "work"


def default_archive_root() -> Path:
    if os.environ.get("TUL_ARCHIVE_ROOT"):
        return Path(os.environ["TUL_ARCHIVE_ROOT"]).expanduser()
    if is_termux():
        return Path("/sdcard/termux/import/tul/archive")
    return Path.home() / ".cache" / "tul" / "archive"


def default_backup_root() -> Path:
    if os.environ.get("TUL_BACKUP_ROOT"):
        return Path(os.environ["TUL_BACKUP_ROOT"]).expanduser()
    return Path.home() / ".cache" / "tul" / "backups"


def default_clipboard_command() -> str | None:
    if is_termux():
        return "termux-clipboard-set"
    if is_windows():
        return "Set-Clipboard"
    return None
