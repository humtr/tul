#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "lib"))

from tulcore.session_handoff import create_session_handoff  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a complete tul session handoff directory.")
    parser.add_argument("--repo", default=str(REPO), help="repo path; defaults to this checkout")
    parser.add_argument("--import-root", default="/sdcard/termux/import/tul", help="directory containing head-tagged tul artifacts")
    parser.add_argument("--out-dir", help="explicit output directory; defaults to import-root/session-handoff/<stamp>-<head7>")
    args = parser.parse_args()

    bundle = create_session_handoff(
        repo=Path(args.repo),
        import_root=Path(args.import_root),
        out_dir=Path(args.out_dir) if args.out_dir else None,
    )
    print(f"Created session handoff: {bundle.directory}")
    print(f"SHA256SUMS: {bundle.sha256s}")
    for path in bundle.files:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
