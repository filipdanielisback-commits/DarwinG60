#!/usr/bin/env python3
"""Run the DarwinG60 host-side ARM64 startup simulation."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.arm64_simulator import ARM64BootSimulator  # noqa: E402


def main() -> int:
    print(ARM64BootSimulator().report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
