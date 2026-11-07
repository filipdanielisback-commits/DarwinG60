# Display/touch research profile integration

## Purpose

The profile loader joins the existing synthetic display/touch fixture with
source-backed research summaries. It does not merge a source observation into
a hardware configuration.

## Behavior

- Loads only the explicitly synthetic 800x600 example fixture.
- Creates the existing metadata-only DisplayTouchSubsystem from its modes.
- Validates the hardware evidence ledger before attaching display/touch claim
  summaries.
- Preserves unresolved touchscreen and LCD module identities in reports.
- Rejects a fixture that claims a real device, a hardware identifier, or
  controller/bus/interrupt details.

## Run

    python tools/display_touch_profile.py

Host-side tests:

    python -m unittest discover -s tests -v

No hardware is detected, probed, initialized, or modified. This is not a
display driver, input driver, compositor, framebuffer, or bootable system.
