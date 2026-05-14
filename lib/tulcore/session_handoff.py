"""Complete session handoff bundle creation."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


HANDOFF_FILE_ORDER = (
    "git-files.txt",
    "migration-summary.md",
    "new-session-prompt.txt",
)


@dataclass
class SessionHandoffBundle:
    directory: Path
    files: list[Path]
    sha256s: Path


def create_session_handoff(
    *,
    repo: Path,
    import_root: Path,
    out_dir: Path | None = None,
    prompt_text: str | None = None,
    now: datetime | None = None,
) -> SessionHandoffBundle:
    repo = repo.expanduser().resolve()
    import_root = import_root.expanduser().resolve()
    head = _git(repo, "rev-parse", "HEAD")
    head7 = head[:7]
    stamp = (now or datetime.now()).strftime("%y%m%d-%H%M%S")
    target_dir = (out_dir.expanduser().resolve() if out_dir else import_root / "session-handoff" / f"{stamp}-{head7}")
    target_dir.mkdir(parents=True, exist_ok=False)

    artifact_names = [
        f"tul-source-{head7}.zip",
        f"tul-review-{head7}.zip",
        f"tul-vf-{head7}.md",
    ]
    files: list[Path] = []
    for name in artifact_names:
        src = import_root / name
        if not src.exists():
            raise FileNotFoundError(f"missing handoff artifact: {src}")
        dst = target_dir / name
        shutil.copy2(src, dst)
        files.append(dst)

    generated = {
        "git-files.txt": _git(repo, "ls-files") + "\n",
        "migration-summary.md": _migration_summary(repo=repo, head=head, head7=head7, artifact_names=artifact_names),
        "new-session-prompt.txt": prompt_text or _new_session_prompt(head=head, head7=head7, artifact_names=artifact_names),
    }
    for name in HANDOFF_FILE_ORDER:
        path = target_dir / name
        path.write_text(generated[name], encoding="utf-8", newline="\n")
        files.append(path)

    sums = target_dir / "SHA256SUMS.txt"
    sums.write_text("".join(f"{_sha256(path)}  {path}\n" for path in files), encoding="utf-8", newline="\n")
    return SessionHandoffBundle(directory=target_dir, files=files, sha256s=sums)


def _migration_summary(*, repo: Path, head: str, head7: str, artifact_names: list[str]) -> str:
    branch = _git(repo, "branch", "--show-current")
    remote = _git(repo, "rev-parse", f"origin/{branch}") if branch else "unknown"
    return "\n".join([
        "# tul migration summary",
        "",
        "## Baseline",
        "",
        "- Project: tul",
        f"- Repo: {repo}",
        f"- Branch: {branch or 'unknown'}",
        f"- HEAD: {head}",
        f"- Remote HEAD: {remote}",
        "- Artifact policy: head-tagged artifacts are canonical; root latest artifacts are not canonical.",
        "",
        "## Files to upload to the new session",
        "",
        *(f"- {name}" for name in artifact_names),
        "- migration-summary.md",
        "- git-files.txt",
        "- new-session-prompt.txt",
        "- SHA256SUMS.txt",
        "",
        "## Current status",
        "",
        f"This handoff was generated for `{head7}`. Verify with `SHA256SUMS.txt` before using the files.",
        "",
    ])


def _new_session_prompt(*, head: str, head7: str, artifact_names: list[str]) -> str:
    return "\n".join([
        "# tul new session prompt",
        "",
        "Use the attached head-tagged artifacts as the current runtime and source context.",
        "",
        "## Required attachments",
        "",
        *(f"- {name}" for name in artifact_names),
        "- migration-summary.md",
        "- git-files.txt",
        "- new-session-prompt.txt",
        "- SHA256SUMS.txt",
        "",
        "## Starting facts",
        "",
        f"- HEAD: {head}",
        f"- Short HEAD: {head7}",
        "- Treat `tul-vf-<head7>.md` as runtime verification evidence.",
        "- Treat `tul-source-<head7>.zip` as source-context transport.",
        "- Treat `tul-review-<head7>.zip` as changed-file review transport.",
        "- Treat repo docs as durable guidance, not runtime logs.",
        "",
    ])


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
