"""Package authoring helpers for tul."""
from __future__ import annotations

import json
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .apply import build_apply_plan
from .config import dump_yaml, load_yaml_file
from .errors import TulError
from .manifest import Manifest, load_manifest, validate_manifest
from .package import manifest_data_from_archive, safe_extract, sha256_file
from .paths import mkdirp, normalize_repo_relative

FORBIDDEN_ARCHIVE_PARTS = {"__pycache__", ".git"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


@dataclass
class PackageCheckResult:
    path: Path
    ok: bool
    checks: list[dict[str, Any]]
    manifest: dict[str, Any]
    sha256: str | None = None
    apply_plan_count: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path),
            "ok": self.ok,
            "sha256": self.sha256,
            "manifest": self.manifest,
            "apply_plan_count": self.apply_plan_count,
            "checks": self.checks,
        }


def _add(checks: list[dict[str, Any]], ok: bool, name: str, detail: str = "") -> None:
    checks.append({"ok": bool(ok), "name": name, "detail": detail})


def _archive_names(path: Path) -> list[str]:
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            return zf.namelist()
    if tarfile.is_tarfile(path):
        with tarfile.open(path) as tf:
            return [member.name for member in tf.getmembers()]
    raise TulError(f"unsupported package archive: {path}")


def _normalize_archive_name(name: str) -> str:
    return name.replace("\\", "/").lstrip("./")


