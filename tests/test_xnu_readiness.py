"""Tests for the non-destructive XNU readiness audit."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from darwing60.xnu_readiness import (
    EXPECTED_SOURCE_COMMIT,
    EXPECTED_TAG,
    EXPECTED_TAG_OBJECT,
    XNUReadinessError,
    audit_xnu_readiness,
    format_report,
)


def make_repository(root: Path) -> None:
    xnu = root / "kernel" / "xnu"
    xnu.mkdir(parents=True)
    (xnu / "UPSTREAM.lock").write_text(
        "\n".join([
            'repository = "https://github.com/apple-oss-distributions/xnu"',
            f'tag = "{EXPECTED_TAG}"',
            f'tag_object = "{EXPECTED_TAG_OBJECT}"',
            f'source_commit = "{EXPECTED_SOURCE_COMMIT}"',
            'source_archive = "https://github.com/apple-oss-distributions/xnu/archive/refs/tags/xnu-11215.1.10.tar.gz"',
            'license = "APPLE_LICENSE"',
            'license_name = "Apple Public Source License 2.0"',
        ]) + "\n",
        encoding="utf-8",
    )
    (xnu / "APPLE_LICENSE").write_text("license text", encoding="utf-8")


def make_imported_submodule(root: Path) -> None:
    upstream = root / "kernel" / "xnu" / "upstream"
    upstream.mkdir(parents=True)
    for name in ("README.md", "APPLE_LICENSE"):
        (upstream / name).write_text("upstream marker", encoding="utf-8")
    for name in ("osfmk", "bsd", "iokit"):
        (upstream / name).mkdir()
    # Git submodules commonly use a .git *file*, not a .git directory.
    (upstream / ".git").write_text("gitdir: ../../.git/modules/kernel/xnu/upstream\n")


class XNUReadinessTests(unittest.TestCase):
    def test_reference_pin_is_distinct_from_source_import_and_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            report = audit_xnu_readiness(
                root, environ={}, platform_name="Linux", command_lookup=lambda _: None
            )
        milestones = report["milestones"]
        self.assertTrue(milestones["source_reference_pinned"])
        self.assertFalse(milestones["source_tree_imported"])
        self.assertFalse(milestones["build_environment_candidate"])
        self.assertFalse(milestones["kernel_build_verified"])

    def test_source_import_requires_expected_tree_and_git_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            make_imported_submodule(root)
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        self.assertTrue(report["milestones"]["source_tree_imported"])

    def test_tree_without_git_metadata_is_not_counted_as_submodule_import(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            make_imported_submodule(root)
            (root / "kernel" / "xnu" / "upstream" / ".git").unlink()
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        self.assertFalse(report["milestones"]["source_tree_imported"])

    def test_mismatched_tag_object_is_an_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            lock = root / "kernel" / "xnu" / "UPSTREAM.lock"
            lock.write_text(lock.read_text().replace(EXPECTED_TAG_OBJECT, "0" * 40))
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        self.assertFalse(report["milestones"]["source_reference_pinned"])
        self.assertTrue(any("tag object" in item for item in report["baseline"]["errors"]))

    def test_missing_license_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            (root / "kernel" / "xnu" / "APPLE_LICENSE").unlink()
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        self.assertFalse(report["baseline"]["license_file_present"])
        self.assertFalse(report["milestones"]["source_reference_pinned"])

    def test_toolchain_candidate_requires_macos_commands_and_existing_sdkroot(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            sdk = root / "sdk"
            sdk.mkdir()
            found = {"make": "/usr/bin/make", "clang": "/usr/bin/clang",
                     "xcrun": "/usr/bin/xcrun", "xcodebuild": "/usr/bin/xcodebuild"}
            report = audit_xnu_readiness(
                root, environ={"SDKROOT": str(sdk)}, platform_name="Darwin",
                command_lookup=lambda name: found.get(name),
            )
        self.assertTrue(report["milestones"]["build_environment_candidate"])

    def test_linux_is_not_reported_as_apple_build_environment_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            sdk = root / "sdk"
            sdk.mkdir()
            found = {name: "/tool/" + name for name in ("make", "clang", "xcrun", "xcodebuild")}
            report = audit_xnu_readiness(
                root, environ={"SDKROOT": str(sdk)}, platform_name="Linux",
                command_lookup=lambda name: found.get(name),
            )
        self.assertFalse(report["milestones"]["build_environment_candidate"])

    def test_build_is_not_inferred_from_toolchain_alone(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            report = audit_xnu_readiness(root, environ={}, platform_name="Darwin")
        self.assertFalse(report["milestones"]["kernel_build_verified"])

    def test_build_verification_requires_real_hashed_artifact_and_log(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            xnu = root / "kernel" / "xnu"
            artifact = xnu / "build" / "kernel.test"
            log = xnu / "build" / "build.log"
            artifact.parent.mkdir()
            artifact.write_bytes(b"test kernel artifact")
            log.write_text("successful build log", encoding="utf-8")
            record = {
                "result": "success",
                "tag": EXPECTED_TAG,
                "tag_object": EXPECTED_TAG_OBJECT,
                "source_commit": EXPECTED_SOURCE_COMMIT,
                "build_host": "macOS test host",
                "sdk": "test SDK",
                "command": "make test-target",
                "artifact": "build/kernel.test",
                "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
                "log": "build/build.log",
                "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
                "reviewed_by": "test reviewer",
            }
            (xnu / "build-verification.json").write_text(json.dumps(record), encoding="utf-8")
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        self.assertTrue(report["milestones"]["kernel_build_verified"])

    def test_build_record_rejects_modified_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            xnu = root / "kernel" / "xnu"
            artifact = xnu / "build" / "kernel.test"
            log = xnu / "build" / "build.log"
            artifact.parent.mkdir()
            artifact.write_bytes(b"artifact")
            log.write_text("log", encoding="utf-8")
            record = {
                "result": "success", "tag": EXPECTED_TAG,
                "tag_object": EXPECTED_TAG_OBJECT, "source_commit": EXPECTED_SOURCE_COMMIT,
                "build_host": "macOS", "sdk": "SDK", "command": "make",
                "artifact": "build/kernel.test", "artifact_sha256": "0" * 64,
                "log": "build/build.log",
                "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
                "reviewed_by": "reviewer",
            }
            (xnu / "build-verification.json").write_text(json.dumps(record), encoding="utf-8")
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        self.assertFalse(report["milestones"]["kernel_build_verified"])

    def test_build_record_cannot_reference_files_outside_xnu_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            xnu = root / "kernel" / "xnu"
            record = {
                "result": "success", "tag": EXPECTED_TAG,
                "tag_object": EXPECTED_TAG_OBJECT, "source_commit": EXPECTED_SOURCE_COMMIT,
                "build_host": "macOS", "sdk": "SDK", "command": "make",
                "artifact": "../../outside", "artifact_sha256": "0" * 64,
                "log": "../../outside", "log_sha256": "0" * 64,
                "reviewed_by": "reviewer",
            }
            (xnu / "build-verification.json").write_text(json.dumps(record), encoding="utf-8")
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        self.assertFalse(report["milestones"]["kernel_build_verified"])

    def test_report_states_non_destructive_scope(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        rendered = format_report(report)
        self.assertIn("Full upstream source imported: NO", rendered)
        self.assertIn("XNU build verified: NO", rendered)
        self.assertIn("does not download, build, install, or boot XNU", rendered)

    def test_malformed_lock_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            (root / "kernel" / "xnu" / "UPSTREAM.lock").write_text("broken line")
            with self.assertRaises(XNUReadinessError):
                audit_xnu_readiness(root)


if __name__ == "__main__":
    unittest.main()
