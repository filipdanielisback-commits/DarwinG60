"""Create starter device metadata; this tool never modifies a phone."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.profile_generator import generate_profile  # noqa: E402

DEVICE_ROOT = ROOT / "devices"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a host-side DarwinG60 device research profile."
    )
    parser.add_argument("--codename", required=True, help="Lowercase device codename")
    parser.add_argument("--manufacturer", required=True, help="Device manufacturer")
    parser.add_argument("--model", required=True, help="Marketing model name")
    args = parser.parse_args()

    try:
        target = generate_profile(
            DEVICE_ROOT, args.codename, args.manufacturer, args.model
        )
    except (ValueError, FileExistsError, OSError) as exc:
        print(f"Error: {exc}")
        return 1

    print(f"Created starter profile: {target.relative_to(ROOT)}")
    print("Review and source every hardware specification before using it.")
    print("This creates metadata only; it does not add hardware support.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
