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




def has_commit_state(data: dict[str, Any]) -> bool:
    return bool(data.get("commit"))


def latest_state_with_commit(work_root: Path, *, project: str | None = None) -> tuple[Path, dict[str, Any]] | None:
    """Return newest matching state that contains a commit suitable for rollback.

    Import/no-op/validated states can be newer than the latest published update.
    Rollback should skip those by default so `tul import --latest` does not hide
    the latest rollbackable commit.
    """
    for path, data in iter_states(work_root, project=project):
        if has_commit_state(data):
            return path, data
    return None


def rollbackable_state_hint(work_root: Path, *, project: str | None = None) -> str | None:
    found = latest_state_with_commit(work_root, project=project)
    if not found:
        return None
    path, data = found
    return f"{data.get('commit')} from {path}"



def is_noop_state(data: dict[str, Any]) -> bool:
    return data.get("outcome") == "noop" or data.get("no_op") is True


def is_imported_state(data: dict[str, Any]) -> bool:
    if data.get("commit"):
        return False
    return data.get("outcome") == "imported" or data.get("phase") in {"imported", "validated"}


def is_failed_state(data: dict[str, Any]) -> bool:
    return data.get("phase") == "failed" or bool(data.get("error"))


def archive_selector_label(
    *,
    all_states: bool = False,
    noop: bool = False,
    imported: bool = False,
    failed: bool = False,
) -> str:
    selectors: list[str] = []
    if all_states:
        selectors.append("all")
    if noop:
        selectors.append("noop")
    if imported:
        selectors.append("imported")
    if failed:
        selectors.append("failed")
    return ", ".join(selectors) if selectors else "latest"


def select_archive_states(
    work_root: Path,
    *,
    project: str | None = None,
    all_states: bool = False,
    noop: bool = False,
    imported: bool = False,
    failed: bool = False,
    keep: int = 0,
) -> list[tuple[Path, dict[str, Any]]]:
    states = iter_states(work_root, project=project)
    filter_mode = noop or imported or failed
    if filter_mode:
        selected: list[tuple[Path, dict[str, Any]]] = []
        for path, data in states:
            if noop and is_noop_state(data):
                selected.append((path, data))
                continue
            if imported and is_imported_state(data):
                selected.append((path, data))
                continue
            if failed and is_failed_state(data):
                selected.append((path, data))
                continue
    elif all_states:
        selected = states
    else:
        selected = states[:1]

    if keep > 0:
        selected = selected[keep:]
    return selected


def archive_inventory(
    work_root: Path,
    *,
    project: str | None = None,
) -> dict[str, int]:
    states = iter_states(work_root, project=project)
    return {
        "total": len(states),
        "noop": sum(1 for _, data in states if is_noop_state(data)),
        "imported": sum(1 for _, data in states if is_imported_state(data)),
        "failed": sum(1 for _, data in states if is_failed_state(data)),
        "rollbackable": sum(1 for _, data in states if has_commit_state(data)),
    }


def archive_protected_paths(
    work_root: Path,
    *,
    project: str | None = None,
) -> dict[str, Path]:
    protected: dict[str, Path] = {}
    latest = latest_state(work_root, project=project)
    if latest:
        protected["latest"] = latest[0]
    rollbackable = latest_state_with_commit(work_root, project=project)
    if rollbackable:
        protected["latest_rollbackable"] = rollbackable[0]
    return protected


def archive_states(
    work_root: Path,
    archive_root: Path,
    *,
    project: str | None = None,
    all_states: bool = False,
    noop: bool = False,
    imported: bool = False,
    failed: bool = False,
    keep: int = 0,
    dry_run: bool = False,
) -> list[tuple[Path, Path, dict[str, Any]]]:
    states = select_archive_states(
        work_root,
        project=project,
        all_states=all_states,
        noop=noop,
        imported=imported,
        failed=failed,
        keep=keep,
    )
    protected = set(archive_protected_paths(work_root, project=project).values())
    archived_items: list[tuple[Path, Path, dict[str, Any]]] = []
    for state_path, data in states:
        if state_path in protected:
            continue
        state_dir = state_path.parent
        if not state_dir.exists():
            continue
        archive_root.mkdir(parents=True, exist_ok=True)
        dest = archive_root / state_dir.name
        if dest.exists():
            dest = archive_root / f"{state_dir.name}-archived-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        if dry_run:
            archived_items.append((state_path, dest, data))
            continue
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


