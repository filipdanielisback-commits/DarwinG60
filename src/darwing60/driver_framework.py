"""Host-side driver matching and lifecycle model.

This module models registration and binding decisions only. It performs no
bus enumeration, MMIO, DMA, interrupts, firmware loading, or hardware I/O.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class DriverState(str, Enum):
    REGISTERED = "registered"
    MATCHED = "matched"
    BOUND_SIMULATED = "bound_simulated"
    FAILED = "failed"


@dataclass(frozen=True)
class DeviceDescriptor:
    """Evidence-backed identity supplied by a host-side test fixture."""

    name: str
    bus: str
    vendor_id: str | None = None
    device_id: str | None = None
    compatible: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.bus.strip():
            raise ValueError("Device name and bus must be non-empty.")
        if any(not item.strip() for item in self.compatible):
            raise ValueError("Compatible identifiers cannot be empty.")


@dataclass(frozen=True)
class DriverDescriptor:
    """Declarative matching information; identifiers must come from evidence."""

    name: str
    buses: tuple[str, ...]
    vendor_device_ids: tuple[tuple[str, str], ...] = ()
    compatibles: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.buses:
            raise ValueError("Driver name and at least one bus are required.")
        if any(not bus.strip() for bus in self.buses):
            raise ValueError("Bus names cannot be empty.")
        if any(not vendor.strip() or not device.strip()
               for vendor, device in self.vendor_device_ids):
            raise ValueError("Vendor/device identifiers cannot be empty.")
        if any(not item.strip() for item in self.compatibles):
            raise ValueError("Compatible identifiers cannot be empty.")


@dataclass
class DriverBinding:
    device: DeviceDescriptor
    driver: DriverDescriptor
    state: DriverState = DriverState.MATCHED
    notes: list[str] = field(default_factory=list)


class DriverManager:
    """A deterministic host-side registry; never discovers real devices."""

    def __init__(self) -> None:
        self._drivers: dict[str, DriverDescriptor] = {}

    @property
    def drivers(self) -> tuple[DriverDescriptor, ...]:
        return tuple(self._drivers.values())

    def register(self, driver: DriverDescriptor) -> None:
        key = driver.name.casefold()
        if key in self._drivers:
            raise ValueError(f"Driver already registered: {driver.name}")
        self._drivers[key] = driver

    @staticmethod
    def matches(driver: DriverDescriptor, device: DeviceDescriptor) -> bool:
        if device.bus not in driver.buses:
            return False
        id_match = (
            device.vendor_id is not None
            and device.device_id is not None
            and (device.vendor_id, device.device_id) in driver.vendor_device_ids
        )
        compatible_match = bool(set(device.compatible) & set(driver.compatibles))
        return id_match or compatible_match

    def find_matches(self, device: DeviceDescriptor) -> tuple[DriverDescriptor, ...]:
        return tuple(
            driver for driver in self._drivers.values()
            if self.matches(driver, device)
        )

    def simulate_bind(self, device: DeviceDescriptor, driver_name: str) -> DriverBinding:
        """Create a clearly simulated binding after a metadata match."""
        driver = self._drivers.get(driver_name.casefold())
        if driver is None:
            raise KeyError(f"Unknown driver: {driver_name}")
        if not self.matches(driver, device):
            raise ValueError("Driver does not match the supplied device metadata.")
        return DriverBinding(
            device=device,
            driver=driver,
            state=DriverState.BOUND_SIMULATED,
            notes=["Host-side simulated binding; no hardware was accessed."],
        )
