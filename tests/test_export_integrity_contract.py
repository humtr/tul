from __future__ import annotations

import json
import hashlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace

from helpers import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "lib"))

from tulcore.integrity import docs_drift_warnings, inspect_review_bundle, inspect_source_bundle  # noqa: E402


class ExportIntegrityContractTest(unittest.TestCase):
    def fake_context(self):
        return SimpleNamespace(
            project_id="tul",
            repo_path=REPO_ROOT,
            global_config={},
        )

    def fake_context_for_repo(self, repo_path: Path):
        return SimpleNamespace(
            project_id="tul",
            repo_path=repo_path,
            global_config={},
        )

    def write_source_bundle(
        self,
        path: Path,
        *,
        head: str,
        working_tree: str = "clean",
        payload_text: str = "# readme\n",
        payload_sha256: str | None = None,
        file_count: int | None = None,
    ) -> None:
        payload_digest = hashlib.sha256(payload_text.encode("utf-8")).hexdigest()
        payload_size = len(payload_text.encode("utf-8"))
        source_hashes = [(payload_digest, "README.md", payload_size)]
        computed_payload_sha256 = self.source_payload_sha256(source_hashes)
        manifest = {
            "kind": "source",
            "head": head,
            "root_layout": "repo-files-at-zip-root",
            "working_tree": working_tree,
            "file_count": file_count if file_count is not None else len(source_hashes),
            "payload_sha256": payload_sha256 or computed_payload_sha256,
        }
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("source-manifest.json", json.dumps(manifest))
            z.writestr("source-file-list.txt", "README.md\n")
            z.writestr("source-file-sha256s.txt", f"{payload_digest}  README.md  {payload_size}\n")
            z.writestr("README.md", payload_text)

    def source_payload_sha256(self, file_hashes: list[tuple[str, str, int]]) -> str:
        h = hashlib.sha256()
        for digest, rel, size in file_hashes:
            h.update(rel.encode("utf-8"))
            h.update(b"\0")
            h.update(str(size).encode("ascii"))
            h.update(b"\0")
            h.update(digest.encode("ascii"))
            h.update(b"\n")
        return h.hexdigest()

    def write_review_bundle(
        self,
        path: Path,
        *,
        head: str,
        verify_text: str = "# tul verify\n",
        verify_sha256: str | None = None,
    ) -> None:
        verify_sha256 = verify_sha256 or hashlib.sha256(verify_text.encode("utf-8")).hexdigest()
        manifest = {
            "kind": "review",
            "head": head,
            "state_commit": "state-commit",
            "basis": "current-head",
            "changed_file_count": 0,
            "runtime_truth": "head-tagged verify markdown upload artifact",
            "embedded_runtime_records_role": "generation-context snapshot",
            "verify_markdown_sha256": verify_sha256,
        }
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            manifest["verify_markdown_entry"] = "tul-vf-aaaaaaa.md"
            z.writestr("export-manifest.json", json.dumps(manifest))
            z.writestr("tul-vf-aaaaaaa.md", verify_text)
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

    def test_source_bundle_rejects_dirty_export_as_current(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "source.zip"
            self.write_source_bundle(path, head="A", working_tree="dirty")
            state = {"source_bundle_export": {"path": str(path)}}
            result = inspect_source_bundle(self.fake_context(), state=state, current_head="A")

        self.assertEqual("stale", result["status"])
        self.assertTrue(any("dirty working tree" in item for item in result["warnings"]))

    def test_source_bundle_rejects_payload_sha_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "source.zip"
            self.write_source_bundle(path, head="A", payload_sha256="0" * 64)
            state = {"source_bundle_export": {"path": str(path)}}
            result = inspect_source_bundle(self.fake_context(), state=state, current_head="A")

        self.assertEqual("invalid", result["status"])
        self.assertTrue(any("payload sha256" in item for item in result["warnings"]))

    def test_source_bundle_rejects_file_count_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "source.zip"
            self.write_source_bundle(path, head="A", file_count=2)
            state = {"source_bundle_export": {"path": str(path)}}
            result = inspect_source_bundle(self.fake_context(), state=state, current_head="A")

        self.assertEqual("invalid", result["status"])
        self.assertTrue(any("file_count" in item for item in result["warnings"]))

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
        self.assertEqual("state-commit", current["state_commit"])
        self.assertEqual("head-tagged verify markdown upload artifact", current["runtime_truth"])
        self.assertEqual("generation-context snapshot", current["embedded_runtime_records_role"])
        self.assertTrue(any("stale" in item for item in stale["warnings"]))

    def test_review_bundle_rejects_verify_markdown_sha_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "review.zip"
            self.write_review_bundle(path, head="A", verify_sha256="0" * 64)
            state = {"review_bundle_export": {"path": str(path)}}
            result = inspect_review_bundle(self.fake_context(), state=state, current_head="A")

        self.assertEqual("invalid", result["status"])
        self.assertTrue(any("verify markdown sha256" in item for item in result["warnings"]))

    def test_docs_drift_does_not_require_status_to_shadow_latest_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            (repo / "docs/status").mkdir(parents=True)
            (repo / "docs/status/current.md").write_text("# current status\n\nRuntime facts live in tul show.\n", encoding="utf-8")
            (repo / "docs/roadmap.md").write_text("# roadmap\n", encoding="utf-8")
            (repo / "docs/manifest.md").write_text("# manifest\n", encoding="utf-8")

            result = docs_drift_warnings(
                self.fake_context_for_repo(repo),
                latest_state_data={"package_name": "tul-macro-stage-a-artifact-test-split-v9"},
            )

        self.assertEqual("clean", result["status"])
        self.assertEqual("tul-macro-stage-a-artifact-test-split-v9", result["latest_package"])
        self.assertEqual([], result["warnings"])


if __name__ == "__main__":
    unittest.main()
