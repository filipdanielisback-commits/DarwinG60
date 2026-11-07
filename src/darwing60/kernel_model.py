"""Host-side architecture model for planned DarwinG60 kernel subsystems.

This module describes interfaces and implementation status only. It is not a
kernel, does not execute privileged instructions, and does not access hardware.
"""
from dataclasses import dataclass
from enum import Enum


class SubsystemStatus(str, Enum):
    PLANNED = "planned"
    INTERFACE_ONLY = "interface-only"
    HOST_MODEL = "host-model"
    HARDWARE_IMPLEMENTATION = "hardware-implementation"
    TESTED_ON_DEVICE = "tested-on-device"


@dataclass(frozen=True)
class KernelSubsystem:
    name: str
    purpose: str
    status: SubsystemStatus
    dependencies: tuple[str, ...] = ()


SUBSYSTEMS = (
    KernelSubsystem("scheduler", "Plans CPU task scheduling.", SubsystemStatus.PLANNED),
    KernelSubsystem("memory-manager", "Defines virtual and physical memory responsibilities.", SubsystemStatus.PLANNED),
    KernelSubsystem("ipc", "Defines communication between processes and services.", SubsystemStatus.PLANNED),
    KernelSubsystem("vfs", "Defines the virtual filesystem boundary.", SubsystemStatus.PLANNED),
    KernelSubsystem("driver-framework", "Defines how hardware drivers will be represented.", SubsystemStatus.PLANNED),
    KernelSubsystem("power-manager", "Coordinates power states and battery information.", SubsystemStatus.PLANNED),
    KernelSubsystem("network-stack", "Defines networking and Wi-Fi integration boundaries.", SubsystemStatus.PLANNED),
)


def validate_subsystems(subsystems: tuple[KernelSubsystem, ...] = SUBSYSTEMS) -> list[str]:
    """Return structural problems in a subsystem catalogue."""
    errors: list[str] = []
    seen: set[str] = set()
    for subsystem in subsystems:
        if not subsystem.name.strip():
            errors.append("Subsystem name cannot be empty.")
        elif subsystem.name in seen:
            errors.append(f"Duplicate subsystem: {subsystem.name}")
        seen.add(subsystem.name)
    known = {item.name for item in subsystems}
    for subsystem in subsystems:
        for dependency in subsystem.dependencies:
            if dependency not in known:
                errors.append(
                    f"{subsystem.name} depends on unknown subsystem {dependency}."
                )
    return errors


def subsystem_report(subsystems: tuple[KernelSubsystem, ...] = SUBSYSTEMS) -> str:
    """Render a concise, honest status report."""
    lines = ["DarwinG60 kernel architecture (host-side catalogue)", ""]
    lines.extend(
        f"- {item.name}: {item.status.value} — {item.purpose}"
        for item in subsystems
    )
    lines.extend(("", "No kernel code is running; all entries are planning metadata."))
    return "\n".join(lines)
