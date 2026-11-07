# Driver Architecture Registry

DarwinG60 tracks seven device-facing driver areas in a per-device
`drivers.json` file:

1. Display and touchscreen
2. GPU
3. Wi-Fi and Bluetooth
4. Battery and charging
5. Audio
6. Sensors
7. Storage

Each entry records its scope, hardware identification notes, implementation
status, evidence references, tests, and open research gaps.

## Commands

From the repository root:

```sh
python tools/driver_registry.py show hanoip
python tools/driver_registry.py check hanoip
python tools/driver_registry.py template example-device
```

The template command prints starter JSON; it does not create a device profile.
The saved registry is `devices/hanoip/drivers.json`.

## Status policy

- `planned`: category identified; work has not started.
- `research`: evidence gathering and interface study.
- `prototype`: a host-side or isolated prototype exists; not proof of a device driver.
- `not_tested`: implementation exists but has not been validated on target hardware.
- `hardware_tested`: reserved for a reproducible, documented test on the named device.

Do not mark a driver as hardware-tested based on a specification, mockup, or
host-side test. A listed chipset does not establish driver availability.
Evidence entries should point to trustworthy public documentation or project
artifacts. Unknown hardware must remain explicitly unknown.

This registry is a planning and documentation tool. It does not access the
phone, control radios, read battery state, access storage, modify firmware,
or provide working drivers. DarwinG60 currently has no functional device
drivers for the seven categories.
