"""Evidence-based hardware readiness report for device research profiles.

This module evaluates metadata completeness only. It does not probe hardware,
build drivers, test a kernel, or establish that a device can boot DarwinG60.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from darwing60.device_catalog import load_device

AREAS: dict[str, tuple[str, ...]] = {
    "cpu": ("ARM64 CPU execution environment",),
    "boot_firmware": ("Boot architecture / firmware",),
    "display_gpu": (
        "Display and touch",
        "GPU",
        "Adreno 618 graphics",
        "Display controller and panel initialization",
    ),
    "wireless": ("Wi-Fi and Bluetooth", "Wi-Fi", "Bluetooth"),
    "power": ("Battery and charging", "Battery status and charging"),
    "kernel_graphics": (
        "Kernel boot",
        "Darwin/XNU kernel boot on Moto G60",
        "Kernel",
    ),
}

STATUS_ORDER = ("documented", "unknown", "not_tested", "not_implemented")


def _normalise(value: str) -> str:
    return " ".join(value.casefold().replace("/", " ").split())


def _match_component(
    components: list[dict[str, Any]], aliases: tuple[str, ...]
) -> dict[str, Any] | None:
    wanted = {_normalise(alias) for alias in aliases}
    for component in components:
        if not isinstance(component, dict):
            continue
        name = _normalise(str(component.get("name", "")))
        if name in wanted:
            return component
    return None


def assess_device(device_root: Path, codename: str) -> dict[str, Any]:
    """Return an evidence-gap summary from one device's JSON metadata."""
    record = load_device(device_root, codename)
    components = record["compatibility"].get("components", [])
    if not isinstance(components, list):
        components = []

    areas: list[dict[str, Any]] = []
    for key, aliases in AREAS.items():
        matched = _match_component(components, aliases)
        if matched is None:
            status = "unknown"
            evidence = "No matching component entry in the compatibility profile."
            implementation = "Not specified"
            component_name = aliases[0]
        else:
            status = str(matched.get("status", "unknown"))
            evidence = str(matched.get("evidence", "No evidence note supplied."))
            implementation = str(
                matched.get("darwing60_implementation", "Not specified")
            )
            component_name = str(matched.get("name", aliases[0]))
        areas.append({
            "key": key,
            "title": key.replace("_", " ").title(),
            "component": component_name,
            "status": status,
            "evidence": evidence,
            "implementation": implementation,
        })

    counts = {status: 0 for status in STATUS_ORDER}
    for area in areas:
        if area["status"] in counts:
            counts[area["status"]] += 1
        else:
            counts["unknown"] += 1

    return {
        "codename": codename,
        "overall_status": record["compatibility"].get(
            "overall_status", "research_only"
        ),
        "areas": areas,
        "counts": counts,
        "scope": (
            "Metadata assessment only. This is not a hardware test, driver test, "
            "kernel boot test, or compatibility certification."
        ),
    }


def render_report(report: dict[str, Any]) -> str:
    lines = [
        f"DarwinG60 hardware readiness report: {report['codename']}",
        f"Profile status: {report['overall_status']}",
        "",
    ]
    for area in report["areas"]:
        lines.extend([
            f"{area['title']} — {area['status']}",
            f"  Component: {area['component']}",
            f"  Evidence: {area['evidence']}",
            f"  Implementation: {area['implementation']}",
            "",
        ])
    lines.append(report["scope"])
    return "\n".join(lines)
