from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

from lib.tulcore.upload_aliases import publish_source_upload_alias, publish_verify_upload_alias


@dataclass
class FakeContext:
    project_id: str
    repo_path: Path
    global_config: dict


class UploadAliasTest(unittest.TestCase):
    def test_source_alias_prunes_old_root_aliases_and_removes_latest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            work = root / "import" / "tul" / "work"
            work.mkdir(parents=True)
            ctx = FakeContext("tul", repo, {"platform": {"work_root": str(work)}})
            source = root / "tul-source-latest.zip"
            source.write_bytes(b"source")
            import_root = work.parent
            (import_root / "tul-source-abcdef0.zip").write_bytes(b"old")
            (import_root / "tul-source-latest.zip").write_bytes(b"latest")

            result = publish_source_upload_alias(ctx, source, head="1234567890abcdef", now=datetime(2026, 5, 14, 1, 2, 3))

            self.assertTrue(Path(result.root_alias).exists())
            self.assertEqual(Path(result.root_alias).name, "tul-source-1234567.zip")
            self.assertTrue(Path(result.dated_alias).exists())
            self.assertFalse((import_root / "tul-source-abcdef0.zip").exists())
            removed = __import__("lib.tulcore.upload_aliases", fromlist=["remove_root_latest_artifacts"]).remove_root_latest_artifacts(ctx, kinds=("source",))
            self.assertIn(str(import_root / "tul-source-latest.zip"), removed)
            self.assertFalse((import_root / "tul-source-latest.zip").exists())

    def test_verify_root_alias_is_markdown_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            work = root / "import" / "tul" / "work"
            work.mkdir(parents=True)
            ctx = FakeContext("tul", repo, {"platform": {"work_root": str(work)}})
            md = root / "tul-vf-latest.md"
            js = root / "tul-vf-latest.json"
            md.write_text("verify\n", encoding="utf-8")
            js.write_text("{}\n", encoding="utf-8")

            result = publish_verify_upload_alias(ctx, md, json_path=js, head="abcdef1234567890", now=datetime(2026, 5, 14, 1, 2, 3))
            import_root = work.parent

            self.assertTrue((import_root / "tul-vf-abcdef1.md").exists())
            self.assertFalse((import_root / "tul-vf-abcdef1.json").exists())
            self.assertTrue(Path(result.dated_json_alias).exists())


if __name__ == "__main__":
    unittest.main()
