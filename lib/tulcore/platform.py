"""Platform detection and platform defaults."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def is_windows() -> bool:
    return os.name == "nt" or sys.platform.startswith("win")


def is_termux() -> bool:
    prefix = os.environ.get("PREFIX", "")
    return "com.termux" in prefix or Path("/data/data/com.termux").exists()


def default_config_path() -> Path:
    override = os.environ.get("TUL_CONFIG")
    if override:
        return Path(os.path.expandvars(os.path.expanduser(override)))
    if is_windows():
        home = Path(os.environ.get("USERPROFILE") or Path.home())
        candidate_home = Path("D:/work/home")
        if candidate_home.exists():
            home = candidate_home
        return home / ".config" / "tul" / "config.yml"
    return Path.home() / ".config" / "tul" / "config.yml"


def default_global_config() -> dict:
    if is_windows():
        return {
            "version": 1,
            "platform": {
                "inbox_roots": [
                    "D:/work/files/downloads",
                    "D:/work/files/downloads/.tul/inbox",
                ],
                "work_root": "D:/work/files/downloads/.tul/work",
                "archive_root": "D:/work/files/downloads/.tul/archive",
                "backup_root": "D:/work/var/backup/tul",
                "clipboard_command": "Set-Clipboard",
            },
            "projects": {},
        }
    if is_termux():
        return {
            "version": 1,
            "platform": {
                "inbox_roots": [
                    "/sdcard/Download",
                    "/sdcard/termux/import",
                    "/sdcard/termux/import/tul/inbox",
                ],
                "work_root": "/sdcard/termux/import/tul/work",
                "archive_root": "/sdcard/termux/import/tul/archive",
                "backup_root": "~/tmp/tul-backups",
                "clipboard_command": "termux-clipboard-set",
            },
            "projects": {},
        }
    return {
        "version": 1,
        "platform": {
            "inbox_roots": [str(Path.home() / "Downloads")],
            "work_root": str(Path.home() / ".cache" / "tul" / "work"),
            "archive_root": str(Path.home() / ".cache" / "tul" / "archive"),
            "backup_root": str(Path.home() / ".cache" / "tul" / "backups"),
        },
        "projects": {},
    }
