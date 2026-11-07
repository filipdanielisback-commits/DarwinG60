# Hardware readiness assessment

The hardware readiness tool summarizes evidence and missing implementation
notes in six areas:

1. CPU architecture and platform documentation.
2. Boot architecture and firmware research.
3. Display, touch, and GPU research.
4. Wi-Fi and Bluetooth driver status.
5. Battery and power-management status.
6. Kernel and graphics readiness.

## Command

Run from the repository root:

```sh
python tools/hardware_readiness.py hanoip
```

The report reads the device's `device.json` and `compatibility.json`. It
does not inspect a physical device, run a driver, validate firmware, build a
kernel, or certify compatibility.

## Status meanings

- `documented`: a source note exists for the hardware or platform fact; this
  does not mean DarwinG60 has implemented it.
- `unknown`: the profile lacks enough evidence.
- `not_implemented`: the profile explicitly records no DarwinG60 implementation.
- `not_tested`: an implementation or hypothesis has not been validated.

## Improving the report

When research is completed, update the device compatibility profile with
specific source references and concise evidence notes. Do not change a status
to working merely because a specification is known. Driver readiness requires
an implementation and appropriate testing; hardware support requires
documented validation on the named device.

The report is a planning aid, not a score predicting successful boot.
