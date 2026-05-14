"""Launcher installation and diagnostics for the tul command."""
from __future__ import annotations

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from . import __version__
from .errors import TulError


PATH_PROFILE_LINE = 'export PATH="$HOME/bin:$PATH"'


def backup_path(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return path.with_name(f"{path.name}.bak-{stamp}")


def same_resolved(a: Path | None, b: Path | None) -> bool:
    if not a or not b:
        return False
    try:
        return a.resolve() == b.resolve()
    except Exception:
        return False


def launcher_version_label(path: Path, *, repo_bin: Path | None = None) -> str:
    if repo_bin is not None and same_resolved(path, repo_bin):
        return f"tul {__version__}"
    return "not checked (launcher is stale, copied, or outside target repo)"


def home_bin_dir() -> Path:
    return Path.home() / "bin"


def profile_path() -> Path:
    return Path.home() / ".profile"


def path_contains_home_bin(home_bin: Path | None = None) -> bool:
    target = str(home_bin or home_bin_dir())
    return target in os.environ.get("PATH", "").split(os.pathsep)


def ensure_posix_profile_path(home_bin: Path | None = None) -> list[str]:
    """Ensure future POSIX shells include ~/bin in PATH.

    The current process PATH cannot be changed for the parent shell, so this
    function updates ~/.profile idempotently and returns user-facing notes.
    """
    home_bin = home_bin or home_bin_dir()
    lines: list[str] = []
    if os.name == "nt":
        return lines
    profile = profile_path()
    existing = ""
    if profile.exists():
        existing = profile.read_text(encoding="utf-8", errors="ignore")
    if PATH_PROFILE_LINE not in existing:
        prefix = "" if not existing or existing.endswith("\n") else "\n"
        profile.write_text(existing + prefix + PATH_PROFILE_LINE + "\n", encoding="utf-8")
        lines.append(f"Added PATH line to {profile}: {PATH_PROFILE_LINE}")
    if not path_contains_home_bin(home_bin):
        lines.append('Current shell may need reload: . ~/.profile && hash -r')
    return lines


def path_launcher_info(repo: Path | None = None) -> list[str]:
    found = shutil.which("tul")
    repo_bin = (repo / "bin" / "tul") if repo else None
    lines = ["launcher:"]
    lines.append(f"- PATH tul: {found or 'not found'}")
    if found:
        found_path = Path(found)
        try:
            lines.append(f"- PATH tul resolved: {found_path.resolve()}")
        except Exception:
            lines.append("- PATH tul resolved: unavailable")
        lines.append(f"- PATH tul version: {launcher_version_label(found_path, repo_bin=repo_bin)}")
    if repo_bin:
        lines.append(f"- repo bin/tul: {repo_bin}")
        lines.append(f"- repo bin/tul version: {launcher_version_label(repo_bin, repo_bin=repo_bin)}")
        if found:
            status = "synced" if same_resolved(Path(found), repo_bin) else "stale-or-copy"
            lines.append(f"- launcher status: {status}")
            if status != "synced":
                lines.append("- suggested fix: python3 bin/tul setup install " + str(repo))
        else:
            lines.append("- launcher status: missing")
            lines.append("- suggested fix: python3 bin/tul setup install " + str(repo))
    return lines


def install_launcher(repo: Path, *, copy: bool = False, force: bool = False, update_profile: bool = True) -> str:
    repo = repo.resolve()
    repo_launcher = repo / "bin" / "tul"
    if not repo_launcher.exists():
        raise TulError(f"missing repo launcher: {repo_launcher}")
    home_bin = home_bin_dir()
    home_bin.mkdir(parents=True, exist_ok=True)
    lines = ["# tul setup install", f"Repo: {repo}", f"Repo launcher: {repo_launcher}"]
    if os.name == "nt":
        cmd = home_bin / "tul.cmd"
        content = f'@echo off\r\n"{sys.executable}" "{repo_launcher}" %*\r\n'
        if cmd.exists() and cmd.read_text(encoding="utf-8", errors="ignore") != content:
            if not force:
                lines.append(f"Existing launcher differs: {cmd}")
                lines.append("Re-run with --force to back it up and replace it.")
                return "\n".join(lines)
            backup = backup_path(cmd)
            shutil.move(str(cmd), str(backup))
            lines.append(f"Backed up existing launcher: {backup}")
        cmd.write_text(content, encoding="utf-8")
        lines.append(f"Installed Windows launcher: {cmd}")
        lines.append("Windows PATH is not modified automatically; add the launcher directory if needed.")
        lines.extend(path_launcher_info(repo))
        return "\n".join(lines)

    launcher = home_bin / "tul"
    if launcher.exists() or launcher.is_symlink():
        if launcher.is_symlink() and same_resolved(launcher, repo_launcher):
            lines.append(f"Launcher already synced: {launcher} -> {repo_launcher}")
            if update_profile:
                lines.extend(ensure_posix_profile_path(home_bin))
            lines.extend(path_launcher_info(repo))
            return "\n".join(lines)
        if launcher.is_symlink():
            launcher.unlink()
            lines.append(f"Removed stale symlink launcher: {launcher}")
        else:
            backup = backup_path(launcher)
            shutil.move(str(launcher), str(backup))
            lines.append(f"Backed up existing non-symlink launcher: {backup}")
    if copy:
        shutil.copy2(repo_launcher, launcher)
        lines.append(f"Copied launcher: {launcher}")
    else:
        launcher.symlink_to(repo_launcher)
        lines.append(f"Symlinked launcher: {launcher} -> {repo_launcher}")
    repo_launcher.chmod(repo_launcher.stat().st_mode | 0o755)
    try:
        launcher.chmod(launcher.stat().st_mode | 0o755)
    except Exception:
        pass
    if update_profile:
        lines.extend(ensure_posix_profile_path(home_bin))
    elif not path_contains_home_bin(home_bin):
        lines.append(f"NOTE: add this directory to PATH if needed: {home_bin}")
        lines.append(f"For Termux/bash: {PATH_PROFILE_LINE}")
    lines.extend(path_launcher_info(repo))
    return "\n".join(lines)
