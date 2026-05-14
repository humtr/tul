"""Post-update export automation helpers.

Post-update exports are a convenience phase after the core update loop has
already committed, pushed, and verified the repo. Export failures are advisory:
they must be recorded clearly but must not change commit/push/rollback facts.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ProjectContext
from .review import export_review_bundle
from .source import export_source_bundle
from .state import write_state


@dataclass
class ExportPhaseItem:
    name: str
    status: str
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    error_type: str | None = None
    reason: str | None = None

    @property
    def ok(self) -> bool:
        return self.status in {"pass", "skipped"}

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "status": self.status,
            "ok": self.ok,
        }
        if self.reason:
            payload["reason"] = self.reason
        if self.error:
            payload["error"] = self.error
        if self.error_type:
            payload["error_type"] = self.error_type
        if self.data:
            payload.update(self.data)
        return payload


@dataclass
class PostUpdateExportResult:
    enabled: bool
    created_at: str
    source: ExportPhaseItem
    review: ExportPhaseItem
    warning_only: bool = True
    release_gate_effect: str = "none"
    snapshot_refreshed: bool | None = None
    side_effect_errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        # Export automation is warning-only. The phase is considered complete
        # when outcomes have been captured, even if one export failed.
        return True

    def warnings(self) -> list[str]:
        warnings: list[str] = []
        for item in (self.source, self.review):
            if item.status == "failed":
                warnings.append(f"{item.name} export failed: {item.error_type or 'Error'}: {item.error or 'unknown error'}")
            elif item.status == "skipped" and item.reason:
                warnings.append(f"{item.name} export skipped: {item.reason}")
        warnings.extend(self.side_effect_errors)
        return warnings

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "warning_only": self.warning_only,
            "release_gate_effect": self.release_gate_effect,
            "source": self.source.to_dict(),
            "review": self.review.to_dict(),
            "snapshot_refreshed": self.snapshot_refreshed,
            "side_effect_errors": list(self.side_effect_errors),
            "warnings": self.warnings(),
        }


def run_post_update_exports(
    ctx: ProjectContext,
    *,
    state_file: Path,
    report_path: Path | None,
    handoff_path: Path | None,
    changed_files: list[str] | None,
    source_enabled: bool = True,
    review_enabled: bool = True,
) -> PostUpdateExportResult:
    """Run optional post-update source/review exports and record the phase.

    The caller should invoke this only after the update state has reached
    handoff-ready. The function catches export errors and records them as
    warning-only outcomes.
    """
    created_at = datetime.now().isoformat(timespec="seconds")
    source_item = _run_source_export(ctx, enabled=source_enabled)
    review_item = _run_review_export(ctx, enabled=review_enabled, changed_files=changed_files or [])
    result = PostUpdateExportResult(
        enabled=True,
        created_at=created_at,
        source=source_item,
        review=review_item,
    )

    # Write aggregate phase data after individual exporters have written their
    # own metadata. This keeps the latest state readable even when one exporter
    # fails after the other succeeds.
    write_state(state_file, post_update_exports=result.to_dict())

    for path in (report_path, handoff_path):
        if path:
            try:
                _write_post_update_export_section(path, result)
            except Exception as exc:  # pragma: no cover - defensive artifact update
                result.side_effect_errors.append(f"{path.name}: {type(exc).__name__}: {exc}")

    try:
        from .verify import refresh_verify_upload_runtime_snapshots

        refreshed = refresh_verify_upload_runtime_snapshots(ctx)
        result.snapshot_refreshed = refreshed
        write_state(state_file, post_update_exports=result.to_dict())
    except Exception as exc:  # pragma: no cover - defensive artifact update
        result.side_effect_errors.append(f"verify-snapshot: {type(exc).__name__}: {exc}")
        write_state(state_file, post_update_exports=result.to_dict())
    return result


def format_post_update_exports(result: PostUpdateExportResult) -> str:
    data = result.to_dict()
    lines = [
        "# tul post-update exports",
        "",
        "Mode: automatic post-update export phase",
        "Release gate effect: none",
        "Failure policy: warning-only",
        f"Created at: {data['created_at']}",
        "",
        "## Source export",
        f"- status: {data['source']['status']}",
    ]
    _append_item_details(lines, data["source"])
    lines.extend(["", "## Review export", f"- status: {data['review']['status']}"])
    _append_item_details(lines, data["review"])
    lines.extend(["", "## Runtime snapshots", f"- refreshed: {str(bool(data.get('snapshot_refreshed'))).lower() if data.get('snapshot_refreshed') is not None else 'unknown'}"])
    warnings = data.get("warnings") or []
    lines.extend(["", "## Warnings"])
    if warnings:
        lines.extend(f"- {item}" for item in warnings)
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def _run_source_export(ctx: ProjectContext, *, enabled: bool) -> ExportPhaseItem:
    if not enabled:
        return ExportPhaseItem("source", "skipped", reason="disabled by update option")
    try:
        result = export_source_bundle(ctx, update_state=True)
        return ExportPhaseItem("source", "pass", data=result.to_dict())
    except Exception as exc:  # pragma: no cover - exercised in user env when export path fails
        return ExportPhaseItem("source", "failed", error=str(exc), error_type=type(exc).__name__)


def _run_review_export(ctx: ProjectContext, *, enabled: bool, changed_files: list[str]) -> ExportPhaseItem:
    if not enabled:
        return ExportPhaseItem("review", "skipped", reason="disabled by update option")
    if not changed_files:
        return ExportPhaseItem("review", "skipped", reason="no changed files recorded for this update")
    try:
        result = export_review_bundle(ctx, update_state=True)
        return ExportPhaseItem("review", "pass", data=result.to_dict())
    except Exception as exc:  # pragma: no cover - exercised in user env when export path fails
        return ExportPhaseItem("review", "failed", error=str(exc), error_type=type(exc).__name__)


def _append_item_details(lines: list[str], item: dict[str, Any]) -> None:
    if item.get("reason"):
        lines.append(f"- reason: {item['reason']}")
    if item.get("path"):
        lines.append(f"- path: {item['path']}")
    for key, label in (
        ("sha256", "sha256"),
        ("payload_sha256", "payload sha256"),
        ("size_bytes", "bytes"),
        ("file_count", "files"),
        ("changed_file_count", "changed files"),
        ("root_layout", "root layout"),
        ("rewritten", "rewritten"),
        ("verified_after_replace", "verified after replace"),
        ("target_mtime", "mtime"),
    ):
        value = item.get(key)
        if value is not None:
            if isinstance(value, bool):
                value = str(value).lower()
            lines.append(f"- {label}: {value}")
    if item.get("error"):
        lines.append(f"- error type: {item.get('error_type') or 'Error'}")
        lines.append(f"- error: {item['error']}")


def _write_post_update_export_section(path: Path, result: PostUpdateExportResult) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    start = "<!-- tul-post-update-exports:start -->"
    end = "<!-- tul-post-update-exports:end -->"
    section = start + "\n" + format_post_update_exports(result).rstrip() + "\n" + end + "\n"
    if start in text and end in text:
        before = text.split(start, 1)[0].rstrip()
        after = text.split(end, 1)[1].lstrip()
        text = before + "\n\n" + section + "\n" + after
    else:
        text = text.rstrip() + "\n\n" + section
    path.write_text(text, encoding="utf-8", newline="\n")


def post_update_exports_json(result: PostUpdateExportResult) -> str:
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False) + "\n"
