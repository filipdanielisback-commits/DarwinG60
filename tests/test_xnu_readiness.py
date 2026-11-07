"""Tests for the non-destructive XNU readiness audit."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwing60.xnu_readiness import (
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
        '\n'.join([
            'repository = "https://github.com/apple-oss-distributions/xnu"',
            f'tag = "{EXPECTED_TAG}"',
            f'tag_object = "{EXPECTED_TAG_OBJECT}"',
            'source_archive = "https://github.com/apple-oss-distributions/xnu/archive/refs/tags/xnu-11215.1.10.tar.gz"',
            'license = "APPLE_LICENSE"',
            'license_name = "Apple Public Source License 2.0"',
        ]) + '\n',
        encoding="utf-8",
    )
    (xnu / "APPLE_LICENSE").write_text("license text", encoding="utf-8")


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

    def test_source_import_requires_all_expected_upstream_sentinels(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository(root)
            upstream = root / "kernel" / "xnu" / "upstream"
            upstream.mkdir()
            for name in ("README.md", "osfmk", "bsd", "iokit", "APPLE_LICENSE"):
                path = upstream / name
                path.mkdir() if name in {"osfmk", "bsd", "iokit"} else path.write_text("x")
            report = audit_xnu_readiness(root, environ={}, platform_name="Linux")
        self.assertTrue(report["milestones"]["source_tree_imported"])

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