def _has_forbidden_member(names: list[str]) -> list[str]:
    bad: list[str] = []
    for name in names:
        normalized = _normalize_archive_name(name)
        parts = [part for part in normalized.split("/") if part]
        if any(part in FORBIDDEN_ARCHIVE_PARTS for part in parts) or any(normalized.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
            bad.append(normalized)
    return bad


def _nested_archive_members(names: list[str], leaf: str) -> list[str]:
    nested: list[str] = []
    for name in names:
        normalized = _normalize_archive_name(name)
        if normalized != leaf and normalized.endswith(f"/{leaf}"):
            nested.append(normalized)
    return sorted(nested)


def _payload_member_names(names: list[str]) -> list[str]:
    payload: list[str] = []
    for name in names:
        normalized = _normalize_archive_name(name)
        if not normalized.startswith("files/") or normalized.endswith("/"):
            continue
        pseudo = Path(normalized)
        if should_skip_zip_member(pseudo):
            continue
        payload.append(normalized)
    return sorted(set(payload))


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _format_list(items: list[str], *, limit: int = 8) -> str:
    if not items:
        return "ok"
    shown = ", ".join(items[:limit])
    if len(items) > limit:
        shown += f", ... (+{len(items) - limit} more)"
    return shown


def _manifest_consistency_checks(manifest_data: dict[str, Any], payload_files: list[str]) -> list[tuple[bool, str, str]]:
    checks: list[tuple[bool, str, str]] = []
    apply_section = manifest_data.get("apply") or {}
    commit_section = manifest_data.get("commit") or {}
    apply_items = _as_list(apply_section.get("files"))
    raw_commit_files = _as_list(commit_section.get("files"))

    destinations: list[str] = []
    sources: list[str] = []
    malformed: list[str] = []
    source_outside_files: list[str] = []
    for index, item in enumerate(apply_items):
        if not isinstance(item, dict):
            malformed.append(f"apply.files[{index}] is not a mapping")
            continue
        src = str(item.get("from") or "").strip()
        dst = str(item.get("to") or "").strip()
        if not src or not dst:
            malformed.append(f"apply.files[{index}] missing from/to")
            continue
        sources.append(src)
        destinations.append(dst)
        if not src.startswith("files/"):
            source_outside_files.append(src)

    duplicate_destinations = sorted({item for item in destinations if destinations.count(item) > 1})
    commit_files = [str(item).strip() for item in raw_commit_files if str(item).strip()]
    destination_set = set(destinations)
    commit_set = set(commit_files)
    missing_from_commit = sorted(destination_set - commit_set)
    extra_commit_files = sorted(commit_set - destination_set)

    payload_set = set(payload_files)
    source_set = set(sources)
    missing_sources = sorted(source_set - payload_set)
    extra_payload = sorted(payload_set - source_set)

    checks.append((not malformed, "manifest apply item shape", _format_list(malformed)))
    checks.append((not source_outside_files, "apply sources under files/", _format_list(source_outside_files)))
    checks.append((not duplicate_destinations, "unique apply destinations", _format_list(duplicate_destinations)))
    checks.append((not missing_sources, "payload covers apply sources", _format_list(missing_sources)))
    checks.append((not extra_payload, "no unreferenced payload files", _format_list(extra_payload)))
    checks.append((not missing_from_commit and not extra_commit_files, "apply destinations match commit.files", _format_mismatch(missing_from_commit, extra_commit_files)))
    return checks


def _format_mismatch(missing: list[str], extra: list[str]) -> str:
    if not missing and not extra:
        return "ok"
    parts: list[str] = []
    if missing:
        parts.append("missing from commit.files: " + _format_list(missing))
    if extra:
        parts.append("commit.files not produced by apply.files: " + _format_list(extra))
    return "; ".join(parts)


def _next_actions_for_failed_checks(checks: list[dict[str, Any]]) -> list[str]:
    failed = {str(item.get("name") or "") for item in checks if not item.get("ok")}
    actions: list[str] = []
    if "root tul-package.yml" in failed:
        actions.append("Rebuild the zip so tul-package.yml is at archive root, not inside a wrapper directory.")
    if "files/ payload" in failed or "payload covers apply sources" in failed or "no unreferenced payload files" in failed:
        actions.append("Keep package payload files under files/ and make apply.files[*].from list exactly those payload files.")
    if "apply destinations match commit.files" in failed:
        actions.append("Make commit.files exactly match the repo-relative destinations in apply.files[*].to.")
    if "manifest validation" in failed:
        actions.append("Check target.project/repo/branch, apply.mode, non-empty apply.files, and commit.message.")
    if "apply plan" in failed:
        actions.append("Inspect apply.files paths against the target repo; directory copies require allow_directory: true and explicit commit.files coverage.")
    if not actions and failed:
        actions.append("Run tul package inspect <package.zip> and compare tul-package.yml with files/ payload contents.")
    return actions


def check_package_archive(path: Path, *, ctx: Any | None = None) -> PackageCheckResult:
    path = path.expanduser().resolve()
    checks: list[dict[str, Any]] = []
    manifest_data: dict[str, Any] = {}
    digest: str | None = None
    apply_plan_count: int | None = None

    _add(checks, path.exists(), "archive exists", str(path))
    if not path.exists():
        return PackageCheckResult(path=path, ok=False, checks=checks, manifest={})

    try:
        names = _archive_names(path)
        _add(checks, True, "archive readable", f"{len(names)} entries")
    except Exception as exc:
        _add(checks, False, "archive readable", str(exc))
        return PackageCheckResult(path=path, ok=False, checks=checks, manifest={})

    normalized_names = [_normalize_archive_name(name) for name in names]
    name_set = set(normalized_names)
    nested_manifests = _nested_archive_members(names, "tul-package.yml")
    nested_readmes = _nested_archive_members(names, "README.md")
    payload_files = _payload_member_names(names)

    _add(
        checks,
        "tul-package.yml" in name_set,
        "root tul-package.yml",
        "ok" if "tul-package.yml" in name_set else ("nested: " + _format_list(nested_manifests) if nested_manifests else "must be at archive root"),
    )
    _add(
        checks,
        "README.md" in name_set,
        "root README.md",
        "ok" if "README.md" in name_set else ("nested: " + _format_list(nested_readmes) if nested_readmes else "recommended package instructions"),
    )
    _add(checks, bool(payload_files), "files/ payload", f"{len(payload_files)} file(s)" if payload_files else "repo files must live under files/")

    bad = _has_forbidden_member(names)
    _add(checks, not bad, "no generated/cache files", _format_list(bad) if bad else "ok")

    try:
        manifest_data = manifest_data_from_archive(path)
        digest = sha256_file(path)
        _add(checks, True, "manifest parse", str(manifest_data.get("name") or path.stem))
    except Exception as exc:
        _add(checks, False, "manifest parse", str(exc))

    if manifest_data:
        manifest = Manifest(path=Path("tul-package.yml"), data=manifest_data)
        try:
            # Basic validation without target context is still useful.
            if ctx is None:
                project = str((manifest.target or {}).get("project") or "")
                repo = str((manifest.target or {}).get("repo") or "")
                branch = str((manifest.target or {}).get("branch") or "")
            else:
                project = ctx.project_id
                repo = ctx.expected_repo
                branch = ctx.expected_branch
            validate_manifest(manifest, project=project, repo=repo, branch=branch)
            _add(checks, True, "manifest validation", "ok")
        except Exception as exc:
            _add(checks, False, "manifest validation", str(exc))

        for ok, name, detail in _manifest_consistency_checks(manifest_data, payload_files):
            _add(checks, ok, name, detail)

        if ctx is not None:
            try:
                with tempfile.TemporaryDirectory(prefix="tul-package-check-") as tmp:
                    extracted = Path(tmp) / "extracted"
                    safe_extract(path, extracted)
                    extracted_manifest = load_manifest(extracted / "tul-package.yml")
                    plan = build_apply_plan(
                        extracted_manifest,
                        extracted_dir=extracted,
                        repo_path=ctx.repo_path,
                        allowed_files=extracted_manifest.commit_files,
                    )
                    apply_plan_count = len(plan)
                    _add(checks, True, "apply plan", f"{len(plan)} operation(s)")
            except Exception as exc:
                _add(checks, False, "apply plan", str(exc))

    ok = all(item.get("ok") for item in checks)
    return PackageCheckResult(path=path, ok=ok, checks=checks, manifest=manifest_data, sha256=digest, apply_plan_count=apply_plan_count)


def format_package_check(result: PackageCheckResult) -> str:
    lines = ["# tul package check", "", f"Package: {result.path}", f"Result: {'pass' if result.ok else 'fail'}"]
    if result.sha256:
        lines.append(f"Sha256: {result.sha256}")
    manifest = result.manifest or {}
    target = manifest.get("target") or {}
    if manifest:
        lines.append(f"Name: {manifest.get('name') or result.path.stem}")
        lines.append(f"Target: {target.get('project')} {target.get('repo')} {target.get('branch')}")
    if result.apply_plan_count is not None:
        lines.append(f"Apply plan operations: {result.apply_plan_count}")
    failed = [item for item in result.checks if not item.get("ok")]
    if failed:
        lines.append("")
        lines.append("## Failure summary")
        for item in failed:
            lines.append(f"- {item.get('name')}: {str(item.get('detail') or '').strip() or 'failed'}")
        actions = _next_actions_for_failed_checks(result.checks)
        if actions:
            lines.append("")
            lines.append("## Next actions")
            for action in actions:
                lines.append(f"- {action}")
    lines.append("")
    lines.append("## Checks")
    for item in result.checks:
        mark = "PASS" if item.get("ok") else "FAIL"
        lines.append(f"- [{mark}] {item.get('name')}")
        detail = str(item.get("detail") or "").strip()
        if detail:
            lines.append(f"  {detail}")
    return "\n".join(lines)


def scaffold_package_dir(
    name: str,
    *,
    out_dir: Path,
    project: str,
    repo: str,
    branch: str,
    message: str,
    force: bool = False,
) -> Path:
    package_dir = (out_dir.expanduser().resolve() / name) if out_dir.name != name else out_dir.expanduser().resolve()
    if package_dir.exists() and any(package_dir.iterdir()) and not force:
        raise TulError(f"package directory already exists and is not empty: {package_dir}")
    mkdirp(package_dir)
    mkdirp(package_dir / "files")
    manifest = {
        "version": 1,
        "name": name.replace("_", "-"),
        "target": {"project": project, "repo": repo, "branch": branch},
        "apply": {"mode": "copy", "files": []},
        "commit": {"files": [], "message": message},
    }
    (package_dir / "tul-package.yml").write_text(dump_yaml(manifest) + "\n", encoding="utf-8")
    (package_dir / "README.md").write_text(
        f"# {name}\n\n"
        "This is a tul package scaffold.\n\n"
        "Add repo files under `files/`, then edit `tul-package.yml` so `apply.files` and `commit.files` list the exact repo-relative files to update.\n\n"
        "Validate before use:\n\n"
        "```bash\n"
        f"tul package zip {package_dir} --out {package_dir.with_suffix('.zip')}\n"
        f"tul package check {package_dir.with_suffix('.zip')} --target {project}\n"
        "```\n",
        encoding="utf-8",
    )
    (package_dir / "files" / ".gitkeep").write_text("", encoding="utf-8")
    return package_dir


def should_skip_zip_member(path: Path) -> bool:
    parts = set(path.parts)
    if parts & FORBIDDEN_ARCHIVE_PARTS:
        return True
    if path.suffix in FORBIDDEN_SUFFIXES:
        return True
    if path.name in {".DS_Store"}:
        return True
    return False


def zip_package_dir(package_dir: Path, *, out_path: Path | None = None, force: bool = False) -> Path:
    package_dir = package_dir.expanduser().resolve()
    if not package_dir.is_dir():
        raise TulError(f"package directory does not exist: {package_dir}")
    if not (package_dir / "tul-package.yml").exists():
        raise TulError(f"missing root tul-package.yml in package dir: {package_dir}")
    if not (package_dir / "README.md").exists():
        raise TulError(f"missing root README.md in package dir: {package_dir}")
    if not (package_dir / "files").is_dir():
        raise TulError(f"missing files/ payload directory in package dir: {package_dir}")
    out = out_path.expanduser().resolve() if out_path else package_dir.with_suffix(".zip")
    if out.exists() and not force:
        raise TulError(f"output archive already exists: {out}; use --force to replace")
    mkdirp(out.parent)
    tmp = out.with_suffix(out.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(package_dir.rglob("*")):
            if item.is_dir() or should_skip_zip_member(item):
                continue
            arcname = item.relative_to(package_dir).as_posix()
            zf.write(item, arcname)
    tmp.replace(out)
    # Validate root layout after writing; this catches accidental nested dirs
    # without requiring scaffold manifests to be fully populated yet.
    names = _archive_names(out)
    if "tul-package.yml" not in names or "README.md" not in names or not any(name.startswith("files/") for name in names):
        raise TulError(f"created archive has invalid root layout: {out}")
    return out


@dataclass
class PackageAddResult:
    package_dir: Path
    repo_path: Path
    added: list[str]
    manifest_path: Path
    message: str | None = None


def find_git_root(start: Path) -> Path:
    start = start.expanduser().resolve()
    proc = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise TulError(f"could not infer git repo root from {start}; pass --target")
    return Path(proc.stdout.strip()).resolve()


def _load_package_manifest_data(package_dir: Path) -> dict[str, Any]:
    manifest_path = package_dir / "tul-package.yml"
    if not manifest_path.exists():
        raise TulError(f"missing package manifest: {manifest_path}")
    return load_yaml_file(manifest_path, required=True)


def _ensure_manifest_lists(data: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    data.setdefault("version", 1)
    data.setdefault("apply", {})
    data.setdefault("commit", {})
    data["apply"].setdefault("mode", "copy")
    files = data["apply"].setdefault("files", [])
    commit_files = data["commit"].setdefault("files", [])
    if not isinstance(files, list):
        raise TulError("manifest apply.files must be a list")
    if not isinstance(commit_files, list):
        raise TulError("manifest commit.files must be a list")
    return files, commit_files


def add_repo_files_to_package(package_dir: Path, repo_files: list[str], *, repo_path: Path | None = None, message: str | None = None) -> PackageAddResult:
    """Copy repo files into package files/ and update tul-package.yml."""
    package_dir = package_dir.expanduser().resolve()
    if not package_dir.is_dir():
        raise TulError(f"package directory does not exist: {package_dir}")
    repo_root = repo_path.expanduser().resolve() if repo_path else find_git_root(Path.cwd())
    if not (repo_root / ".git").exists():
        raise TulError(f"not a git repo root: {repo_root}")
    manifest_path = package_dir / "tul-package.yml"
    data = _load_package_manifest_data(package_dir)
    apply_files, commit_files = _ensure_manifest_lists(data)
    added: list[str] = []
    for raw in repo_files:
        rel = normalize_repo_relative(raw)
        src = (repo_root / rel).resolve()
        if not src.exists():
            raise TulError(f"repo file does not exist: {rel}")
        if src.is_dir():
            raise TulError(f"directory add is not supported by package add: {rel}")
        dst_rel = f"files/{rel}"
        dst = package_dir / dst_rel
        mkdirp(dst.parent)
        shutil.copy2(src, dst)
        apply_files[:] = [item for item in apply_files if not (isinstance(item, dict) and str(item.get("to")) == rel)]
        apply_files.append({"from": dst_rel, "to": rel})
        if rel not in [str(item) for item in commit_files]:
            commit_files.append(rel)
        added.append(rel)
    if message is not None:
        data.setdefault("commit", {})["message"] = message
    marker = package_dir / "files" / ".gitkeep"
    if marker.exists() and added:
        marker.unlink()
    manifest_path.write_text(dump_yaml(data) + "\n", encoding="utf-8", newline="\n")
    return PackageAddResult(package_dir=package_dir, repo_path=repo_root, added=added, manifest_path=manifest_path, message=message)


def format_package_add(result: PackageAddResult) -> str:
    lines = ["# tul package add", "", f"Package dir: {result.package_dir}", f"Repo: {result.repo_path}", f"Manifest: {result.manifest_path}", "", "## Added files"]
    lines.extend(f"- {item}" for item in result.added) if result.added else lines.append("- none")
    lines.extend(["", "Next:", f"- tul package summary {result.package_dir}", f"- tul package zip {result.package_dir} --force", f"- tul package check {result.package_dir.with_suffix('.zip')}"])
    return "\n".join(lines)


def summarize_package_dir(package_dir: Path) -> dict[str, Any]:
    package_dir = package_dir.expanduser().resolve()
    data = _load_package_manifest_data(package_dir)
    apply_files = ((data.get("apply") or {}).get("files") or [])
    commit_files = ((data.get("commit") or {}).get("files") or [])
    payload_files = []
    files_dir = package_dir / "files"
    if files_dir.exists():
        payload_files = sorted(item.relative_to(package_dir).as_posix() for item in files_dir.rglob("*") if item.is_file() and not should_skip_zip_member(item))
    return {"package_dir": str(package_dir), "name": data.get("name"), "target": data.get("target") or {}, "message": (data.get("commit") or {}).get("message"), "apply_count": len(apply_files) if isinstance(apply_files, list) else 0, "commit_count": len(commit_files) if isinstance(commit_files, list) else 0, "payload_count": len(payload_files), "commit_files": commit_files, "payload_files": payload_files}


def format_package_summary(summary: dict[str, Any]) -> str:
    target = summary.get("target") or {}
    lines = ["# tul package summary", "", f"Package dir: {summary.get('package_dir')}", f"Name: {summary.get('name')}", f"Target: {target.get('project')} {target.get('repo')} {target.get('branch')}", f"Message: {summary.get('message')}", f"Apply files: {summary.get('apply_count')}", f"Commit files: {summary.get('commit_count')}", f"Payload files: {summary.get('payload_count')}", "", "## Commit files"]
    commit_files = summary.get("commit_files") or []
    lines.extend(f"- {item}" for item in commit_files) if commit_files else lines.append("- none")
    return "\n".join(lines)
