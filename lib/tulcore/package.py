from __future__ import annotations

import hashlib
import json
import shutil
import tarfile
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

from .config import GlobalConfig
from .errors import TulError
from .manifest import Manifest, find, load
from .paths import ensure_inside


@dataclass
class ImportedPackage:
    source: Path
    work_dir: Path
    extract_dir: Path
    sha256: str
    manifest: Manifest


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    if src.name.endswith(".zip"):
        with zipfile.ZipFile(src) as z:
            for info in z.infolist():
                ensure_inside(dest, dest / info.filename)
            z.extractall(dest)
    elif src.name.endswith(".tar.gz") or src.name.endswith(".tgz"):
        with tarfile.open(src) as t:
            for member in t.getmembers():
                ensure_inside(dest, dest / member.name)
            t.extractall(dest)
    else:
        raise TulError(f"unsupported package type: {src}")


def candidates(cfg: GlobalConfig) -> list[Path]:
    out = []
    for root in cfg.inbox_roots():
        if root.exists():
            for pat in ("*.zip", "*.tar.gz", "*.tgz"):
                out.extend(root.glob(pat))
    return sorted(set(out), key=lambda p: p.stat().st_mtime, reverse=True)


def manifest_from_archive(path: Path) -> Manifest | None:
    with tempfile.TemporaryDirectory(prefix="tul-manifest-") as tmp:
        root = Path(tmp)
        try:
            safe_extract(path, root)
        except Exception:
            return None
        m = find(root)
        return load(m) if m else None


def select(cfg: GlobalConfig, project: str | None, package_arg: str = "latest") -> Path:
    if package_arg != "latest":
        p = Path(package_arg).expanduser()
        if not p.exists():
            raise TulError(f"package not found: {p}")
        return p

    scored = []
    for p in candidates(cfg):
        m = manifest_from_archive(p)
        score = 0
        if m:
            score += 10
            if project and m.target_project() == project:
                score += 100
        scored.append((score, p.stat().st_mtime, p))

    if not scored:
        raise TulError("no package candidates found")

    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    best_score = scored[0][0]
    best = [p for score, _, p in scored if score == best_score]
    if len(best) == 1:
        return best[0]

    print("Package candidates:")
    for i, p in enumerate(best, 1):
        print(f"{i}. {p}")
    choice = input("Select package [1]: ").strip() or "1"
    return best[int(choice) - 1]


def import_package(cfg: GlobalConfig, source: Path) -> ImportedPackage:
    import datetime as dt

    safe = "".join(ch if ch.isalnum() or ch in "-_." else "-" for ch in source.stem)
    work = cfg.work_root() / f"{safe}-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    extract = work / "extracted"
    work.mkdir(parents=True, exist_ok=True)

    copied = work / source.name
    shutil.copy2(source, copied)
    digest = sha256(copied)
    safe_extract(copied, extract)

    mf = find(extract)
    if not mf:
        raise TulError("tul-package.yml not found in package")
    manifest = load(mf)

    (work / "state.json").write_text(json.dumps({
        "source": str(source),
        "copied": str(copied),
        "sha256": digest,
        "extract_dir": str(extract),
        "state": "extracted",
    }, indent=2), encoding="utf-8")

    return ImportedPackage(copied, work, extract, digest, manifest)
