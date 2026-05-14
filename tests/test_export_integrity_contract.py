from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace

from helpers import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "lib"))

from tulcore.integrity import inspect_review_bundle, inspect_source_bundle  # noqa: E402


class ExportIntegrityContractTest(unittest.TestCase):
    def fake_context(self):
        return SimpleNamespace(
            project_id="tul",
            repo_path=REPO_ROOT,
            global_config={},
        )

    def write_source_bundle(self, path: Path, *, head: str) -> None:
        manifest = {
            "kind": "source",
            "head": head,
            "root_layout": "repo-files-at-zip-root",
            "file_count": 3,
            "payload_sha256": "dummy",
        }
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("source-manifest.json", json.dumps(manifest))
            z.writestr("source-file-list.txt", "README.md\n")
            z.writestr("source-file-sha256s.txt", "README.md  dummy\n")

    def write_review_bundle(self, path: Path, *, head: str) -> None:
        manifest = {
            "kind": "review",
            "head": head,
            "basis": "current-head",
            "changed_file_count": 0,
        }
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            manifest["verify_markdown_entry"] = "tul-vf-aaaaaaa.md"
            z.writestr("export-manifest.json", json.dumps(manifest))
            z.writestr("tul-vf-aaaaaaa.md", "# tul verify\n")
            z.writestr("state.json", "{}\n")
            z.writestr("handoff.md", "# handoff\n")

    def test_source_bundle_current_and_stale_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "source.zip"
            self.write_source_bundle(path, head="A")
            state = {"source_bundle_export": {"path": str(path)}}
            current = inspect_source_bundle(self.fake_context(), state=state, current_head="A")
            stale = inspect_source_bundle(self.fake_context(), state=state, current_head="B")
        self.assertEqual("current", current["status"])
        self.assertEqual("stale", stale["status"])
        self.assertTrue(any("stale" in item for item in stale["warnings"]))

    def test_review_bundle_current_and_stale_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "review.zip"
            self.write_review_bundle(path, head="A")
            state = {"review_bundle_export": {"path": str(path)}}
            current = inspect_review_bundle(self.fake_context(), state=state, current_head="A")
            stale = inspect_review_bundle(self.fake_context(), state=state, current_head="B")
        self.assertEqual("current", current["status"])
        self.assertEqual("stale", stale["status"])
        self.assertEqual("current-head", current["basis"])
        self.assertEqual("tul-vf-aaaaaaa.md", current["verify_markdown_entry"])
        self.assertTrue(any("stale" in item for item in stale["warnings"]))


if __name__ == "__main__":
    unittest.main()
