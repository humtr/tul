from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from lib.tulcore.config import ProjectContext
from lib.tulcore.state import write_state
from lib.tulcore.verify import VerifyResult, refresh_verify_upload_runtime_snapshots, write_verify_artifacts


def init_repo(repo: Path) -> str:
    subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / "README.md").write_text("test\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()


class VerifySnapshotRefreshTest(unittest.TestCase):
    def test_refresh_rewrites_head_tagged_verify_markdown_with_transport_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            head = init_repo(repo)
            work = root / "import" / "tul" / "work"
            ctx = ProjectContext(
                target=str(repo),
                project_id="tul",
                repo_path=repo,
                global_config={"platform": {"work_root": str(work)}},
                repo_config={"name": "tul", "repo": "humtr/tul", "branch": "main"},
                global_config_path=root / "config.yml",
            )
            result = VerifyResult(project="tul", repo=str(repo), branch="main", head=head, remote_head=head)
            result.add("local repo: smoke", True, "ok")
            artifacts = write_verify_artifacts(ctx, result, include_runtime_snapshots=False)
            import_root = work.parent
            source = import_root / f"tul-source-{head[:7]}.zip"
            review = import_root / f"tul-review-{head[:7]}.zip"
            source.write_bytes(b"source")
            review.write_bytes(b"review")
            write_state(
                work / "run" / "state.json",
                project="tul",
                source_bundle_export={"upload_aliases": {"root_alias": str(source)}},
                review_bundle_export={"upload_aliases": {"root_alias": str(review)}},
            )

            self.assertTrue(refresh_verify_upload_runtime_snapshots(ctx))

            upload_markdown = Path(artifacts["upload_markdown"])
            text = upload_markdown.read_text(encoding="utf-8")
            self.assertIn("## Runtime snapshots", text)
            self.assertIn(f"- Upload source: {source}", text)
            self.assertIn(f"- Upload review: {review}", text)
            payload = json.loads(Path(artifacts["json"]).read_text(encoding="utf-8"))
            aliases = payload["artifact"]["upload_aliases"]
            self.assertEqual(str(source), aliases["source"]["root_alias"])
            self.assertEqual(str(review), aliases["review"]["root_alias"])


if __name__ == "__main__":
    unittest.main()
