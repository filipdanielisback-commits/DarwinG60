#!/usr/bin/env python3
"""Print or validate the DarwinG60 Moto G60 device profile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.device_profile import (  # noqa: E402
    ProfileError,
    build_report,
    load_compatibility,
    load_device_profile,
    validate_profiles,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--json", action="store_true", help="print the device profile as JSON")
    group.add_argument("--check", action="store_true", help="validate profile metadata")
    args = parser.parse_args()

    try:
        if args.check:
            errors = validate_profiles()
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            print("DarwinG60 device profile: OK")
            return 0
        if args.json:
            print(json.dumps({
                "device": load_device_profile(),
                "compatibility": load_compatibility(),
            }, indent=2))
            return 0
        print(build_report())
        return 0
    except ProfileError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
