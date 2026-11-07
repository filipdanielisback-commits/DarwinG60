# Moto G60 device profile: hanoip

This directory records public, research-level information for the Motorola Moto G60 and its shared Moto G40 Fusion device family.

## Files

- `device.json` — structured device metadata.
- `compatibility.json` — current DarwinG60 implementation and evidence matrix.
- `sources.md` — references and confidence notes.

## Important distinction

A published hardware specification is not proof that DarwinG60 can use that hardware. The compatibility matrix deliberately separates documented hardware facts from project implementation status.

At this stage, DarwinG60 has **no XNU kernel port, bootloader, device drivers, or bootable image**. The profile is intended for research tools and planning only.

## Run the profile report

From the repository root:

```sh
python tools/device_info.py
python tools/device_info.py --json
python tools/device_info.py --check
```

The commands read repository files only. They do not communicate with or modify a phone.
