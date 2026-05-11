"""Update state persistence."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_state(path: Path, **updates: Any) -> dict[str, Any]:
    state = read_state(path)
    state.update(updates)
    state["updated_at"] = now_iso()
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return state


def read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"created_at": now_iso(), "phase": "new"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"created_at": now_iso(), "phase": "unknown", "state_parse_error": True}
