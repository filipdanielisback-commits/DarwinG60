"""List and inspect DarwinG60 device profile metadata.

This tool only reads files in the repository. It never connects to or modifies
a phone and cannot validate real hardware compatibility.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVICE_ROOT = ROOT / "devices"


def device_profiles() -> list[tuple[str, Path]]:
    if not DEVICE_ROOT.exists():
        return []
    return sorted(
        (path.name, path)
        for path in DEVICE_ROOT.iterdir()
        if path.is_dir() and (path / "device.json").is_file()
    )


def load_profile(codename: str) -> dict:
    path = DEVICE_ROOT / codename / "device.json"
    if not path.is_file():
        raise FileNotFoundError(f"No device profile found for: {codename}")
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Device profile must contain a JSON object: {path}")
    return data


def check_profiles() -> list[str]:
    errors: list[str] = []
    for codename, path in device_profiles():
        try:
            data = load_profile(codename)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{codename}: {exc}")
            continue
        if not data:
            errors.append(f"{codename}: profile is empty")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect DarwinG60 device profile metadata (host-side only)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="List known device profiles")
    show_parser = subparsers.add_parser("show", help="Show a device profile")
    show_parser.add_argument("codename")
    subparsers.add_parser("check", help="Validate profile JSON structure")
    args = parser.parse_args()

    if args.command == "list":
        profiles = device_profiles()
        if not profiles:
            print("No device profiles found.")
        for codename, _ in profiles:
            print(codename)
        return 0

    if args.command == "show":
        try:
            print(json.dumps(load_profile(args.codename), indent=2))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"Error: {exc}")
            return 1
        return 0

    errors = check_profiles()
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Checked {len(device_profiles())} device profile(s).")
    print("Metadata checks only; no hardware compatibility is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
