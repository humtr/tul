"""Warning-only export integrity and docs drift helpers.

This module checks whether explicit source/review artifacts still line up with
current repo state. It is intentionally advisory: stale or missing export
artifacts must not change the release gate by themselves.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from .config import ProjectContext, platform_paths
from .gitops import current_branch, head, remote_head
from .review import review_bundle_path
from .source import ROOT_LAYOUT, source_bundle_path
from .state import latest_state


SOURCE_REQUIRED_ENTRIES = {"source-manifest.json", "source-file-list.txt", "source-file-sha256s.txt"}
REVIEW_REQUIRED_ENTRIES = {"export-manifest.json", "state.json", "handoff.md"}
DOC_DRIFT_FILES = (
    "docs/status/current.md",
    "docs/roadmap.md",
    "docs/manifest.md",
)
SOURCE_NOT_IMPLEMENTED_PHRASES = (
    "`tul export source` is not implemented",
    "tul export source` is not implemented",
    "Source export: proposed future tul command",
    "Source export: proposed future command",
    "proposed future tul command and artifact",
)


def export_integrity_data(ctx: ProjectContext) -> dict[str, Any]:
    """Return warning-only source/review export and docs-drift status."""
    latest = _latest_state_entry(ctx)
    state_path = latest[0] if latest else None
    state = latest[1] if latest else {}
    branch = current_branch(ctx.repo_path)
    current_head = _safe_head(ctx.repo_path)
    current_remote = _safe_remote_head(ctx.repo_path, branch)
    source = inspect_source_bundle(ctx, state=state, current_head=current_head)
    review = inspect_review_bundle(ctx, state=state, current_head=current_head)
    docs = docs_drift_warnings(ctx, latest_state_data=state)
    warnings: list[str] = []
    warnings.extend(source.get("warnings") or [])
    warnings.extend(review.get("warnings") or [])
    warnings.extend(docs.get("warnings") or [])
    return {
        "ok": True,
        "kind": "export-integrity",
        "project": ctx.project_id,
        "repo": str(ctx.repo_path),
        "branch": branch,
        "head": current_head,
        "remote_head": current_remote,
        "latest_state": str(state_path) if state_path else None,
        "latest_package": state.get("package_name") or state.get("package"),
        "source_bundle": source,
        "review_bundle": review,
        "docs_drift": docs,
        "warning_count": len(warnings),
        "warnings": warnings,
        "gate_effect": "warning-only",
    }


def format_export_integrity(ctx: ProjectContext) -> str:
    data = export_integrity_data(ctx)
    source = data["source_bundle"]
    review = data["review_bundle"]
    docs = data["docs_drift"]
    lines = [
        "# tul show exports",
        "",
        "Mode: warning-only",
        "Release gate effect: none",
        f"Project: {data['project']}",
        f"Repo: {data['repo']}",
        f"Branch: {data.get('branch') or 'unknown'}",
        f"HEAD: {data.get('head') or 'unknown'}",
        f"Remote HEAD: {data.get('remote_head') or 'unavailable'}",
        f"Latest state: {data.get('latest_state') or 'none'}",
        f"Latest package: {data.get('latest_package') or 'unknown'}",
        "",
        "## Source bundle",
        f"- status: {source.get('status')}",
        f"- path: {source.get('path') or source.get('expected_path') or 'none'}",
    ]
    for key, label in (
        ("sha256", "sha256"),
        ("payload_sha256", "payload sha256"),
        ("manifest_head", "manifest head"),
        ("current_head", "current head"),
        ("root_layout", "root layout"),
        ("file_count", "files"),
    ):
        value = source.get(key)
        if value is not None:
            lines.append(f"- {label}: {value}")
    if source.get("state_sha256_matches_actual") is not None:
        lines.append(f"- state sha256 matches actual: {str(bool(source['state_sha256_matches_actual'])).lower()}")
    lines.extend([
        "",
        "## Review bundle",
        f"- status: {review.get('status')}",
        f"- path: {review.get('path') or review.get('expected_path') or 'none'}",
    ])
    for key, label in (
        ("sha256", "sha256"),
        ("manifest_head", "manifest head"),
        ("current_head", "current head"),
        ("changed_file_count", "changed files"),
    ):
        value = review.get(key)
        if value is not None:
            lines.append(f"- {label}: {value}")
    if review.get("recorded_in_latest_state") is not None:
        lines.append(f"- recorded in latest state: {str(bool(review['recorded_in_latest_state'])).lower()}")
    lines.extend([
        "",
        "## Docs drift",
        f"- status: {docs.get('status')}",
        f"- checked files: {docs.get('checked_file_count')}",
    ])
    warnings = data.get("warnings") or []
    lines.extend(["", "## Warnings"])
    if warnings:
        lines.extend(f"- {item}" for item in warnings)
    else:
        lines.append("- none")
    return "\n".join(lines)


def inspect_source_bundle(ctx: ProjectContext, *, state: dict[str, Any] | None = None, current_head: str | None = None) -> dict[str, Any]:
    state = state or {}
    recorded = state.get("source_bundle_export") if isinstance(state.get("source_bundle_export"), dict) else {}
    recorded_path = recorded.get("path") if isinstance(recorded, dict) else None
    path = Path(str(recorded_path)) if recorded_path else source_bundle_path(ctx)
    result: dict[str, Any] = {
        "kind": "source",
        "expected_path": str(source_bundle_path(ctx)),
        "path": str(path),
        "recorded_in_latest_state": bool(recorded_path),
        "current_head": current_head,
        "status": "not_generated",
        "warnings": [],
    }
    if not path.exists():
        result["warnings"].append(f"source bundle is not generated at {path}")
        return result
    result["exists"] = True
    result["size_bytes"] = path.stat().st_size
    result["sha256"] = _sha256(path)
    if recorded.get("sha256"):
        result["recorded_sha256"] = recorded.get("sha256")
        result["state_sha256_matches_actual"] = recorded.get("sha256") == result["sha256"]
        if not result["state_sha256_matches_actual"]:
            result["warnings"].append("source bundle sha256 differs from the latest state record")
    try:
        with zipfile.ZipFile(path) as z:
            bad = z.testzip()
            if bad:
                result["status"] = "invalid"
                result["warnings"].append(f"source bundle has corrupt member: {bad}")
                return result
            names = set(z.namelist())
            missing = sorted(SOURCE_REQUIRED_ENTRIES - names)
            if missing:
                result["status"] = "invalid"
                result["warnings"].append("source bundle missing required metadata: " + ", ".join(missing))
                return result
            manifest = json.loads(z.read("source-manifest.json").decode("utf-8"))
            result["manifest_head"] = manifest.get("head")
            result["manifest_remote_head"] = manifest.get("remote_head")
            result["root_layout"] = manifest.get("root_layout")
            result["file_count"] = manifest.get("file_count")
            result["payload_sha256"] = manifest.get("payload_sha256")
            result["created_at"] = manifest.get("created_at")
            if manifest.get("root_layout") != ROOT_LAYOUT:
                result["status"] = "invalid"
                result["warnings"].append(f"source bundle root layout is {manifest.get('root_layout')!r}, expected {ROOT_LAYOUT!r}")
                return result
            if current_head and manifest.get("head") and manifest.get("head") != current_head:
                result["status"] = "stale"
                result["warnings"].append(f"source bundle is stale: manifest head {manifest.get('head')} != current HEAD {current_head}")
                return result
            result["status"] = "current"
            return result
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError, KeyError) as exc:
        result["status"] = "invalid"
        result["warnings"].append(f"source bundle cannot be inspected: {type(exc).__name__}: {exc}")
        return result


def inspect_review_bundle(ctx: ProjectContext, *, state: dict[str, Any] | None = None, current_head: str | None = None) -> dict[str, Any]:
    state = state or {}
    recorded = state.get("review_bundle_export") if isinstance(state.get("review_bundle_export"), dict) else {}
    recorded_path = recorded.get("path") if isinstance(recorded, dict) else None
    path = Path(str(recorded_path)) if recorded_path else review_bundle_path(ctx)
    result: dict[str, Any] = {
        "kind": "review",
        "expected_path": str(review_bundle_path(ctx)),
        "path": str(path),
        "recorded_in_latest_state": bool(recorded_path),
        "current_head": current_head,
        "status": "not_generated",
        "warnings": [],
    }
    if not path.exists():
        return result
    result["exists"] = True
    result["size_bytes"] = path.stat().st_size
    result["sha256"] = _sha256(path)
    if not recorded_path:
        result["warnings"].append("review bundle exists but is not recorded in the latest state")
    try:
        with zipfile.ZipFile(path) as z:
            bad = z.testzip()
            if bad:
                result["status"] = "invalid"
                result["warnings"].append(f"review bundle has corrupt member: {bad}")
                return result
            names = set(z.namelist())
            missing = sorted(REVIEW_REQUIRED_ENTRIES - names)
            if missing:
                result["status"] = "invalid"
                result["warnings"].append("review bundle missing required entries: " + ", ".join(missing))
                return result
            manifest = json.loads(z.read("export-manifest.json").decode("utf-8"))
            verify_entry = str(manifest.get("verify_markdown_entry") or "")
            if not verify_entry:
                result["status"] = "invalid"
                result["warnings"].append("review bundle manifest missing verify_markdown_entry")
                return result
            if verify_entry not in names:
                result["status"] = "invalid"
                result["warnings"].append(f"review bundle missing verify markdown entry: {verify_entry}")
                return result
            verify_bytes = z.read(verify_entry)
            verify_sha256 = hashlib.sha256(verify_bytes).hexdigest()
            expected_verify_sha256 = str(manifest.get("verify_markdown_sha256") or "").strip()
            if expected_verify_sha256 and expected_verify_sha256 != verify_sha256:
                result["status"] = "invalid"
                result["warnings"].append("review bundle verify markdown sha256 differs from export manifest")
                return result
            if verify_bytes.startswith(b"missing:"):
                result["warnings"].append(f"review bundle verify markdown entry is a missing-artifact marker: {verify_entry}")
            result["verify_markdown_entry"] = verify_entry
            result["verify_markdown_sha256"] = verify_sha256
            result["verify_markdown_path"] = manifest.get("verify_markdown_path")
            result["runtime_truth"] = manifest.get("runtime_truth")
            result["embedded_runtime_records_role"] = manifest.get("embedded_runtime_records_role")
            result["manifest_head"] = manifest.get("head")
            result["state_commit"] = manifest.get("state_commit")
            result["basis"] = manifest.get("basis")
            result["changed_file_count"] = manifest.get("changed_file_count")
            result["created_at"] = manifest.get("created_at")
            if current_head and manifest.get("head") and manifest.get("head") != current_head:
                result["status"] = "stale"
                result["warnings"].append(f"review bundle is stale: manifest head {manifest.get('head')} != current HEAD {current_head}")
                return result
            result["status"] = "current"
            return result
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError, KeyError) as exc:
        result["status"] = "invalid"
        result["warnings"].append(f"review bundle cannot be inspected: {type(exc).__name__}: {exc}")
        return result


def docs_drift_warnings(ctx: ProjectContext, *, latest_state_data: dict[str, Any] | None = None) -> dict[str, Any]:
    latest_state_data = latest_state_data or {}
    warnings: list[str] = []
    checked = 0
    latest_package = str(latest_state_data.get("package_name") or latest_state_data.get("package") or "").strip()
    for rel in DOC_DRIFT_FILES:
        path = ctx.repo_path / rel
        if not path.exists():
            warnings.append(f"{rel} is missing")
            continue
        checked += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for phrase in SOURCE_NOT_IMPLEMENTED_PHRASES:
            if phrase in text:
                warnings.append(f"{rel} still contains pre-implementation source-export wording: {phrase}")
                break
    status = "warning" if warnings else "clean"
    return {
        "status": status,
        "checked_files": list(DOC_DRIFT_FILES),
        "checked_file_count": checked,
        "latest_package": latest_package or None,
        "warnings": warnings,
    }


def _latest_state_entry(ctx: ProjectContext) -> tuple[Path, dict[str, Any]] | None:
    paths = platform_paths(ctx.global_config)
    work_root = paths.get("work_root")
    if not work_root:
        return None
    return latest_state(Path(work_root), project=ctx.project_id)


def _safe_head(repo: Path) -> str | None:
    try:
        return head(repo)
    except Exception:
        return None


def _safe_remote_head(repo: Path, branch: str | None) -> str | None:
    if not branch:
        return None
    try:
        return remote_head(repo, branch)
    except Exception:
        return None


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
