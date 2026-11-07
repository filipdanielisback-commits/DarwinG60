# Core subsystem architecture

DarwinG60 is intended to grow into an independent operating-system research
project. This document records the responsibilities of major kernel areas;
it does not claim that a kernel or device drivers currently exist.

## Planned kernel areas

| Subsystem | Responsibility | Current state |
|---|---|---|
| Scheduler | Decide which task receives CPU time | Planned |
| Memory manager | Manage address spaces and memory ownership | Planned |
| IPC | Define safe communication between processes | Planned |
| VFS | Provide a common filesystem interface | Planned |
| Driver framework | Establish hardware-driver boundaries | Planned |
| Power manager | Coordinate power states and battery reporting | Planned |
| Network stack | Provide networking interfaces, including future Wi-Fi support | Planned |

The Python catalogue in `src/darwing60/kernel_model.py` is metadata for
architecture planning and validation. It is not an executable kernel.

## User interface is a separate layer

A future graphical shell should consume system services rather than directly
owning hardware. The status bar, control center, settings, notifications, and
battery indicators belong to the user-interface and service layers.

## Hardware boundary

Moto G60 support requires verified device documentation, a supported boot
strategy, a kernel, and device-specific drivers. Wi-Fi and battery support
must not be marked working until implemented and tested on actual supported
hardware. Host-side simulations do not count as device support.

## Design principles

- Keep kernel, services, drivers, and graphical shell as separate layers.
- Prefer documented interfaces and testable components.
- Track implementation status honestly.
- Keep original project code and licensing clear; do not copy proprietary Apple
  operating-system components.
