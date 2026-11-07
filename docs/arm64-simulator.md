# ARM64 Startup Simulator

The simulator is a host-side educational model of a possible ARM64 startup
sequence. It is not an ARM emulator, firmware implementation, bootloader, or
kernel.

## Run

From the repository root:

```bash
python tools/arm64_simulator.py
python -m unittest discover -s tests -v
```

## What it models

- A conceptual sequence from reset through userspace.
- A CPU profile using currently documented project metadata.
- Validation of illustrative memory-region ranges for overlap and invalid sizes.

## Important limitations

- It executes ordinary Python on the host computer.
- It does not execute ARM64 instructions or inspect the Moto G60.
- The memory-region validator accepts values supplied by the caller; it does
  not provide a real Moto G60 physical memory map.
- It does not access firmware, the bootloader, partitions, or device storage.
- Every stage is labelled `SIMULATED`; no bootable artifact is produced.

Physical memory layouts, firmware interfaces, and kernel handoff details remain
research questions until supported by reliable device-specific documentation.
