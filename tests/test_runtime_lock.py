from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

from lib.tulcore.errors import TulError
from lib.tulcore.runtime_lock import runtime_lock, runtime_lock_path


@dataclass
class FakeContext:
    project_id: str
    repo_path: Path
    global_config: dict


class RuntimeLockTest(unittest.TestCase):
    def test_lock_file_blocks_nested_runtime_operation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ctx = FakeContext("tul", root / "repo", {"platform": {"work_root": str(root / "work")}})

            with runtime_lock(ctx, "export") as path:
                self.assertTrue(path.exists())
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual("tul", payload["project"])
                self.assertEqual("export", payload["command"])
                with self.assertRaises(TulError):
                    with runtime_lock(ctx, "verify fresh"):
                        pass

            self.assertFalse(runtime_lock_path(ctx).exists())

    def test_lock_file_is_removed_after_exception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ctx = FakeContext("tul", root / "repo", {"platform": {"work_root": str(root / "work")}})

            with self.assertRaises(RuntimeError):
                with runtime_lock(ctx, "run"):
                    raise RuntimeError("boom")

            self.assertFalse(runtime_lock_path(ctx).exists())


if __name__ == "__main__":
    unittest.main()
