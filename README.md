# DarwinG60

**Experimental ARM64 Darwin/XNU research for the Motorola Moto G60 (device codename: `hanoip`).**

DarwinG60 is an exploratory, open-source research project. Its long-term goal is to investigate what would be required to bring parts of the Darwin/XNU ecosystem to the Moto G60 platform. At this stage, it is a documentation and research project—not a working iOS port, not a bootable Darwin image, and not a replacement for Android.

> [!WARNING]
> No Darwin/XNU build, EFI loader, device driver set, or bootable image is currently provided by this repository. Do not flash experimental files or assume that an image is safe for your phone. Early development will focus on source research, emulation, documentation, and non-destructive testing.

## Project status

**Status: Research / pre-alpha**

- [x] Repository and project scope established
- [ ] Verify device hardware and boot-chain documentation
- [ ] Set up a reproducible research/build environment
- [ ] Investigate ARM64 Darwin/XNU boot requirements
- [ ] Prototype components in an emulator before device experiments
- [ ] Document Moto G60-specific hardware gaps
- [ ] Evaluate whether any safe, meaningful device-side prototype is feasible

Nothing in the unchecked list should be interpreted as implemented.

## Goals

- Study the ARM64 Darwin/XNU boot process and its platform assumptions.
- Document the Moto G60 (`hanoip`) hardware and existing open-source device support.
- Explore boot-chain and EFI concepts in a controlled, reversible development environment.
- Keep Android preservation and recovery considerations central to any future device research.
- Publish reproducible notes, source changes, and test results.

## Non-goals and limitations

- This project does **not** contain or distribute Apple's proprietary iOS components.
- It does **not** claim to run iOS 18 or any version of iOS on the Moto G60.
- It does **not** promise that XNU can be made to boot on this device.
- It does **not** provide instructions or images for bypassing device security or performing risky flashing.
- A menu, kernel build, or image file alone would not demonstrate working hardware support.

Darwin/XNU is not the same thing as the complete iOS operating system. iOS also depends on proprietary frameworks, services, drivers, signing, and hardware integration that are outside this repository's scope.

## Device target

| Item | Value |
|---|---|
| Device | Motorola Moto G60 |
| Device codename | `hanoip` |
| CPU architecture | ARM64 (to be confirmed against reliable device documentation) |
| Project phase | Research and feasibility |
| Current bootable release | None |

Hardware details will be added only after they are checked against reliable documentation or measured and recorded.

## Repository layout

```text
DarwinG60/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── ROADMAP.md
├── SECURITY.md
└── docs/
    ├── architecture.md
    ├── boot-process.md
    └── compatibility.md
```

## Getting involved

Start with [CONTRIBUTING.md](CONTRIBUTING.md), then review the [roadmap](ROADMAP.md) and the documents in [docs/](docs/). Research notes should include links to primary sources and clearly distinguish confirmed facts from hypotheses.

## Licensing

Original project code and documentation are offered under the MIT License in [LICENSE](LICENSE). This license does not apply to third-party code, trademarks, firmware, or proprietary components. Any future third-party source imports must retain their original licenses and notices.

Apple, iOS, and Darwin are trademarks or products of their respective owners. This is an independent community research project and is not affiliated with or endorsed by Apple or Motorola.

## Host-side prototype

The repository includes a harmless Python boot-menu simulation and repository checker. These run on a host environment and do not interact with a phone:

```sh
python3 tools/menu_demo.py
python3 tools/dg60_check.py
python3 -m unittest discover -s tests -v
```

The menu is a user-interface concept only. It cannot launch Android, load XNU, or change device boot settings. See [the menu design](docs/design/boot-menu.md) and [development guide](docs/development.md).

## Device research layer

The first structured target profile is stored in `devices/hanoip/`:

- `device.json` records published Moto G60 hardware information.
- `compatibility.json` separates documented hardware facts from components that DarwinG60 has not implemented.
- `sources.md` records the references and confidence limits.

A read-only Python report tool is available:

```sh
python tools/device_info.py
python tools/device_info.py --json
python tools/device_info.py --check
```

The report and tests validate metadata only; they do not probe or modify a handset.

## ARM64 startup simulator

A host-side educational model describes a hypothetical ARM64 startup sequence:

```sh
python tools/arm64_simulator.py
python -m unittest discover -s tests -v
```

It models conceptual startup stages and validates caller-supplied illustrative memory ranges. It does not emulate ARM64 instructions, provide a real Moto G60 memory map, access firmware, or produce a bootable artifact. See [the simulator documentation](docs/arm64-simulator.md).

## Automated host checks

GitHub Actions runs the Python unit tests, validates the device profile, and runs the repository checker on pushes and pull requests. A green check means the host-side project checks passed, not that DarwinG60 boots on hardware.

See [the device layer design](docs/device-layer.md) for details.


## System information dashboard

The integrated read-only dashboard combines device metadata, compatibility
counts, implementation flags, and the conceptual ARM64 startup sequence:

```sh
python tools/system_info.py
python tools/system_info.py --json
python tools/system_info.py --check
```

It reads repository files only. It does not query or modify a connected phone.
See [system information documentation](docs/system-information.md).

## Feature tracker and core architecture

See [WORKING.md](WORKING.md) for the public feature tracker, including planned Wi-Fi, battery reporting, graphical interface, status bar, Control Center, kernel, and Moto G60 hardware support. The current kernel catalogue and service registry are host-side architecture prototypes only; they are not a running kernel or hardware services.

Core design notes: [kernel subsystem architecture](docs/architecture/core-subsystems.md) and [service architecture](docs/services.md).

## Porting to other devices

DarwinG60 has a documented [multi-device porting plan](docs/porting/README.md)
and [host-side porting commands](docs/porting/commands.md). The Moto G60 remains
the primary target. Every additional device needs its own hardware research and
compatibility assessment; UEFI must not be assumed to exist on every Android
device. See [WORKING.md](WORKING.md) for the porting tracker.

## Device compatibility database

The host-side device catalogue can list profiles, inspect a device, display a
component compatibility matrix, and check metadata consistency. See
[compatibility database documentation](docs/porting/compatibility-database.md).
It does not probe hardware or establish that a port works.



## Device profile generator

Create starter metadata for a future device with
`python tools/generate_device_profile.py --codename example-device --manufacturer Example --model "Example Phone"`.
See [the generator guide](docs/porting/profile-generator.md). The tool creates
research files only and does not add device support.

## Hardware readiness report

Run `python tools/hardware_readiness.py hanoip` to summarize six areas of
device research and implementation gaps. See
[hardware readiness documentation](docs/porting/hardware-readiness.md).
The report reads repository metadata only and does not test hardware.

## Driver architecture registry

DarwinG60 now tracks seven planned driver areas for each device: display and
touchscreen, GPU, Wi-Fi and Bluetooth, battery and charging, audio, sensors,
and storage. Inspect the Moto G60 registry with
`python tools/driver_registry.py show hanoip` and validate it with
`python tools/driver_registry.py check hanoip`. See
[driver registry documentation](docs/architecture/driver-registry.md).
These are planning records, not working drivers or verified hardware support.

## Moto G60 hardware research

The initial seven-category hardware research dossier is available at
[devices/hanoip hardware research](docs/porting/hanoip-hardware-research.md).
It records sourced platform facts, conflicting specifications, unknown
component identifiers, and driver research gaps. It does not claim working
DarwinG60 drivers.
