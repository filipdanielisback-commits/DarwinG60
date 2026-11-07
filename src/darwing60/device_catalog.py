"""Read-only compatibility catalogue for DarwinG60 device research."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def list_devices(device_root: Path) -> list[str]:
    """Return codenames with both device and compatibility metadata."""
    if not device_root.is_dir():
        return []
    return sorted(
        path.name for path in device_root.iterdir()
        if path.is_dir()
        and (path / "device.json").is_file()
        and (path / "compatibility.json").is_file()
    )


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return data


def load_device(device_root: Path, codename: str) -> dict[str, Any]:
    """Load a device's identity and compatibility records."""
    if not codename or Path(codename).name != codename:
        raise ValueError("Invalid device codename.")
    folder = device_root / codename
    device = _read_json(folder / "device.json")
    compatibility = _read_json(folder / "compatibility.json")
    if compatibility.get("device_codename") != codename:
        raise ValueError(
            f"Compatibility metadata codename does not match folder: {codename}"
        )
    return {"codename": codename, "device": device, "compatibility": compatibility}


def compatibility_matrix(record: dict[str, Any]) -> list[dict[str, str]]:
    """Flatten compatibility components into a display-friendly matrix."""
    components = record["compatibility"].get("components", [])
    rows: list[dict[str, str]] = []
    for item in components:
        if not isinstance(item, dict):
            continue
        rows.append({
            "component": str(item.get("name", "Unnamed component")),
            "status": str(item.get("status", "unknown")),
            "implementation": str(item.get("darwing60_implementation", "Not specified")),
        })
    return rows


def validate_catalogue(device_root: Path) -> list[str]:
    """Check metadata consistency; this does not validate real hardware."""
    errors: list[str] = []
    for codename in list_devices(device_root):
        try:
            record = load_device(device_root, codename)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{codename}: {exc}")
            continue
        statuses = {"documented", "unknown", "not_implemented", "not_tested"}
        for row in compatibility_matrix(record):
            if row["status"] not in statuses:
                errors.append(
                    f"{codename}: unsupported status {row['status']} "
                    f"for {row['component']}"
                )
    return errors
