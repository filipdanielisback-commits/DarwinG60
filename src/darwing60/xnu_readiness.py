"""Non-destructive audit of DarwinG60's pinned XNU research baseline.

This module inspects repository metadata and the local host environment only.
It does not download, configure, compile, install, or boot XNU.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import platform
import shutil
from pathlib import Path
from typing import Any, Callable

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
XNU_ROOT = REPOSITORY_ROOT / "kernel" / "xnu"
LOCK_PATH = XNU_ROOT / "UPSTREAM.lock"
EXPECTED_TAG = "xnu-11215.1.10"
EXPECTED_TAG_OBJECT = "d95cbeef34d1a9cca097b33d385db3b2aae1a755"
EXPECTED_SOURCE_COMMIT = "8d741a5de7ff4191bf97d57b9f54c2f6d4a15585"
SOURCE_TREE = XNU_ROOT / "upstream"
BUILD_RECORD = XNU_ROOT / "build-verification.json"
SOURCE_SENTINELS = ("README.md", "osfmk", "bsd", "iokit", "APPLE_LICENSE")


class XNUReadinessError(ValueError):
    """Raised when the XNU source pin is missing or malformed."""


def _parse_lock(path: Path) -> dict[str, str]:
    """Parse the deliberately small key/value subset used by UPSTREAM.lock."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise XNUReadinessError(f"Cannot read upstream lock file: {path}") from exc
    values: dict[str, str] = {}
    for number, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise XNUReadinessError(f"Invalid lock entry on line {number}.")
        key, raw_value = (part.strip() for part in line.split("=", 1))
        try:
            value = ast.literal_eval(raw_value)
        except (SyntaxError, ValueError) as exc:
            raise XNUReadinessError(f"Invalid value for {key!r} on line {number}.") from exc
        if not isinstance(value, str) or not key:
            raise XNUReadinessError(f"Lock entry on line {number} must be a string.")
        if key in values:
            raise XNUReadinessError(f"Duplicate lock key: {key}.")
        values[key] = value
    return values


