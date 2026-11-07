"""Inventory XNU build prerequisites on a macOS host; never changes the host."""
from __future__ import annotations

import os
import platform
import plistlib
import shutil
import subprocess
from pathlib import Path


def run(command: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except OSError as exc:
        return 127, str(exc)
    return result.returncode, (result.stdout + result.stderr).strip()


def main() -> int:
    print("DarwinG60 XNU macOS/KDK dependency probe")
    print("========================================")
    print(f"Host platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    for label, command in (
        ("macOS version", ["sw_vers", "-productVersion"]),
        ("macOS build", ["sw_vers", "-buildVersion"]),
    ):
        code, output = run(command)
        print(f"{label}: {output if code == 0 else 'UNAVAILABLE'}")

    commands = {
        "xcodebuild": ["xcodebuild", "-version"],
        "xcodebuild_sdks": ["xcodebuild", "-showsdks"],
        "clang": ["clang", "--version"],
        "make": ["make", "--version"],
        "sdk_path": ["xcrun", "--sdk", "macosx", "--show-sdk-path"],
        "developer_directory": ["xcode-select", "-p"],
    }
    outputs: dict[str, str] = {}
    for name, command in commands.items():
        if shutil.which(command[0]) is None:
            outputs[name] = "MISSING"
        else:
            code, output = run(command)
            outputs[name] = output if code == 0 else f"FAILED ({code}): {output}"
        print(f"\n[{name}]\n{outputs[name]}")

    print("\n[KDK inventory]")
    configured_kdk = os.environ.get("KDKROOT")
    kdk_root = Path(configured_kdk) if configured_kdk else Path("/Library/Developer/KDKs")
    if configured_kdk:
        kdk_paths = [kdk_root] if kdk_root.is_dir() else []
    else:
        kdk_paths = sorted(kdk_root.glob("*.kdk")) if kdk_root.is_dir() else []
    if not kdk_paths:
        print(f"No KDK found under {kdk_root}")
    for kdk in kdk_paths:
        print(f"KDK candidate: {kdk}")
        plist_paths = (
            kdk / "System/Library/Extensions/System.kext/Info.plist",
            kdk / "System/Library/Extensions/System.kext/Contents/Info.plist",
        )
        metadata_found = False
        for plist_path in plist_paths:
            if plist_path.is_file():
                try:
                    with plist_path.open("rb") as stream:
                        version = plistlib.load(stream).get("CFBundleVersion", "UNKNOWN")
                    print(f"  System.kext CFBundleVersion: {version}")
                    metadata_found = True
                except (OSError, plistlib.InvalidFileException) as exc:
                    print(f"  Could not read {plist_path}: {exc}")
        if not metadata_found:
            print("  System.kext CFBundleVersion: NOT_FOUND")

    sdk_path_value = outputs.get("sdk_path", "")
    sdk_exists = False
    if sdk_path_value and not sdk_path_value.startswith(("FAILED", "MISSING")):
        sdk = Path(sdk_path_value.splitlines()[0])
        sdk_exists = sdk.is_dir()
        checks = {
            "AvailabilityVersions availability.pl": sdk / "usr/local/libexec/availability.pl",
            "Kernel.framework headers": sdk / "System/Library/Frameworks/Kernel.framework/Headers",
            "System.kext version metadata": sdk / "System/Library/Extensions/System.kext/Info.plist",
            "libfirehose kernel library": sdk / "usr/local/lib/libfirehose_kernel.dylib",
        }
        print("\n[SDK dependency inventory]")
        for label, candidate_path in checks.items():
            print(f"{label}: {'PRESENT' if candidate_path.exists() else 'MISSING'} ({candidate_path})")

    tools_present = all(shutil.which(name) for name in ("xcodebuild", "clang", "make", "xcrun"))
    candidate = platform.system() == "Darwin" and tools_present and sdk_exists
    print("\nAssessment:")
    print("macOS toolchain candidate detected." if candidate else
          "No complete macOS toolchain candidate detected.")
    print("KDK compatibility: NOT ESTABLISHED by tool presence alone.")
    print("Exact XNU SDK/KDK compatibility: NOT ESTABLISHED.")
    print("No XNU build was attempted by this probe.")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write("## DarwinG60 XNU macOS/KDK dependency probe\n\n")
            summary.write(f"- Host: {platform.platform()} ({platform.machine()})\n")
            summary.write(f"- macOS toolchain candidate: **{'yes' if candidate else 'no'}**\n")
            summary.write("- Exact XNU SDK/KDK compatibility: **not established**\n")
            summary.write("- KDK and dependency inventory: see job logs\n")
            summary.write("- XNU build attempted by this probe: **no**\n")
    return 0 if candidate else 1


if __name__ == "__main__":
    raise SystemExit(main())
