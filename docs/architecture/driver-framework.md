# Host-side driver framework prototype

DarwinG60 now has a first driver-framework **model** for research and tests.

## What it does

- Registers declarative driver descriptors.
- Matches supplied device metadata by bus plus vendor/device ID or compatible string.
- Produces explicit simulated bindings.
- Rejects duplicate registrations and mismatched bindings.

## What it does not do

This is not a kernel driver framework and does not enumerate a physical bus,
map registers, allocate DMA, receive interrupts, load firmware, communicate
with a device, or control hardware. The test identities are synthetic fixtures,
not Moto G60 component IDs.

## Why start here?

A common matching and lifecycle model gives future driver work a consistent
place to record supported identifiers and test matching logic. Actual device
identifiers must be backed by reliable, device-specific evidence before they
are added. A future kernel implementation will need a real platform/bus model,
memory and interrupt abstractions, concurrency rules, power management, and
a documented hardware interface.

## Example (host-side only)

```python
from darwing60.driver_framework import (
    DeviceDescriptor, DriverDescriptor, DriverManager,
)

manager = DriverManager()
manager.register(DriverDescriptor(
    name="example-sensor",
    buses=("i2c",),
    compatibles=("example,sensor-v1",),
))
fixture = DeviceDescriptor(
    name="test fixture",
    bus="i2c",
    compatible=("example,sensor-v1",),
)
print(manager.find_matches(fixture))
binding = manager.simulate_bind(fixture, "example-sensor")
print(binding.state.value)  # bound_simulated
```

All identities in this example are invented test fixtures. Do not interpret
them as hardware discoveries or working Moto G60 support.
