"""Command-line checker for the hanoip hardware evidence ledger."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.hardware_evidence import (  # noqa: E402
    EvidenceError, build_report, load_evidence, validate_evidence,
)

def main() -> int:
    try:
        ledger = load_evidence()
    except EvidenceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_evidence(ledger)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(build_report(ledger))
    print("\nEvidence ledger validation: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
