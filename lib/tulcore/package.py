"""Package discovery, import, and safe extraction."""
from __future__ import annotations

import hashlib
import shutil
import tarfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import platform_paths
from .errors import PackageError, SafetyError
from .manifest import Manifest, load_manifest
from .paths import ensure_inside, mkdirp, safe_join


@dataclass
class PackageCandidate:
    source: Path
    manifest_data: dict
    mtime: float

    @property
    def name(self) -> str:
        return str(self.manifest_data.get("name") or self.source.stem)


@dataclass
class ImportedPackage:
    source: Path
    work_dir: Path
    extracted_dir: Path
    manifest: Manifest
    sha256: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _manifest_from_archive(path: Path) -> dict | None:
    try:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as zf:
                try:
                    raw = zf.read("tul-package.yml").decode("utf-8")
                except KeyError:
                    return None
        elif tarfile.is_tarfile(path):
            with tarfile.open(path) as tf:
                member = tf.getmember("tul-package.yml")
                extracted = tf.extractfile(member)
                if extracted is None:
                    return None
                raw = extracted.read().decode("utf-8")
        else:
            return None
    except Exception:
        return None
    from .config import load_yaml_text

    try:
        return load_yaml_text(raw)
    except Exception:
        return None



def manifest_data_from_archive(path: Path) -> dict:
    """Read tul-package.yml from an archive without extracting it."""
    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise PackageError(f"package does not exist: {path}")
    data = _manifest_from_archive(path)
    if data is None:
        raise PackageError(f"package has no readable root tul-package.yml: {path}")
    return data


def candidate_record(candidate: PackageCandidate) -> dict:
    """Return a stable, machine-readable summary for package discovery output."""
    target = candidate.manifest_data.get("target") or {}
    commit = candidate.manifest_data.get("commit") or {}
    try:
        size = candidate.source.stat().st_size
    except OSError:
        size = None
    return {
        "path": str(candidate.source),
        "name": candidate.name,
        "mtime": datetime.fromtimestamp(candidate.mtime).astimezone().isoformat(timespec="seconds"),
        "mtime_epoch": candidate.mtime,
        "size": size,
        "target": {
            "project": target.get("project"),
            "repo": target.get("repo"),
            "branch": target.get("branch"),
        },
        "commit": {
            "message": commit.get("message"),
            "files": commit.get("files") or [],
        },
    }

def discover_candidates(global_config: dict, *, project: str, repo: str | None, branch: str | None) -> list[PackageCandidate]:
    paths = platform_paths(global_config)
    candidates: list[PackageCandidate] = []
    for root in paths.get("inbox_roots") or []:
        if not root.exists() or not root.is_dir():
            continue
        for path in sorted(root.glob("*")):
            if path.suffix.lower() != ".zip" and not path.name.lower().endswith(".tar.gz"):
                continue
            data = _manifest_from_archive(path)
            if not data:
                continue
            target = data.get("target") or {}
            if str(target.get("project")) != str(project):
                continue
            if repo and str(target.get("repo")) != str(repo):
                continue
            if branch and str(target.get("branch")) != str(branch):
                continue
            candidates.append(PackageCandidate(source=path, manifest_data=data, mtime=path.stat().st_mtime))
    return sorted(candidates, key=lambda item: item.mtime, reverse=True)


def select_package(global_config: dict, *, explicit: str | None, project: str, repo: str | None, branch: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.exists():
            raise PackageError(f"package does not exist: {path}")
        return path
    candidates = discover_candidates(global_config, project=project, repo=repo, branch=branch)
    if not candidates:
        roots = platform_paths(global_config).get("inbox_roots") or []
        root_list = "\n".join(f"- {root}" for root in roots)
        raise PackageError(f"no matching package found in inbox roots:\n{root_list}")
    return candidates[0].source


def import_package(source: Path, global_config: dict) -> ImportedPackage:
    paths = platform_paths(global_config)
    work_root = mkdirp(paths.get("work_root") or (Path.home() / ".cache" / "tul" / "work"))
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    package_id = f"{source.stem}-{stamp}"
    work_dir = mkdirp(work_root / package_id)
    copied = work_dir / source.name
    shutil.copy2(source, copied)
    digest = sha256_file(copied)
    (work_dir / "source.sha256").write_text(digest + "  " + copied.name + "\n", encoding="utf-8")
    extracted = mkdirp(work_dir / "extracted")
    safe_extract(copied, extracted)
    manifest = load_manifest(extracted / "tul-package.yml")
    return ImportedPackage(source=copied, work_dir=work_dir, extracted_dir=extracted, manifest=manifest, sha256=digest)


def safe_extract(archive: Path, dest: Path) -> None:
    dest = dest.resolve()
    mkdirp(dest)
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zf:
            for member in zf.infolist():
                _validate_archive_member(dest, member.filename)
            zf.extractall(dest)
        return
    if tarfile.is_tarfile(archive):
        with tarfile.open(archive) as tf:
            for member in tf.getmembers():
                _validate_archive_member(dest, member.name)
            tf.extractall(dest)
        return
    raise PackageError(f"unsupported package archive: {archive}")


def _validate_archive_member(dest: Path, name: str) -> None:
    raw = name.replace("\\", "/")
    if raw.startswith("/") or raw.startswith("~/") or (len(raw) >= 2 and raw[1] == ":"):
        raise SafetyError(f"archive member uses absolute path: {name}")
    candidate = safe_join(dest, raw)
    ensure_inside(dest, candidate)
