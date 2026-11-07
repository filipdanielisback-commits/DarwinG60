# DarwinG60 device layer

## Purpose

The device layer separates published device facts from DarwinG60 implementation claims. It gives future research code one structured source for the target device's identity and a separate matrix for what is known, unknown, or not implemented.

## Current structure

- `devices/hanoip/device.json`: descriptive hardware profile.
- `devices/hanoip/compatibility.json`: evidence and implementation matrix.
- `devices/hanoip/sources.md`: references and confidence notes.
- `src/darwing60/device_profile.py`: read-only profile loader, report builder and metadata validator.
- `tools/device_info.py`: command-line interface.
- `tests/test_device_profile.py`: automated metadata tests.

## Design rules

1. Never infer a driver from a marketing specification.
2. Keep unknown low-level platform details explicitly unknown.
3. Distinguish community documentation from vendor documentation.
4. Keep device access out of the initial development workflow.
5. A passing metadata test means the files are structurally consistent; it does not mean the hardware is supported.

## Next research questions

- Which public platform documentation can establish the exact SoC and board revision?
- Which device-tree details are descriptive and which depend on proprietary firmware?
- What is the minimum host-side model needed to explore ARM64 platform initialization without touching a handset?
