"""Print the integrated synthetic display/touch research profile."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.display_touch_profile import (  # noqa: E402
    DisplayProfileError, load_display_touch_profile,
)

def main() -> int:
    try:
        profile = load_display_touch_profile()
    except DisplayProfileError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(profile.build_report())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
