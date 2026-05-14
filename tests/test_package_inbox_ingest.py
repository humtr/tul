from __future__ import annotations

import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

from lib.tulcore.errors import PackageError
from lib.tulcore.package import discover_package_inventory, import_package, safe_extract


def write_package(path: Path) -> None:
    manifest = """version: 1
name: sample-package

target:
  project: tul
  repo: humtr/tul
  branch: main

apply:
  mode: copy
  files:
    - from: files/README.md
      to: README.md

commit:
  files:
    - README.md
  message: sample
"""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("tul-package.yml", manifest)
        z.writestr("files/README.md", "sample\n")
        z.writestr("README.md", "sample package\n")


class PackageInboxIngestTest(unittest.TestCase):
    def test_external_download_package_is_moved_to_project_inbox_after_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            download = root / "Download"
            work = root / "termux" / "import" / "tul" / "work"
            download.mkdir(parents=True)
            work.mkdir(parents=True)
            source = download / "sample-package.zip"
            write_package(source)

            imported = import_package(source, {
                "platform": {
                    "inbox_roots": [str(download), str(work.parent / "inbox")],
                    "work_root": str(work),
                }
            })

            self.assertFalse(source.exists())
            self.assertTrue(imported.source.exists())
            self.assertIsNotNone(imported.ingested_source)
            self.assertTrue(Path(imported.ingested_source).exists())
            self.assertEqual(work.parent / "inbox", Path(imported.ingested_source).parent)

    def test_project_inbox_package_is_not_moved_again(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            work = root / "termux" / "import" / "tul" / "work"
            inbox = work.parent / "inbox"
            inbox.mkdir(parents=True)
            work.mkdir(parents=True, exist_ok=True)
            source = inbox / "sample-package.zip"
            write_package(source)

            imported = import_package(source, {
                "platform": {
                    "inbox_roots": [str(inbox)],
                    "work_root": str(work),
                }
            })

            self.assertTrue(source.exists())
            self.assertIsNone(imported.ingested_source)

    def test_tar_gz_packages_are_not_discovered_or_extracted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inbox = root / "inbox"
            work = root / "work"
            dest = root / "dest"
            inbox.mkdir()
            work.mkdir()
            package = inbox / "sample-package.tar.gz"
            manifest = root / "tul-package.yml"
            manifest.write_text("version: 1\nname: sample\n", encoding="utf-8")
            with tarfile.open(package, "w:gz") as tf:
                tf.add(manifest, "tul-package.yml")

            discovery = discover_package_inventory(
                {"platform": {"inbox_roots": [str(inbox)], "work_root": str(work)}},
                project="tul",
                repo="humtr/tul",
                branch="main",
            )

            self.assertEqual([], discovery.matching)
            self.assertEqual([], discovery.incompatible)
            self.assertEqual([], discovery.invalid)
            with self.assertRaises(PackageError):
                safe_extract(package, dest)


if __name__ == "__main__":
    unittest.main()
