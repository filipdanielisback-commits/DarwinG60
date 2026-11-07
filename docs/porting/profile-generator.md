# Device profile generator

The profile generator creates a starter research folder for a new device. It
writes four repository files: `device.json`, `compatibility.json`,
`sources.md`, and `README.md`.

## Command

Run from the repository root:

```sh
python tools/generate_device_profile.py --codename example-device --manufacturer Example --model "Example Phone"
```

Choose a short lowercase codename containing letters, numbers, hyphens, or
underscores. The generator refuses to overwrite an existing device directory.

## What it deliberately does not do

- It does not search for or invent device specifications.
- It does not claim the device is compatible.
- It does not probe, unlock, flash, or otherwise modify a phone.
- It does not create a bootloader, kernel, firmware image, or driver.

After generation, research the exact model and fill in values only when
supported by reliable public sources. Keep unknown values null or marked
unknown. Update the compatibility matrix only when evidence supports a status.
