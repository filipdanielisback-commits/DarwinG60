# Security and safe testing

DarwinG60 is experimental research software. No device-ready image or supported installation procedure is currently provided.

## Reporting a concern

Please do not publish secrets, access tokens, private device identifiers, or personal information in an issue. For a security-sensitive report, contact the repository maintainer privately through GitHub.

## Safe development expectations

- Prefer source review, documentation, emulation, and non-destructive tests.
- Do not test unverified images on a primary or personal device.
- Do not publish instructions that could leave a device unusable without a well-documented, supported recovery path.
- Keep third-party code and dependencies traceable to their original sources.
- Treat downloaded binaries and firmware as untrusted unless their origin and integrity are verified.

## Status

There is no supported bootable release. The project does not currently provide device flashing guidance or a guarantee of recovery from experimental modifications.