def _display(value: Any, default: str = "none") -> str:
    if value is None or value == "":
        return default
    return str(value)


def _push_verified_value(data: dict[str, Any]) -> str:
    if data.get("outcome") == "noop" or data.get("no_op") is True:
        return "not applicable"
    value = data.get("push_verified")
    if value is None:
        return "not applicable"
    return str(bool(value)).lower()


def _canonical_verify_latest_path(
    value: str,
    *,
    project: str | None = None,
    work_root: Path | None = None,
) -> str:
    """Return the current import-root latest path for stale latest references.

    Bundle G moved stable latest verify artifacts from `logs/verify/` to the
    tul import root. A state written during the bootstrap update can still
    contain the former `logs/verify/<project>-vf-latest.md` path. Compact state
    is a decision view, so display the canonical current latest path when the
    stored value is recognizably the stale latest pointer. Timestamped run
    artifacts are preserved as-is.
    """
    if not project or work_root is None:
        return value
    path = Path(value)
    if path.name not in {f"{project}-vf-latest.md", f"{project}-vf-latest.json"}:
        return value
    if path.parent.name == "verify" and path.parent.parent.name == "logs":
        return str(Path(work_root).parent / path.name)
    return value


def _verify_artifact_value(
    data: dict[str, Any],
    *,
    project: str | None = None,
    work_root: Path | None = None,
) -> str | None:
    artifacts = data.get("verify_artifacts")
    if isinstance(artifacts, dict):
        for key in ("latest_markdown", "markdown", "latest_json", "json"):
            if artifacts.get(key):
                return _canonical_verify_latest_path(str(artifacts[key]), project=project, work_root=work_root)
    for key in ("verify", "verify_markdown", "verify_latest_markdown", "latest_verify"):
        if data.get(key):
            return _canonical_verify_latest_path(str(data[key]), project=project, work_root=work_root)
    return None


def _has_legacy_repo_zip_export(data: dict[str, Any]) -> bool:
    """Return true when a state contains the retired repo_zip_export field.

    Stage 6 temporarily surfaced repo zip paths before source/review export
    semantics were settled. A path alone is not valid evidence of a fresh,
    wrapper-free source export, so compact state intentionally suppresses it.
    """
    if isinstance(data.get("repo_zip_export"), dict):
        return True
    return any(data.get(key) for key in ("repo_zip", "repo_zip_path", "latest_repo_zip"))




def _source_bundle_export(data: dict[str, Any]) -> dict[str, Any] | None:
    export = data.get("source_bundle_export")
    if isinstance(export, dict):
        return export
    return None


def _source_bundle_lines(data: dict[str, Any]) -> list[str]:
    export = _source_bundle_export(data)
    if not export:
        return ["- source bundle: explicit source export only"]
    if export.get("ok") is False:
        return [f"- source bundle: failed ({export.get('error') or export.get('error_type') or 'unknown error'})"]
    path = export.get("path") or "unknown"
    lines = [f"- source bundle: {path}"]
    if export.get("sha256"):
        lines.append(f"- source bundle sha256: {export['sha256']}")
    if export.get("payload_sha256"):
        lines.append(f"- source bundle payload sha256: {export['payload_sha256']}")
    if export.get("size_bytes") is not None:
        lines.append(f"- source bundle bytes: {export['size_bytes']}")
    if export.get("file_count") is not None:
        lines.append(f"- source bundle files: {export['file_count']}")
    if export.get("root_layout"):
        lines.append(f"- source bundle root layout: {export['root_layout']}")
    if export.get("rewritten") is not None:
        lines.append(f"- source bundle rewritten: {str(bool(export['rewritten'])).lower()}")
    if export.get("verified_after_replace") is not None:
        lines.append(f"- source bundle verified after replace: {str(bool(export['verified_after_replace'])).lower()}")
    if export.get("target_mtime"):
        lines.append(f"- source bundle mtime: {export['target_mtime']}")
    return lines


