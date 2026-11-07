"""Inspect device compatibility metadata; no phone or hardware access."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.device_catalog import (  # noqa: E402
    compatibility_matrix,
    list_devices,
    load_device,
    validate_catalogue,
)

DEVICE_ROOT = ROOT / "devices"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect DarwinG60 device compatibility metadata."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List devices in the catalogue")
    show = commands.add_parser("show", help="Show one device profile")
    show.add_argument("codename")
    matrix = commands.add_parser("matrix", help="Show component compatibility")
    matrix.add_argument("codename")
    commands.add_parser("check", help="Check metadata consistency")
    args = parser.parse_args()

    if args.command == "list":
        for codename in list_devices(DEVICE_ROOT):
            print(codename)
        return 0

    if args.command in {"show", "matrix"}:
        try:
            record = load_device(DEVICE_ROOT, args.codename)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"Error: {exc}")
            return 1
        if args.command == "show":
            print(json.dumps(record, indent=2))
        else:
            for row in compatibility_matrix(record):
                print(f'{row["component"]}: {row["status"]}')
        return 0

    errors = validate_catalogue(DEVICE_ROOT)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Catalogue metadata valid for {len(list_devices(DEVICE_ROOT))} device(s).")
    print("This does not establish hardware compatibility.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