def audit_xnu_readiness(
    root: Path = REPOSITORY_ROOT,
    environ: dict[str, str] | None = None,
    platform_name: str | None = None,
    command_lookup: Callable[[str], str | None] = shutil.which,
) -> dict[str, Any]:
    """Return a machine-readable, evidence-conscious XNU readiness report."""
    root = Path(root)
    xnu_root = root / "kernel" / "xnu"
    lock_path = xnu_root / "UPSTREAM.lock"
    env = dict(os.environ if environ is None else environ)
    host_platform = platform_name or platform.system()

    lock = _parse_lock(lock_path)
    errors: list[str] = []
    if lock.get("repository") != "https://github.com/apple-oss-distributions/xnu":
        errors.append("Unexpected upstream repository URL.")
    if lock.get("tag") != EXPECTED_TAG:
        errors.append(f"Expected pinned tag {EXPECTED_TAG}.")
    if lock.get("tag_object") != EXPECTED_TAG_OBJECT:
        errors.append("Pinned tag object does not match the reviewed baseline.")
    if lock.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append("Pinned upstream source commit does not match the reviewed tag target.")
    if lock.get("license") != "APPLE_LICENSE":
        errors.append("Lock file does not point to the expected upstream license.")
    license_present = (xnu_root / "APPLE_LICENSE").is_file()
    if not license_present:
        errors.append("The upstream Apple license text is missing.")

    source_root = xnu_root / "upstream"
    missing_source_items = [
        item for item in SOURCE_SENTINELS if not (source_root / item).exists()
    ]
    git_metadata = source_root / ".git"
    source_imported = not missing_source_items and git_metadata.exists()
    if not git_metadata.exists():
        missing_source_items.append(".git submodule metadata (initialize submodules)")

    required_commands = ("make", "clang", "xcrun", "xcodebuild")
    commands = {name: command_lookup(name) is not None for name in required_commands}
    sdkroot_value = env.get("SDKROOT", "").strip()
    sdkroot_present = bool(sdkroot_value and Path(sdkroot_value).exists())
    host_is_macos = host_platform == "Darwin"
    toolchain_candidate = (
        host_is_macos
        and all(commands.values())
        and sdkroot_present
    )

    # A build is only counted when a reviewed record points to real, hashed
    # artifacts and logs inside this repository (never inside the upstream submodule).
    build_verified = False
    build_record_errors: list[str] = []
    if BUILD_RECORD.is_file():
        try:
            record = json.loads(BUILD_RECORD.read_text(encoding="utf-8"))
            required_fields = (
                "result", "tag", "tag_object", "source_commit", "build_host",
                "sdk", "command", "artifact", "artifact_sha256", "log",
                "log_sha256", "reviewed_by",
            )
            for field in required_fields:
                if not isinstance(record.get(field), str) or not record[field].strip():
                    build_record_errors.append(f"Missing build record field: {field}")
            if record.get("result") != "success":
                build_record_errors.append("Build record result is not success.")
            if record.get("tag") != EXPECTED_TAG:
                build_record_errors.append("Build record tag does not match the pinned tag.")
            if record.get("tag_object") != EXPECTED_TAG_OBJECT:
                build_record_errors.append("Build record tag object does not match.")
            if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
                build_record_errors.append("Build record source commit does not match.")
            for path_field, hash_field in (("artifact", "artifact_sha256"), ("log", "log_sha256")):
                relative = record.get(path_field)
                expected_hash = record.get(hash_field)
                if not isinstance(relative, str) or not isinstance(expected_hash, str):
                    continue
                candidate = (xnu_root / relative).resolve()
                try:
                    candidate.relative_to(xnu_root.resolve())
                except ValueError:
                    build_record_errors.append(f"{path_field} must stay inside kernel/xnu/.")
                    continue
                if not candidate.is_file():
                    build_record_errors.append(f"Build {path_field} file is missing.")
                    continue
                actual_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
                if actual_hash != expected_hash:
                    build_record_errors.append(f"Build {path_field} SHA-256 does not match.")
            build_verified = not build_record_errors
        except (OSError, json.JSONDecodeError) as exc:
            build_record_errors.append(f"Cannot read build verification record: {exc}")
    else:
        build_record_errors.append("No reviewed build-verification.json record exists.")

    return {
        "project": "DarwinG60",
        "device_codename": "hanoip",
        "baseline": {
            "repository": lock.get("repository"),
            "tag": lock.get("tag"),
            "tag_object": lock.get("tag_object"),
            "source_commit": lock.get("source_commit"),
            "source_archive": lock.get("source_archive"),
            "license_file_present": license_present,
            "lock_valid": not errors,
            "errors": errors,
        },
        "milestones": {
            "source_reference_pinned": not errors,
            "source_tree_imported": source_imported,
            "build_environment_candidate": toolchain_candidate,
            "kernel_build_verified": build_verified,
        },
        "source_import": {
            "source_root": str(source_root),
            "missing_expected_items": missing_source_items,
            "status": "imported" if source_imported else "not_imported",
        },
        "build_environment": {
            "host_platform": host_platform,
            "required_commands": commands,
            "sdkroot_configured": sdkroot_present,
            "sdkroot_path": sdkroot_value or None,
            "candidate_status": (
                "candidate_only; exact SDK/KDK compatibility remains unverified"
                if toolchain_candidate
                else "not_ready_or_not_detected"
            ),
        },
        "build_verification": {
            "status": "verified" if build_verified else "not_verified",
            "record_path": str(BUILD_RECORD),
            "errors": build_record_errors,
            "note": (
                "A reviewed JSON record, matching pinned source, and SHA-256-verified build artifact and log are required; the audit never compiles XNU."
            ),
        },
        "device_port_status": "not_ported; Moto G60 platform support unverified",
        "limitations": [
            "This is a host-side metadata and prerequisite audit, not an XNU build.",
            "A candidate toolchain does not prove the exact SDK/KDK is compatible.",
            "The pinned tag is an iOS 18-era research baseline, not a verified point-release mapping.",
            "No Moto G60 boot, driver, firmware, or hardware compatibility is established.",
        ],
    }


def format_report(report: dict[str, Any]) -> str:
    """Format the audit as concise terminal output."""
    milestones = report["milestones"]
    baseline = report["baseline"]
    environment = report["build_environment"]
    lines = [
        "DarwinG60 XNU readiness audit",
        "==============================",
        f"Baseline: {baseline['tag']} ({baseline['tag_object']})",
        f"Source reference pinned: {'YES' if milestones['source_reference_pinned'] else 'NO'}",
        f"Full upstream source imported: {'YES' if milestones['source_tree_imported'] else 'NO'}",
        f"Build environment candidate: {'YES' if milestones['build_environment_candidate'] else 'NO'}",
        f"XNU build verified: {'YES' if milestones['kernel_build_verified'] else 'NO'}",
        "",
        f"Host: {environment['host_platform']}",
        f"SDKROOT configured: {'YES' if environment['sdkroot_configured'] else 'NO'}",
        "Commands: " + ", ".join(
            f"{name}={'found' if found else 'missing'}"
            for name, found in environment["required_commands"].items()
        ),
        f"Source import status: {report['source_import']['status']}",
        f"Build verification: {report['build_verification']['status']}",
        f"Device status: {report['device_port_status']}",
    ]
    for error in baseline["errors"]:
        lines.append(f"ERROR: {error}")
    lines.extend(["", "This tool does not download, build, install, or boot XNU."])
    return "\n".join(lines)
