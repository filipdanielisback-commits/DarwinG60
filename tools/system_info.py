#!/usr/bin/env python3
"""Display the integrated DarwinG60 research dashboard."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.device_profile import ProfileError  # noqa: E402
from darwing60.system_info import build_system_info, render_dashboard, to_json  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--check", action="store_true", help="return failure if metadata validation fails")
    args = parser.parse_args()

    try:
        data = build_system_info()
    except (ProfileError, KeyError, TypeError) as exc:
        print(f"DarwinG60 system report failed: {exc}", file=sys.stderr)
        return 2

    print(to_json(data) if args.json else render_dashboard(data))
    if args.check and data["validation_errors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
