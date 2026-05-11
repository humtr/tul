from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def update(work_dir: Path | None, **items: Any) -> None:
    if not work_dir:
        return
    path = work_dir / "state.json"
    data = {}
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    data.update(items)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write(work_dir: Path | None, name: str, text: str) -> None:
    if not work_dir:
        return
    (work_dir / name).write_text(text, encoding="utf-8", newline="\n")
