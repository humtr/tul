from __future__ import annotations

from pathlib import Path

from . import platform
from .config import load_global, repo_name_from_slug, save_global, save_repo, slug_from_remote
from .errors import TulError
from .gitops import git, remote_url, repo_root, sync
from .handoff import build


def init_project(target: str, branch: str | None = None, handoff: bool = False) -> None:
    cfg = load_global(create=True)
    raw = Path(target).expanduser()

    if raw.exists():
        repo = repo_root(raw)
    elif "/" in target and not target.startswith((".", "~", "/")):
        name = repo_name_from_slug(target)
        repo = platform.default_project_root() / name
        if not repo.exists():
            repo.parent.mkdir(parents=True, exist_ok=True)
            git_url = f"git@github.com:{target.removesuffix('.git')}.git"
            git(repo.parent, "clone", git_url, str(repo))
        repo = repo_root(repo)
    else:
        entry = cfg.projects.get(target)
        if not entry:
            raise TulError(f"unknown project alias: {target}")
        repo = repo_root(Path(str(entry["path"])).expanduser())

    try:
        print(sync(repo))
    except Exception as exc:
        print(f"WARNING: init sync skipped: {exc}")

    slug = slug_from_remote(remote_url(repo) or "")
    name = repo.name
    cfg.projects.setdefault(name, {})
    cfg.projects[name]["path"] = str(repo)
    save_global(cfg)

    repo_cfg = {
        "version": 1,
        "name": name,
        "repo": slug,
        "branch": branch or __import__("subprocess").check_output(["git", "branch", "--show-current"], cwd=repo, text=True).strip(),
        "track": "loop-runtime",
        "check": {
            "commands": [
                "python -m py_compile bin/tul",
                "python -m py_compile lib/tulcore/*.py",
                "git diff --check",
            ]
        },
    }

    if not (repo / ".tul.yml").exists():
        save_repo(repo, repo_cfg)
        print(f"Created {repo / '.tul.yml'}")
    else:
        print(f"Existing {repo / '.tul.yml'} left in place")

    print(f"Registered project alias: {name} -> {repo}")

    if handoff:
        print(build(repo, name, repo_cfg))
    else:
        print(f"Initial handoff: tul handoff {name}")
