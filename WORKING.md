# DarwinG60 feature tracker

This is the public status board for the long-term DarwinG60 operating-system
project. Status labels describe implementation evidence, not ambition.

**Status definitions**
- **Planned** — identified, not implemented.
- **In development** — code is actively being built.
- **Host prototype** — works only in host-side tests or simulations.
- **Hardware testing** — implementation exists and is being tested on named hardware.
- **Working** — verified on supported hardware with documented test evidence.

## Core operating-system foundations

| Feature | Status | Notes |
|---|---|---|
| Project architecture and documentation | Host prototype | Research structure and design docs exist |
| Kernel subsystem catalogue | Host prototype | Metadata only; no real kernel |
| Kernel scheduler | Planned | No scheduler implementation |
| Memory manager | Planned | No real memory management |
| Inter-process communication (IPC) | Planned | Interface design still needed |
| Virtual filesystem (VFS) | Planned | No mounted filesystem |
| Driver framework | Planned | No device drivers |
| Actual OS kernel | Planned | Major milestone; not yet implemented |
| Boot process / bootloader | Planned | No bootable image or device boot support |

## Moto G60 hardware support

| Feature | Status | Notes |
|---|---|---|
| Moto G60 (hanoip) device profile | Host prototype | Reference metadata only |
| Hardware bring-up | Planned | Requires a verified, supported development path |
| Display and touch | Planned | No working driver |
| Wi-Fi | Planned | No wireless driver or network stack |
| Bluetooth | Planned | No Bluetooth implementation |
| Battery status and charging | Planned | No power or battery driver |
| Audio | Planned | No audio driver |
| Cameras | Planned | No camera support |
| Sensors | Planned | No sensor integration |
| GPU acceleration | Planned | No graphics driver |
| Storage | Planned | No device storage driver or filesystem integration |

## Graphical interface and user experience

| Feature | Status | Notes |
|---|---|---|
| Graphical shell | Planned | No graphical interface yet |
| Status bar | Planned | Future UI component |
| Control Center / quick settings | Planned | Future UI component |
| Wi-Fi controls | Planned | Depends on networking and UI services |
| Battery indicator | Planned | Depends on power and battery reporting |
| Settings application | Planned | Future system application |
| Notifications | Planned | Requires service and UI architecture |
| App launching / application model | Planned | Requires userspace design |
| Lock screen | Planned | Future UI component |

## Host-side developer tools

| Feature | Status | Notes |
|---|---|---|
| Repository checker | Host prototype | Runs on a development host |
| Device profile validator | Host prototype | Validates project metadata |
| ARM64 boot-flow simulator | Host prototype | Conceptual simulation only |
| System information dashboard | Host prototype | Reports project metadata |
| Service registry model | Host prototype | In-process lifecycle labels only |
| Automated host tests | Host prototype | Does not prove hardware compatibility |

## Rules for changing a status

1. A mockup is not a working system feature.
2. A host-side simulation is not hardware support.
3. A driver is not working until tested on the target hardware.
4. Wi-Fi requires demonstrated connectivity, not just a settings toggle.
5. Battery support requires real device readings and charging-state validation.
6. Kernel and boot milestones require reproducible build and test evidence.

DarwinG60 is an independent open-source research project. It is not a port of
complete iOS and does not contain Apple's proprietary frameworks or drivers.


## Porting to Another Device

The primary target remains Moto G60 / `hanoip`. Additional devices require
their own reviewed profile, boot-architecture research, driver feasibility
assessment, and validation plan. No second device is currently supported.

| Porting area | Status | Notes |
|---|---|---|
| Device inventory command | Host prototype | Reads repository metadata only |
| Device-specific profiles | In development | Current profile is hanoip |
| Boot architecture research | Planned | Verify each device; UEFI is not universal |
| UEFI/firmware compatibility assessment | Planned | No generic UEFI loader assumed |
| Kernel portability | Planned | Requires a real kernel architecture |
| Per-device driver matrix | Planned | Display, touch, storage, Wi-Fi, battery, audio, sensors, GPU |
| Per-device graphical integration | Planned | Depends on core services and drivers |
| Hardware validation | Planned | No additional device is currently validated |

See [porting overview](docs/porting/README.md) and
[host-side command reference](docs/porting/commands.md).


## Device compatibility database

| Feature | Status | Notes |
|---|---|---|
| Multi-device compatibility catalogue | Host prototype | Reads per-device JSON metadata |
| Compatibility matrix CLI | Host prototype | Reports documented/unknown/unimplemented states |
| Second device profile | Planned | No additional device is validated |

See [compatibility database documentation](docs/porting/compatibility-database.md).


## Device profile generator

| Feature | Status | Notes |
|---|---|---|
| Starter profile generator | Host prototype | Creates four metadata/documentation files |
| Unknown-value protection | Host prototype | Hardware specifications start unknown |
| Existing-profile overwrite protection | Host prototype | Generator refuses existing codename directories |

See [profile generator documentation](docs/porting/profile-generator.md).


## Six-area hardware readiness assessment

| Area | Status | Notes |
|---|---|---|
| CPU and platform research | Host prototype | Summarizes device profile evidence |
| Boot and firmware research | Host prototype | Reports unknowns; does not validate boot firmware |
| Display and GPU | Host prototype | Tracks documentation and implementation gaps |
| Wi-Fi and Bluetooth | Host prototype | Reports driver implementation status |
| Battery and power management | Host prototype | Tracks missing power support evidence |
| Kernel and graphics readiness | Host prototype | Does not test or boot a kernel |

See [hardware readiness documentation](docs/porting/hardware-readiness.md).
