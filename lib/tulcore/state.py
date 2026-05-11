"""Update state persistence and phase tracking."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PHASES = [
    "new",
    "imported",
    "validated",
    "applied",
    "checked",
    "swept",
    "staged",
    "committed",
    "committed-no-push",
    "checked-no-commit",
    "verified",
    "noop",
    "handoff-ready",
    "failed",
    "archived",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"created_at": now_iso(), "phase": "new"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"created_at": now_iso(), "phase": "unknown", "state_parse_error": True, "path": str(path)}
    if isinstance(data, dict):
        return data
    return {"created_at": now_iso(), "phase": "unknown", "state_parse_error": True, "path": str(path)}


def write_state(path: Path, **updates: Any) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    state = read_state(path)
    state.update(updates)
    state.setdefault("created_at", now_iso())
    state["updated_at"] = now_iso()
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return state


def set_phase(path: Path, phase: str, **updates: Any) -> dict[str, Any]:
    if phase not in PHASES:
        raise ValueError(f"unknown state phase: {phase}")
    return write_state(path, phase=phase, **updates)


def record_error(path: Path | None, exc: BaseException, *, failed_at: str | None = None) -> dict[str, Any] | None:
    if path is None:
        return None
    current = read_state(path)
    last_phase = current.get("phase")
    return set_phase(
        path,
        "failed",
        failed_at=failed_at or last_phase,
        last_successful_phase=last_phase,
        error_type=type(exc).__name__,
        error=str(exc),
    )


def find_state_files(work_root: Path) -> list[Path]:
    if not work_root.exists():
        return []
    return sorted(work_root.glob("*/state.json"), key=lambda p: p.stat().st_mtime, reverse=True)


def latest_state(work_root: Path, *, project: str | None = None) -> tuple[Path, dict[str, Any]] | None:
    for path in find_state_files(work_root):
        data = read_state(path)
        if project is None or str(data.get("project") or "") == str(project):
            return path, data
    return None



def iter_states(work_root: Path, *, project: str | None = None) -> list[tuple[Path, dict[str, Any]]]:
    result: list[tuple[Path, dict[str, Any]]] = []
    for path in find_state_files(work_root):
        data = read_state(path)
        if project is None or str(data.get("project") or "") == str(project):
            result.append((path, data))
    return result


def archive_states(
    work_root: Path,
    archive_root: Path,
    *,
    project: str | None = None,
    all_states: bool = False,
) -> list[tuple[Path, Path, dict[str, Any]]]:
    states = iter_states(work_root, project=project)
    if not all_states:
        states = states[:1]
    archived_items: list[tuple[Path, Path, dict[str, Any]]] = []
    for state_path, _data in states:
        state_dir = state_path.parent
        if not state_dir.exists():
            continue
        archive_root.mkdir(parents=True, exist_ok=True)
        dest = archive_root / state_dir.name
        if dest.exists():
            dest = archive_root / f"{state_dir.name}-archived-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.move(str(state_dir), str(dest))
        new_state = dest / "state.json"
        archived = set_phase(
            new_state,
            "archived",
            archived_from=str(state_dir),
            archived_to=str(dest),
        )
        archived_items.append((new_state, dest, archived))
    return archived_items


def state_commit(data: dict[str, Any]) -> str | None:
    value = data.get("commit")
    if value:
        return str(value)
    return None

def archive_latest_state(work_root: Path, archive_root: Path, *, project: str | None = None) -> tuple[Path, Path, dict[str, Any]] | None:
    archived = archive_states(work_root, archive_root, project=project, all_states=False)
    return archived[0] if archived else None


def summarize_state(path: Path, data: dict[str, Any]) -> str:
    lines = [
        f"State file: {path}",
        f"Phase: {data.get('phase', 'unknown')}",
    ]
    if data.get("outcome"):
        lines.append(f"Outcome: {data['outcome']}")
    if data.get("no_op") is not None:
        lines.append(f"No-op: {str(data.get('no_op')).lower()}")
    if data.get("reason"):
        lines.append(f"Reason: {data['reason']}")
    for key in (
        "project",
        "package_name",
        "package",
        "sha256",
        "commit",
        "branch",
        "apply_plan",
        "apply_log",
        "report",
        "handoff",
    ):
        if data.get(key):
            lines.append(f"{key.replace('_', ' ').title()}: {data[key]}")
    if data.get("outcome") == "noop" or data.get("no_op") is True:
        lines.append("Push verified: not applicable for no-op")
    elif data.get("push_verified") is not None:
        lines.append(f"Push verified: {str(data.get('push_verified')).lower()}")
    if data.get("changed_files") is not None:
        files = data.get("changed_files") or []
        lines.extend(["", "Changed files:"])
        if files:
            lines.extend(f"- {item}" for item in files)
        else:
            lines.append("- none")
    if data.get("error"):
        lines.extend([
            "",
            "Failure:",
            f"- failed_at: {data.get('failed_at') or 'unknown'}",
            f"- last_successful_phase: {data.get('last_successful_phase') or 'unknown'}",
            f"- error_type: {data.get('error_type') or 'unknown'}",
            f"- error: {data.get('error')}",
        ])
    if data.get("archived_to"):
        lines.extend(["", "Archive:", f"- archived_to: {data.get('archived_to')}"])
    return "\n".join(lines)
