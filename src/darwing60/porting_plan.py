"""Read-only helpers for the device porting inventory."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEVICE_ROOT = ROOT / "devices"


def device_profiles() -> list[tuple[str, Path]]:
    if not DEVICE_ROOT.exists():
        return []
    return sorted(
        (path.name, path)
        for path in DEVICE_ROOT.iterdir()
        if path.is_dir() and (path / "device.json").is_file()
    )


def load_profile(codename: str) -> dict:
    if not codename or Path(codename).name != codename:
        raise ValueError("Invalid device codename.")
    path = DEVICE_ROOT / codename / "device.json"
    if not path.is_file():
        raise FileNotFoundError(f"No device profile found for: {codename}")
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Device profile must contain a JSON object: {path}")
    return data


def check_profiles() -> list[str]:
    errors: list[str] = []
    for codename, _ in device_profiles():
        try:
            data = load_profile(codename)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{codename}: {exc}")
            continue
    return errors
