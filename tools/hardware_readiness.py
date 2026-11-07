"""Print evidence gaps from a DarwinG60 device metadata profile."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.readiness import assess_device, render_report  # noqa: E402

DEVICE_ROOT = ROOT / "devices"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assess device metadata readiness; no hardware is accessed."
    )
    parser.add_argument("codename", help="Device profile codename, e.g. hanoip")
    args = parser.parse_args()
    try:
        report = assess_device(DEVICE_ROOT, args.codename)
    except (OSError, ValueError, KeyError) as exc:
        print(f"Error: {exc}")
        return 1
    print(render_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
