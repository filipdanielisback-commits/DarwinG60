"""Integrated, read-only system information for DarwinG60 host-side research."""
from __future__ import annotations

import json
from typing import Any

from darwing60.arm64_simulator import ARM64BootSimulator
from darwing60.device_profile import (
    load_compatibility,
    load_device_profile,
    validate_profiles,
)


def build_system_info() -> dict[str, Any]:
    """Collect project metadata into one stable, JSON-serializable report."""
    profile = load_device_profile()
    compatibility = load_compatibility()
    device = profile["device"]
    platform = profile["platform"]
    status = profile["research_status"]
    components = compatibility["components"]
    counts: dict[str, int] = {}
    for item in components:
        state = item.get("status", "unknown")
        counts[state] = counts.get(state, 0) + 1

    return {
        "project": "DarwinG60",
        "mode": "HOST-SIDE RESEARCH ONLY",
        "device": {
            "manufacturer": device["manufacturer"],
            "name": device["marketing_name"],
            "codename": device["codename"],
        },
        "platform": {
            "architecture": platform["architecture"],
            "soc": platform["soc_marketing_name"],
            "cpu": platform["cpu"],
            "gpu": platform["gpu"],
        },
        "implementation": dict(status),
        "compatibility": {
            "component_count": len(components),
            "status_counts": counts,
            "components": components,
        },
        "simulated_startup": [
            {
                "name": stage.name,
                "status": stage.status,
                "description": stage.description,
            }
            for stage in ARM64BootSimulator().run()
        ],
        "validation_errors": validate_profiles(),
        "limitations": [
            "No hardware probing is performed.",
            "No real bootloader or XNU kernel is implemented.",
            "The startup sequence is a conceptual simulation.",
            "No phone settings, storage, or partitions are accessed.",
        ],
    }


def render_dashboard(data: dict[str, Any]) -> str:
    """Render a readable terminal dashboard from system information."""
    device = data["device"]
    platform = data["platform"]
    counts = data["compatibility"]["status_counts"]
    implementation = data["implementation"]

    lines = [
        "╔══════════════════════════════════════════════╗",
        "║             DARWING60 SYSTEM INFO            ║",
        "╚══════════════════════════════════════════════╝",
        f"Mode:     {data['mode']}",
        f"Device:   {device['manufacturer']} {device['name']} ({device['codename']})",
        f"SoC:      {platform['soc']}",
        f"CPU:      {platform['cpu']}",
        f"GPU:      {platform['gpu']}",
        "",
        "PROJECT IMPLEMENTATION",
        "-----------------------",
        f"Bootloader: {implementation['bootloader_implemented']}",
        f"XNU port:   {implementation['xnu_kernel_ported']}",
        f"Drivers:    {implementation['device_drivers_implemented']}",
        f"Boot image: {implementation['bootable_image_available']}",
        "",
        "COMPATIBILITY INVENTORY",
        "-----------------------",
        f"Total components: {data['compatibility']['component_count']}",
    ]
    for status in sorted(counts):
        lines.append(f"{status}: {counts[status]}")

    lines.extend(["", "SIMULATED STARTUP"])
    for index, stage in enumerate(data["simulated_startup"], start=1):
        lines.append(f"{index}. [{stage['status']}] {stage['name']}")

    lines.extend([
        "",
        f"Metadata validation: {'PASS' if not data['validation_errors'] else 'FAIL'}",
        "Safety: read-only host report; no phone communication.",
    ])
    if data["validation_errors"]:
        lines.extend(["", "VALIDATION ERRORS"])
        lines.extend(f"- {error}" for error in data["validation_errors"])
    return "\n".join(lines)


def to_json(data: dict[str, Any]) -> str:
    """Serialize system information as formatted JSON."""
    return json.dumps(data, indent=2, sort_keys=True)
