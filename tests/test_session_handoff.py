from __future__ import annotations

import hashlib
from datetime import datetime
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT, git

import sys

sys.path.insert(0, str(REPO_ROOT / "lib"))

from tulcore.session_handoff import create_session_handoff  # noqa: E402


class SessionHandoffTest(unittest.TestCase):
    def test_session_handoff_includes_prompt_and_complete_checksums(self) -> None:
        head = git("rev-parse", "HEAD")
        head7 = head[:7]
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            for name in (
                f"tul-source-{head7}.zip",
                f"tul-review-{head7}.zip",
                f"tul-vf-{head7}.md",
            ):
                (root / name).write_text(name + "\n", encoding="utf-8")

            bundle = create_session_handoff(
                repo=REPO_ROOT,
                import_root=root,
                now=datetime(2026, 5, 14, 1, 2, 3),
            )

            names = {path.name for path in bundle.files}
            self.assertIn("new-session-prompt.txt", names)
            self.assertIn("migration-summary.md", names)
            self.assertIn("git-files.txt", names)
            sums = bundle.sha256s.read_text(encoding="utf-8")
            for path in bundle.files:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertIn(f"{digest}  {path}", sums)
            self.assertNotIn("FAILED", sums)


if __name__ == "__main__":
    unittest.main()
