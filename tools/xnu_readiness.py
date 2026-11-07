"""Run the non-destructive DarwinG60 XNU readiness audit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.xnu_readiness import (  # noqa: E402
    XNUReadinessError,
    audit_xnu_readiness,
    format_report,
)


def main() -> int:
    try:
        report = audit_xnu_readiness(ROOT)
    except XNUReadinessError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(format_report(report))
    print("\nJSON report:")
    print(json.dumps(report, indent=2))
    return 1 if report["baseline"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
