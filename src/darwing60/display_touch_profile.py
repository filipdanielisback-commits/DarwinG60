"""Join synthetic display metadata to source-backed device research.

This is a host-side profile loader. It never discovers or configures hardware.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from darwing60.display_touch import (
    DisplayError, DisplayMode, DisplayTouchSubsystem, PanelProfile,
)
from darwing60.hardware_evidence import (
    EvidenceError, load_evidence, validate_evidence,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = ROOT / "examples" / "display-touch-synthetic.json"


class DisplayProfileError(ValueError):
    """Invalid synthetic display profile or associated research metadata."""


@dataclass(frozen=True)
class EvidenceSummary:
    claim_id: str
    subject: str
    status: str
    confidence: str
    finding: str


@dataclass(frozen=True)
class DisplayTouchResearchProfile:
    subsystem: DisplayTouchSubsystem
    device_label: str
    evidence: tuple[EvidenceSummary, ...]
    touch_coordinate_space: str

    @property
    def is_synthetic(self) -> bool:
        return True

    def build_report(self) -> str:
        mode = self.subsystem.current_mode
        lines = [
            f"Display/touch profile: {self.device_label}",
            "Profile kind: synthetic host-side fixture",
            f"Mode: {mode.name} ({mode.width}x{mode.height} @ {mode.refresh_hz:g} Hz)",
            f"Touch coordinates: {self.touch_coordinate_space}",
            "No physical hardware was detected or configured.",
            "",
            "Related hardware research:",
        ]
        for item in self.evidence:
            lines.append(
                f"- [{item.status}/{item.confidence}] {item.subject}: {item.finding}"
            )
        return "\n".join(lines)


def _read_fixture(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DisplayProfileError(f"Synthetic fixture not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DisplayProfileError(f"Invalid synthetic fixture JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise DisplayProfileError("Synthetic fixture must be a JSON object.")
    return data


def load_display_touch_profile(
    fixture_path: Path = DEFAULT_FIXTURE,
    evidence_path: Path | None = None,
) -> DisplayTouchResearchProfile:
    """Load synthetic modes and attach evidence summaries without merging identities."""
    fixture = _read_fixture(fixture_path)
    if fixture.get("schema_version") != 1:
        raise DisplayProfileError("Unsupported display fixture schema_version.")
    if fixture.get("synthetic") is not True:
        raise DisplayProfileError("Only explicitly synthetic display fixtures are accepted.")
    if fixture.get("device") != "synthetic-test-fixture":
        raise DisplayProfileError("Fixture device must remain synthetic-test-fixture.")

    panel_data = fixture.get("panel")
    if not isinstance(panel_data, dict):
        raise DisplayProfileError("Fixture panel section is required.")
    if panel_data.get("hardware_identifier") is not None:
        raise DisplayProfileError("Synthetic fixture cannot assert a hardware identifier.")

    raw_modes = panel_data.get("modes")
    if not isinstance(raw_modes, list) or not raw_modes:
        raise DisplayProfileError("Fixture must contain at least one display mode.")
    try:
        modes = tuple(
            DisplayMode(
                width=int(item["width"]),
                height=int(item["height"]),
                refresh_hz=float(item["refresh_hz"]),
                name=str(item["name"]),
            )
            for item in raw_modes
        )
        panel = PanelProfile(
            name=str(panel_data["name"]),
            modes=modes,
            preferred_mode=str(panel_data["preferred_mode"]),
            synthetic=True,
            hardware_identifier=None,
        )
        subsystem = DisplayTouchSubsystem(panel)
    except (KeyError, TypeError, ValueError, DisplayError) as exc:
        raise DisplayProfileError(f"Invalid synthetic panel metadata: {exc}") from exc

    touch_data = fixture.get("touch")
    if not isinstance(touch_data, dict):
        raise DisplayProfileError("Fixture touch section is required.")
    if touch_data.get("coordinate_space") != "normalized-0-to-1":
        raise DisplayProfileError("Unsupported synthetic touch coordinate space.")
    if any(touch_data.get(key) is not None for key in ("controller_identifier", "bus", "interrupt")):
        raise DisplayProfileError("Synthetic fixture cannot assert touch hardware details.")

    try:
        ledger = load_evidence(evidence_path) if evidence_path else load_evidence()
    except EvidenceError as exc:
        raise DisplayProfileError(f"Unable to load hardware evidence: {exc}") from exc
    errors = validate_evidence(ledger)
    if errors:
        raise DisplayProfileError("Hardware evidence ledger is invalid: " + "; ".join(errors))

    evidence = tuple(
        EvidenceSummary(
            claim_id=item["id"],
            subject=item["subject"],
            status=item["status"],
            confidence=item["confidence"],
            finding=item["finding"],
        )
        for item in ledger["claims"]
        if item.get("category") == "display_touch"
    )
    return DisplayTouchResearchProfile(
        subsystem=subsystem,
        device_label=str(fixture.get("device")),
        evidence=evidence,
        touch_coordinate_space=str(touch_data["coordinate_space"]),
    )
