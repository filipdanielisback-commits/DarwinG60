"""Safe, host-side model of a hypothetical ARM64 startup sequence.

This module does not execute machine code, inspect hardware, reserve memory,
or boot an operating system. Addresses in the memory map are illustrative.
"""
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CPUProfile:
    architecture: str = "AArch64 (ARM64)"
    soc: str = "Qualcomm Snapdragon 732G"
    gpu: str = "Adreno 618"
    hardware_verified: bool = False


@dataclass(frozen=True)
class MemoryRegion:
    name: str
    start: int
    size: int
    purpose: str

    @property
    def end(self) -> int:
        return self.start + self.size


@dataclass(frozen=True)
class BootStage:
    name: str
    description: str
    status: str = "SIMULATED"


def validate_memory_map(regions: Iterable[MemoryRegion]) -> list[str]:
    """Return validation issues for an illustrative map."""
    ordered = sorted(regions, key=lambda region: region.start)
    issues: list[str] = []
    for region in ordered:
        if region.start < 0 or region.size <= 0:
            issues.append(f"{region.name}: start must be >= 0 and size > 0")
    for previous, current in zip(ordered, ordered[1:]):
        if previous.end > current.start:
            issues.append(f"{previous.name} overlaps {current.name}")
    return issues


class ARM64BootSimulator:
    """Describes startup stages; it does not perform a real boot."""

    def __init__(self, cpu: CPUProfile | None = None) -> None:
        self.cpu = cpu or CPUProfile()
        self.stages = (
            BootStage("reset", "A processor reset is represented."),
            BootStage("firmware", "Platform firmware would initialize the board."),
            BootStage("boot-manager", "A boot manager would select an entry."),
            BootStage("kernel-handoff", "Control would be handed to a kernel."),
            BootStage("userspace", "A userspace environment would start."),
        )

    def run(self) -> list[BootStage]:
        """Return the planned sequence without executing hardware operations."""
        return list(self.stages)

    def report(self) -> str:
        lines = [
            "DarwinG60 ARM64 Startup Simulator",
            "MODE: HOST-SIDE SIMULATION ONLY",
            f"Architecture: {self.cpu.architecture}",
            f"SoC: {self.cpu.soc}",
            f"GPU: {self.cpu.gpu}",
            f"Hardware profile verified: {'yes' if self.cpu.hardware_verified else 'no'}",
            "",
            "Startup sequence:",
        ]
        lines.extend(
            f"{index}. [{stage.status}] {stage.name}: {stage.description}"
            for index, stage in enumerate(self.run(), start=1)
        )
        lines.extend([
            "",
            "No firmware, bootloader, kernel, or device memory was accessed.",
        ])
        return "\n".join(lines)
