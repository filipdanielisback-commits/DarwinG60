# Device porting command reference

These commands are intended for local project metadata and planning. They do
not communicate with a phone, alter firmware, unlock a bootloader, flash
partitions, or install an operating system.

Run from the repository root.

## Current project commands

```sh
python tools/dg60_check.py
python tools/device_info.py
python tools/system_info.py
python tools/system_info.py --check
python -m unittest discover -s tests
```

## Porting workflow commands

The planned command-line interface is:

```sh
python tools/porting_plan.py list
python tools/porting_plan.py show hanoip
python tools/porting_plan.py check
```

- `list` lists device profiles present in the repository.
- `show <codename>` prints the profile's identity and research status.
- `check` checks the structure of device profile metadata.

These are repository-management commands only. They do not test hardware
compatibility or prove that a device can boot DarwinG60.

## Research checklist

For a new target, record the exact model and codename, gather reliable public
sources, document its boot architecture, and map required drivers. Unknown or
unverified fields must remain marked as unknown. Any future device-level
experiments require a separate safety and feasibility review; this project
does not provide firmware-modification or flashing instructions.
