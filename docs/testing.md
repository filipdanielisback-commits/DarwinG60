# Testing and validation

## Repository checker

DarwinG60 includes a host-side repository checker at `tools/dg60_check.py`.

Run it from any directory with Python 3:

```sh
python3 tools/dg60_check.py
```

The checker verifies that core project documents exist and that the README clearly identifies the target and current non-bootable research status.

It does not compile XNU, inspect a connected phone, validate firmware, or prove hardware compatibility. A passing result means only that these basic repository checks passed.

## Test philosophy

- Prefer host-side tests and emulation.
- Never treat a successful documentation check as evidence of a bootable system.
- Keep test output and exact source revisions with research notes.
- Do not run unverified builds on a personal device.
