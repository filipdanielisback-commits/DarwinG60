"""Inventory a macOS host as a possible XNU build environment.

This is an environment probe only. It does not configure or compile XNU and
cannot establish SDK/KDK compatibility for the pinned source revision.
"""
from __future__ import annotations

import os
import platform
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
    print("DarwinG60 XNU macOS build-environment probe")
    print("==========================================")
    print(f"Host platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
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

    sdk_path = outputs.get("sdk_path", "")
    sdk_exists = (
        bool(sdk_path)
        and sdk_path not in ("MISSING",)
        and not sdk_path.startswith("FAILED")
        and Path(sdk_path.splitlines()[0]).exists()
    )
    tools_present = all(
        shutil.which(name) for name in ("xcodebuild", "clang", "make", "xcrun")
    )
    candidate = platform.system() == "Darwin" and tools_present and sdk_exists
    print("\nAssessment:")
    print("macOS toolchain candidate detected." if candidate else
          "No complete macOS toolchain candidate detected.")
    print("This does NOT prove compatibility with XNU xnu-11215.1.10.")
    print("No XNU build was attempted.")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write("## DarwinG60 XNU build environment probe\n\n")
            summary.write(f"- Host: {platform.platform()} ({platform.machine()})\n")
            summary.write(f"- macOS toolchain candidate: **{'yes' if candidate else 'no'}**\n")
            summary.write("- Exact XNU SDK/KDK compatibility: **not established**\n")
            summary.write("- XNU build attempted: **no**\n\n")
            summary.write("See job logs for Xcode, SDK, compiler and make versions.\n")
    return 0 if candidate else 1


if __name__ == "__main__":
    raise SystemExit(main())
