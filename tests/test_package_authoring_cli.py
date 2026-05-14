from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from helpers import run_tul


class PackageAuthoringCliTest(unittest.TestCase):
    def test_package_new_honors_out_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)

            result = run_tul(
                "package",
                "new",
                "sample-package",
                "--project",
                "tul",
                "--repo",
                "humtr/tul",
                "--branch",
                "main",
                "--message",
                "Test package",
                "--out",
                str(out),
            )

            package_dir = out / "sample-package"
            self.assertIn(str(package_dir), result.stdout)
            self.assertTrue((package_dir / "tul-package.yml").exists())

    def test_package_zip_honors_out_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            run_tul(
                "package",
                "new",
                "sample-package",
                "--project",
                "tul",
                "--repo",
                "humtr/tul",
                "--branch",
                "main",
                "--message",
                "Test package",
                "--out",
                str(out),
            )
            archive = out / "custom-name.zip"

            result = run_tul("package", "zip", str(out / "sample-package"), "--out", str(archive))

            self.assertIn(str(archive), result.stdout)
            self.assertTrue(archive.exists())


if __name__ == "__main__":
    unittest.main()
