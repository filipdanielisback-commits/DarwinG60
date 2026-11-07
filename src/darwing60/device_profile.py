"""Read-only device profile and compatibility reporting for DarwinG60."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEVICE_DIRECTORY = REPOSITORY_ROOT / "devices" / "hanoip"


class ProfileError(ValueError):
    """Raised when device metadata is missing or malformed."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ProfileError(f"Required profile file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ProfileError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ProfileError(f"Expected a JSON object in {path}")
    return data


def load_device_profile() -> dict[str, Any]:
    data = load_json(DEVICE_DIRECTORY / "device.json")
    required = ("device", "platform", "memory_and_storage", "display", "research_status")
    missing = [key for key in required if key not in data]
    if missing:
        raise ProfileError("Device profile is missing sections: " + ", ".join(missing))
    return data


def load_compatibility() -> dict[str, Any]:
    data = load_json(DEVICE_DIRECTORY / "compatibility.json")
    if not isinstance(data.get("components"), list):
        raise ProfileError("Compatibility file must contain a components list")
    return data


def build_report() -> str:
    profile = load_device_profile()
    compatibility = load_compatibility()
    device = profile["device"]
    platform = profile["platform"]
    display = profile["display"]
    memory = profile["memory_and_storage"]
    status = profile["research_status"]

    lines = [
        "DarwinG60 Device Research",
        "=========================",
        f"Device: {device['manufacturer']} {device['marketing_name']}",
        f"Codename: {device['codename']}",
        f"SoC: {platform['soc_marketing_name']}",
        f"CPU: {platform['cpu']}",
        f"GPU: {platform['gpu']}",
        f"RAM options: {', '.join(map(str, memory['ram_gb_options']))} GB",
        f"Storage options: {', '.join(map(str, memory['storage_gb_options']))} GB",
        f"Display: {display['diagonal_inches']} inch, "
        f"{display['resolution_pixels'][0]}x{display['resolution_pixels'][1]}, "
        f"{display['refresh_rate_hz']} Hz",
        "",
        "DarwinG60 implementation status",
        "-------------------------------",
        f"Hardware probed: {status['hardware_probed_by_darwing60']}",
        f"Bootloader implemented: {status['bootloader_implemented']}",
        f"XNU kernel ported: {status['xnu_kernel_ported']}",
        f"Drivers implemented: {status['device_drivers_implemented']}",
        f"Bootable image available: {status['bootable_image_available']}",
        "",
        "Compatibility overview",
        "----------------------",
    ]
    for component in compatibility["components"]:
        lines.append(f"- [{component['status']}] {component['name']}")
    lines.extend([
        "",
        "Research-only prototype. This report does not test or modify a phone.",
    ])
    return "\n".join(lines)


def validate_profiles() -> list[str]:
    """Return validation errors; an empty list means the metadata is structurally valid."""
    errors: list[str] = []
    try:
        profile = load_device_profile()
        compatibility = load_compatibility()
    except ProfileError as exc:
        return [str(exc)]

    if profile.get("schema_version") != 1:
        errors.append("Unsupported device profile schema_version")
    if profile.get("device", {}).get("codename") != "hanoip":
        errors.append("Expected device codename 'hanoip'")
    allowed = {"documented", "unknown", "not_implemented", "not_tested"}
    for index, component in enumerate(compatibility["components"]):
        if not isinstance(component, dict):
            errors.append(f"Component {index} must be an object")
            continue
        if component.get("status") not in allowed:
            errors.append(f"Component {index} has an invalid status")
        for field in ("name", "evidence", "darwing60_implementation"):
            if not component.get(field):
                errors.append(f"Component {index} is missing {field}")
    return errors
