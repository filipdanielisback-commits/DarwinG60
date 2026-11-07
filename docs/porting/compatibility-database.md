# Device compatibility database

The `devices/<codename>/` directories are the source of truth for per-device
research. Each complete record contains `device.json` and
`compatibility.json`. The catalogue reader in
`src/darwing60/device_catalog.py` loads these records and produces a
component matrix.

## Commands

Run from the repository root:

```sh
python tools/device_catalog.py list
python tools/device_catalog.py show hanoip
python tools/device_catalog.py matrix hanoip
python tools/device_catalog.py check
```

These commands inspect repository files only. They do not probe a phone or
prove that any component works.

## Adding another device profile

Create a new `devices/<codename>/` directory with:
- `device.json` for identity and sourced reference specifications;
- `compatibility.json` for per-component research status;
- `sources.md` for source links and verification notes;
- `README.md` for known limitations and the research summary.

Use only evidence-backed values. Mark unverified properties as unknown. Do not
copy the Moto G60 hardware values into another device's profile.

## Status vocabulary

- `documented`: a public source describes the component or platform; this
  does not mean DarwinG60 supports it.
- `unknown`: research is incomplete.
- `not_implemented`: DarwinG60 has no implementation.
- `not_tested`: an implementation exists but has not been validated.

A future `working` status requires separate documented test evidence and
hardware validation. Catalogue validation checks metadata consistency only.