def _review_bundle_export(data: dict[str, Any]) -> dict[str, Any] | None:
    export = data.get("review_bundle_export")
    if isinstance(export, dict):
        return export
    return None


def _review_bundle_lines(data: dict[str, Any]) -> list[str]:
    export = _review_bundle_export(data)
    if not export:
        return ["- review bundle: not generated"]
    if export.get("ok") is False:
        return [f"- review bundle: failed ({export.get('error') or export.get('error_type') or 'unknown error'})"]
    path = export.get("path") or "unknown"
    lines = [f"- review bundle: {path}"]
    if export.get("sha256"):
        lines.append(f"- review bundle sha256: {export['sha256']}")
    if export.get("size_bytes") is not None:
        lines.append(f"- review bundle bytes: {export['size_bytes']}")
    if export.get("changed_file_count") is not None:
        lines.append(f"- review bundle changed files: {export['changed_file_count']}")
    if export.get("rewritten") is not None:
        lines.append(f"- review bundle rewritten: {str(bool(export['rewritten'])).lower()}")
    if export.get("verified_after_replace") is not None:
        lines.append(f"- review bundle verified after replace: {str(bool(export['verified_after_replace'])).lower()}")
    if export.get("target_mtime"):
        lines.append(f"- review bundle mtime: {export['target_mtime']}")
    return lines


def summarize_compact_state(
    work_root: Path,
    *,
    project: str,
    rollback_command: str = "tul rollback",
) -> str:
    latest = latest_state(work_root, project=project)
    rollbackable = latest_state_with_commit(work_root, project=project)
    total_states = len(iter_states(work_root, project=project))

    lines = ["# tul state", "", f"Project: {project}"]
    if not latest:
        lines.extend(["", "Latest state:", "- none"])
    else:
        path, data = latest
        lines.extend([
            "",
            "Latest state:",
            f"- phase: {_display(data.get('phase'), 'unknown')}",
            f"- outcome: {_display(data.get('outcome'))}",
            f"- package: {_display(data.get('package_name') or data.get('package'))}",
            f"- commit: {_display(data.get('commit'))}",
            f"- push verified: {_push_verified_value(data)}",
            "",
            "Latest rollbackable:",
        ])
        if rollbackable:
            rollback_path, rollback_data = rollbackable
            lines.extend([
                f"- commit: {_display(rollback_data.get('commit'))}",
                f"- command: {rollback_command}",
            ])
        else:
            lines.extend(["- commit: none", f"- command: {rollback_command}"])
        lines.extend(["", "Artifacts:", f"- state: {path}"])
        for key in ("report", "handoff"):
            if data.get(key):
                lines.append(f"- {key}: {data[key]}")
        verify_artifact = _verify_artifact_value(data, project=project, work_root=work_root)
        if verify_artifact:
            lines.append(f"- verify: {verify_artifact}")
        if _has_legacy_repo_zip_export(data) or _source_bundle_export(data) or _review_bundle_export(data):
            lines.extend(["", "Exports:"])
            if _has_legacy_repo_zip_export(data):
                lines.append("- source bundle: unresolved (legacy repo zip path suppressed)")
            else:
                lines.extend(_source_bundle_lines(data))
            lines.extend(_review_bundle_lines(data))

    lines.extend([
        "",
        "Cleanup:",
        f"- work states: {total_states}",
        "- suggestion: tul archive --noop --dry-run --keep 3",
        "",
        "For full history:",
        "- tul state --all --limit 5",
        "- tul state --json",
    ])
    return "\n".join(lines)


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
    if _has_legacy_repo_zip_export(data):
        lines.append("Source Export: unresolved (legacy repo zip path suppressed)")
    source_export = _source_bundle_export(data)
    if source_export:
        if source_export.get("ok") is False:
            lines.append(f"Source Bundle: failed ({source_export.get('error') or 'unknown error'})")
        elif source_export.get("path"):
            lines.append(f"Source Bundle: {source_export.get('path')}")
    review_export = _review_bundle_export(data)
    if review_export:
        if review_export.get("ok") is False:
            lines.append(f"Review Bundle: failed ({review_export.get('error') or 'unknown error'})")
        elif review_export.get("path"):
            lines.append(f"Review Bundle: {review_export.get('path')}")
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
