# DarwinG60 System Information

The integrated dashboard combines the checked-in device profile, compatibility
inventory, project implementation flags, and conceptual startup sequence.

## Run

From the repository root:

```sh
python tools/system_info.py
python tools/system_info.py --json
python tools/system_info.py --check
python -m unittest discover -s tests -v
```

## Output

The text view summarizes the Moto G60 research target and explicitly labels
startup stages as simulated. The JSON view is intended for future scripts and
simple front ends. The check option returns a non-zero exit code when metadata
validation fails.

## Boundaries

This is a read-only host-side report. It reads repository files only. It does
not query Android, inspect live hardware, read device memory, or alter any
phone settings. A displayed CPU or SoC profile is project metadata, not a live
hardware measurement. A successful metadata check does not indicate that XNU
or a bootloader works on the device.
