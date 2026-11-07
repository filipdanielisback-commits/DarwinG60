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

## Driver architecture registry

| Feature | Status | Notes |
|---|---|---|
| Seven-category driver registry | Host prototype | Metadata catalogue and validator only |
| Display and touchscreen driver | Planned | No functional device driver |
| GPU driver | Planned | No graphics acceleration implementation |
| Wi-Fi and Bluetooth drivers | Planned | No wireless drivers |
| Battery and charging driver | Planned | No battery telemetry implementation |
| Audio driver | Planned | No audio implementation |
| Sensor drivers | Planned | No sensor integration |
| Storage driver | Planned | No device storage integration |

See [driver registry documentation](docs/architecture/driver-registry.md).

## Moto G60 hardware research

| Feature | Status | Notes |
|---|---|---|
| Seven-category hardware research dossier | Host prototype | Public-source review; exact component IDs remain unresolved |
| Display/touch panel identification | Research | Archived kernel DTS identifies Tianma/ILI7807S 1080×2460 config with 60/120 Hz modes; exact module SKU unknown |
| GPU platform identification | Documented | Adreno 618; no DarwinG60 GPU driver |
| Wireless platform research | Research | FastConnect platform features found; exact handset module unconfirmed |
| Battery capacity research | Documented | 6000 mAh listed in community sources; charging IC unknown |
| Audio codec identification | Research | Exact codec not confirmed |
| Sensor inventory | Research | Exact sensor part numbers unknown |
| Storage controller identification | Research | Capacity variants found; controller/media type unknown |

See [Moto G60 hardware research dossier](docs/porting/hanoip-hardware-research.md).

## Driver framework

| Feature | Status | Notes |
|---|---|---|
| Host-side driver registry/matching model | Host prototype | Synthetic metadata only; no bus discovery or hardware I/O |
| Simulated driver binding | Host prototype | Clearly labeled simulated lifecycle state |
| Moto G60 physical driver binding | Not implemented | Exact IDs and a real kernel/platform foundation are still required |

See [driver framework design](docs/architecture/driver-framework.md).

## Display and touch

| Feature | Status | Notes |
|---|---|---|
| Synthetic display-mode model | Host prototype | Test metadata only; no panel output |
| Synthetic frame sequence | Host prototype | Metadata counter only; no framebuffer or scanout |
| Normalized multi-touch event model | Host prototype | Validates and converts synthetic events |
| Rotation-aware coordinate conversion | Host prototype | Logical coordinates only |
| Moto G60 panel identification | Research | Kernel DTS supports 1080×2460 Tianma/ILI7807S configuration; exact module SKU unconfirmed |
| Moto G60 touch-controller identification | Research | Kernel DTS says ILITEK over SPI; Android gesture code uses an NVT-labelled sysfs path, which does not independently identify the IC |
| Physical display/touch driver | Not implemented | Requires verified hardware and kernel interfaces |

See [display/touch prototype](docs/architecture/display-touch-prototype.md).


## Hardware evidence ledger

| Feature | Status | Notes |
|---|---|---|
| Source-backed hardware evidence ledger | Host prototype | Separates source observations from physical-hardware conclusions |
| Evidence-ledger validator | Host prototype | Checks source references, statuses, required fields and duplicate IDs |
| Touch-controller physical identity | Unresolved | ILITEK kernel binding and NVT-labelled Android gesture interface remain unreconciled |

See [hardware evidence ledger documentation](docs/porting/hardware-evidence-ledger.md).


## Display/touch profile integration

| Feature | Status | Notes |
|---|---|---|
| Synthetic display profile loader | Host prototype | Loads the synthetic fixture into the metadata-only display subsystem |
| Hardware evidence attachment | Host prototype | Displays source observations without promoting uncertain identities |
| Touch controller and LCD module identity | Unresolved | Physical component identities remain unverified |

See [display/touch profile integration](docs/architecture/display-touch-profile-integration.md).


## Display event pipeline

| Feature | Status | Notes |
|---|---|---|
| Ordered display mode events | Host prototype | Synchronous host-side event dispatch |
| Logical rotation events | Host prototype | Rotation-aware synthetic touch coordinates |
| Touch input event flow | Host prototype | Normalized points transformed to logical pixels |
| Frame metadata events | Host prototype | Advances metadata counter only; no framebuffer or scanout |

See [display event pipeline documentation](docs/architecture/display-event-pipeline.md).


## Graphical compositor prototype

| Feature | Status | Notes |
|---|---|---|
| Rectangular scene surfaces | Host prototype | Metadata for background, status bar, windows and overlays |
| Z-order and visibility | Host prototype | Visible surfaces composed into ordered snapshots |
| Touch hit testing | Host prototype | Synthetic touch selects the topmost surface |
| Pixel rendering / GPU / framebuffer | Planned | No rasterization or physical display output |

See [graphical compositor prototype](docs/architecture/graphical-compositor-prototype.md).


## System shell prototype

| Feature | Status | Notes |
|---|---|---|
| Home screen and app shortcuts | Host prototype | In-process app selection model only |
| Status bar | Host prototype | Clock and simulated connectivity / demo battery values |
| Quick Settings | Host prototype | Wi-Fi, Bluetooth and Do Not Disturb toggles are simulated |
| Notifications panel | Host prototype | In-memory notification records and dismiss operation |
| System app execution / hardware indicators | Planned | No OS process launch or physical device integration |

See [system shell prototype](docs/architecture/system-shell-prototype.md).


## Synthetic graphical renderer

| Feature | Status | Notes |
|---|---|---|
| Host-side SVG rendering | Host prototype | Converts shell snapshots into standalone vector images |
| Status bar, home tiles and panels | Host prototype | Renders simulated shell state with DarwinG60 styling |
| GPU / framebuffer / physical panel output | Planned | SVG generation is not a device graphics driver |

See [synthetic shell renderer documentation](docs/architecture/synthetic-shell-renderer.md).
