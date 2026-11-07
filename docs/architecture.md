# Architecture research notes

## Purpose

This document is a place to record the major layers that would need investigation for an ARM64 Darwin/XNU research effort. It is not a design specification for a working port.

## Conceptual layers

1. **Boot environment** — the platform's firmware and boot stages, their interfaces, and the assumptions they pass to later stages.
2. **Kernel** — XNU source, architecture support, platform initialization, memory management, interrupts, and scheduling.
3. **Hardware support** — device-specific drivers and interfaces for storage, display, input, networking, power, and other peripherals.
4. **Userspace** — the runtime, libraries, services, and system components expected by the target Darwin environment.
5. **Integration and validation** — reproducible builds, logs, compatibility tests, and recovery planning.

A successful build of one layer does not prove that the layers above or below it work together.

## Research rules

- Cite upstream source files, documentation, and exact revisions.
- Keep original project code separate from imported third-party code.
- Record assumptions and unknowns explicitly.
- Do not describe a component as implemented until there is a reproducible test result.

## Driver architecture registry

The seven-category, per-device driver planning catalogue is documented in
[Driver Architecture Registry](architecture/driver-registry.md). It is a
metadata-only host tool and does not implement or test hardware drivers.

The first host-side driver framework model is documented in
[driver-framework.md](architecture/driver-framework.md). It is a metadata-only
prototype and does not perform physical device discovery or hardware I/O.
