"""Inspect and validate the device driver planning registry."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.driver_registry import (  # noqa: E402
    build_registry, load_registry, render_registry, validate_registry,
)

REGISTRY_DIR = ROOT / "devices"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect driver planning metadata; no hardware is accessed.")
    sub = parser.add_subparsers(dest="command", required=True)
    show = sub.add_parser("show", help="Print the seven driver categories for a device")
    show.add_argument("codename")
    check = sub.add_parser("check", help="Validate a saved device driver registry")
    check.add_argument("codename")
    export = sub.add_parser("template", help="Print a starter registry as JSON")
    export.add_argument("codename")
    args = parser.parse_args()

    if args.command == "template":
        import json
        print(json.dumps(build_registry(args.codename), indent=2))
        return 0

    path = REGISTRY_DIR / args.codename / "drivers.json"
    try:
        data = load_registry(path)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    errors = validate_registry(data)
    if args.command == "check":
        if errors:
            print("\n".join(errors))
            return 1
        print(f"{args.codename}: driver registry metadata is valid.")
        return 0
    print(render_registry(data))
    if errors:
        print("\nValidation warnings:")
        print("\n".join(errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
