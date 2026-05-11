"""Update state persistence and phase tracking."""
from __future__ import annotations

import json
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


def summarize_state(path: Path, data: dict[str, Any]) -> str:
    lines = [
        f"State file: {path}",
        f"Phase: {data.get('phase', 'unknown')}",
    ]
    for key in ("project", "package_name", "package", "sha256", "commit", "branch", "report", "handoff"):
        if data.get(key):
            lines.append(f"{key.replace('_', ' ').title()}: {data[key]}")
    if data.get("push_verified") is not None:
        lines.append(f"Push verified: {str(data.get('push_verified')).lower()}")
    if data.get("error"):
        lines.extend([
            "",
            "Failure:",
            f"- failed_at: {data.get('failed_at') or 'unknown'}",
            f"- error_type: {data.get('error_type') or 'unknown'}",
            f"- error: {data.get('error')}",
        ])
    return "\n".join(lines)
