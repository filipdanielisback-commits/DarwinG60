# Boot menu concept

## Purpose

The first DarwinG60 menu prototype is a host-side simulation of the proposed
selection screen. It is intended to help us discuss the user experience and
separate future boot paths conceptually.

## Proposed entries

| Entry | Intended meaning | Current implementation |
|---|---|---|
| Darwin / XNU research | Future experimental Darwin path | Informational placeholder only |
| Android | Preserve access to the original OS | Informational placeholder only |
| Project information | Display project status | Text in simulator |

## Important distinction

The Python prototype is **not an EFI application or a bootloader**. It does not
read or write device partitions, alter boot configuration, launch Android, or
load XNU. A real boot design would require separate platform research and
careful validation before any device-side work.

## Future design questions

- What firmware interfaces does the target actually expose?
- What boot stages and image formats are supported?
- Can an alternative boot environment coexist with the existing boot flow?
- What is the recovery plan if an experiment fails?
- Which parts can be tested in an emulator first?

These questions remain open. No compatibility claim should be made until
supported by evidence and reproducible tests.
