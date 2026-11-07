# Hardware evidence ledger

The hardware-evidence.json file is a source-observation ledger for Moto G60
(hanoip). It separates what a public source file says from claims about the
physical handset.

## Status meanings

- source_observed: the cited source contains the described declaration or
  configuration. This does not prove the physical component in every variant.
- provisional: evidence supports a working hypothesis, but important
  correlation remains.
- unresolved: available sources do not establish the requested identity.
  An unresolved entry may correctly have no sources.

## Current display/touch ledger

The archived kernel DTS contains a Tianma/ILI7807S-labelled panel
configuration. The Android gesture configuration references an NVT-labelled
sysfs interface, while the archived kernel DTS declares an ILITEK-family SPI
binding. The ledger keeps these as separate source observations and leaves
the physical touch controller unresolved.

## Validation

src/darwing60/hardware_evidence.py validates required fields, status values,
source URLs, duplicate identifiers, and the rule that source-observed or
provisional claims require citations. Unresolved claims are allowed to have
no source because absence of evidence is recorded honestly.

Run host-side tests with:

    python -m unittest discover -s tests -v

This validator reads JSON only. It does not inspect, probe, configure, or
modify a phone, and a valid ledger is not hardware validation.
