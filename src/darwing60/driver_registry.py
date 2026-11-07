"""Metadata-only driver architecture registry for DarwinG60."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DRIVER_CATEGORIES: tuple[dict[str, str], ...] = (
    {"id": "display_touch", "name": "Display and touchscreen", "scope": "Panel output, display modes, touch input and gesture events."},
    {"id": "gpu", "name": "GPU", "scope": "Graphics device discovery, command submission research and rendering acceleration."},
    {"id": "wifi_bluetooth", "name": "Wi-Fi and Bluetooth", "scope": "Wireless networking, radio control and Bluetooth device communication."},
    {"id": "battery_power", "name": "Battery and charging", "scope": "Battery telemetry, charging state, thermal signals and power policy."},
    {"id": "audio", "name": "Audio", "scope": "Audio routing, playback, capture and codec research."},
    {"id": "sensors", "name": "Sensors", "scope": "Sensor discovery and standardized motion, orientation and environmental events."},
    {"id": "storage", "name": "Storage", "scope": "Storage-controller research, block-device abstraction and filesystem integration."},
)
VALID_STATUSES = {"planned", "research", "prototype", "not_tested", "hardware_tested"}
DEFAULT_STATUS = "planned"


def build_registry(codename: str) -> dict[str, Any]:
    """Create an in-memory registry for a device; no hardware is accessed."""
    if not codename or Path(codename).name != codename:
        raise ValueError("Invalid device codename.")
    return {
        "schema_version": 1,
        "device_codename": codename,
        "scope": "Planning metadata only; no driver implementation or hardware support is implied.",
        "drivers": [
            {
                **category,
                "status": DEFAULT_STATUS,
                "hardware": "Unknown; requires device-specific research.",
                "darwing60_implementation": "None",
                "evidence": [],
                "tests": [],
                "gaps": ["Identify the exact hardware component and its software interface."],
            }
            for category in DRIVER_CATEGORIES
        ],
    }


def load_registry(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Driver registry must be a JSON object.")
    return data


def validate_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    codename = data.get("device_codename")
    if not isinstance(codename, str) or not codename:
        errors.append("device_codename must be a non-empty string.")
    drivers = data.get("drivers")
    if not isinstance(drivers, list):
        return errors + ["drivers must be a list."]
    seen: set[str] = set()
    for item in drivers:
        if not isinstance(item, dict):
            errors.append("Each driver entry must be an object.")
            continue
        driver_id = item.get("id")
        if not isinstance(driver_id, str) or not driver_id:
            errors.append("Every driver needs a non-empty id.")
            continue
        if driver_id in seen:
            errors.append(f"Duplicate driver id: {driver_id}")
        seen.add(driver_id)
        if item.get("status") not in VALID_STATUSES:
            errors.append(f"{driver_id}: invalid status {item.get('status')!r}.")
        for field in ("evidence", "tests", "gaps"):
            if not isinstance(item.get(field), list):
                errors.append(f"{driver_id}: {field} must be a list.")
    expected = {category["id"] for category in DRIVER_CATEGORIES}
    missing = sorted(expected - seen)
    extra = sorted(seen - expected)
    if missing:
        errors.append("Missing driver categories: " + ", ".join(missing))
    if extra:
        errors.append("Unknown driver categories: " + ", ".join(extra))
    return errors


def render_registry(data: dict[str, Any]) -> str:
    lines = [f"DarwinG60 driver registry: {data.get('device_codename', 'unknown')}", ""]
    for driver in data.get("drivers", []):
        lines.extend([
            f"{driver.get('name', driver.get('id', 'Unknown'))} — {driver.get('status', 'unknown')}",
            f"  Scope: {driver.get('scope', 'Not specified')}",
            f"  Hardware: {driver.get('hardware', 'Unknown')}",
            f"  Implementation: {driver.get('darwing60_implementation', 'Not specified')}",
            f"  Evidence entries: {len(driver.get('evidence', []))}",
            f"  Tests recorded: {len(driver.get('tests', []))}",
            f"  Open gaps: {len(driver.get('gaps', []))}",
            "",
        ])
    lines.append(str(data.get("scope", "Planning metadata only.")))
    return "\n".join(lines)
