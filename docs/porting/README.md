# Porting to another device

DarwinG60 currently targets the Motorola Moto G60 (`hanoip`). This directory
defines a repeatable research process for evaluating additional devices. A
new device is a separate engineering target, not simply a renamed Moto G60
configuration.

## Porting status

No second device is currently supported. This plan is documentation and
host-side metadata work only. It does not unlock, flash, repartition, or modify
a phone.

## What must be researched for each device

1. **Identity and documentation** — manufacturer, exact model, codename,
   SoC family, architecture, and trustworthy public hardware references.
2. **Boot architecture** — documented boot chain, firmware interfaces, and
   whether a UEFI-compatible environment is actually present or would need a
   separately engineered solution. Do not assume every Android phone has UEFI.
3. **Kernel feasibility** — CPU support, memory layout documentation, kernel
   baseline research, and licensing constraints.
4. **Drivers** — display, touch, storage, USB, networking/Wi-Fi, Bluetooth,
   audio, battery/charging, sensors, and GPU.
5. **Userspace and graphics** — display stack, input, service interfaces,
   shell, status bar, control center, and settings.
6. **Validation plan** — define non-destructive host tests first, then a
   separately reviewed hardware validation plan.

## UEFI is not a universal requirement

Some devices expose UEFI, some use vendor-specific boot firmware, and some
Android devices use boot flows that do not provide a conventional UEFI
environment. The correct approach is to document and verify the target's
actual boot architecture before designing a loader. Do not label a device
"UEFI supported" based on guesswork.

## Device profile structure

Each candidate gets a directory under `devices/<codename>/` containing:
- `device.json` — identity and reference specifications;
- `compatibility.json` — researched subsystem compatibility;
- `sources.md` — links and notes supporting hardware claims;
- `PORTING.md` — device-specific gaps and research decisions.

Keep unknown values explicitly unknown. A profile is not evidence of a working
port.

## Current target

See [Moto G60 / hanoip](../../devices/hanoip/README.md). It remains the primary
research target until another device has a reviewed profile and a feasible,
documented development path.
