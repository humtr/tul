"""Shared source/review artifact schema constants."""
from __future__ import annotations

SOURCE_MANIFEST_ENTRY = "source-manifest.json"
SOURCE_FILE_LIST_ENTRY = "source-file-list.txt"
SOURCE_FILE_SHA256S_ENTRY = "source-file-sha256s.txt"
SOURCE_ROOT_LAYOUT = "repo-files-at-zip-root"
SOURCE_REQUIRED_ENTRIES = (
    "README.md",
    ".tul.yml",
    "bin/tul",
    "lib/tulcore/__init__.py",
    SOURCE_MANIFEST_ENTRY,
    SOURCE_FILE_LIST_ENTRY,
    SOURCE_FILE_SHA256S_ENTRY,
)
SOURCE_METADATA_ENTRIES = {
    SOURCE_MANIFEST_ENTRY,
    SOURCE_FILE_LIST_ENTRY,
    SOURCE_FILE_SHA256S_ENTRY,
}

REVIEW_MANIFEST_ENTRY = "export-manifest.json"
REVIEW_RUNTIME_TRUTH = "head-tagged verify markdown upload artifact"
REVIEW_EMBEDDED_RUNTIME_RECORDS_ROLE = "generation-context snapshot"
REVIEW_REQUIRED_ENTRIES = (
    "README.md",
    "git-head.txt",
    "changed-files.txt",
    "diff.patch",
    "state.json",
    "report.md",
    "handoff.md",
    REVIEW_MANIFEST_ENTRY,
)
