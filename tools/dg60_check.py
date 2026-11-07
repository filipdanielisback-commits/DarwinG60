#!/usr/bin/env python3
"""Validate the DarwinG60 research repository without touching a device.

Run from the repository root:
    python3 tools/dg60_check.py
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "ROADMAP.md",
    "SECURITY.md",
    "docs/architecture.md",
    "docs/boot-process.md",
    "docs/compatibility.md",
)
PROJECT = {
    "name": "DarwinG60",
    "device": "Motorola Moto G60",
    "codename": "hanoip",
    "architecture": "ARM64 (research target; device details require source verification)",
    "status": "research-only",
    "bootable_release": False,
}


def main() -> int:
    print(f"{PROJECT['name']} repository check")
    print("=" * 36)
    failures = 0

    for relative in REQUIRED_FILES:
        path = ROOT / relative
        exists = path.is_file()
        print(f"[{'OK' if exists else 'MISSING'}] {relative}")
        failures += not exists

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    for phrase in ("hanoip", "not a working iOS port", "bootable"):
        present = phrase.casefold() in readme.casefold()
        print(f"[{'OK' if present else 'CHECK'}] README mentions: {phrase}")
        failures += not present

    print("\nProject metadata:")
    print(json.dumps(PROJECT, indent=2))
    print("\nNo device was accessed or modified.")
    if failures:
        print(f"\nResult: {failures} check(s) need attention.")
        return 1
    print("\nResult: all repository checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
