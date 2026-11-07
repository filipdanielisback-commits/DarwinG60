# Display and touch interface prototype

## Status

**Host-side synthetic prototype only.** This is not a kernel driver, display
server, framebuffer, DRM/KMS implementation, touchscreen driver, or Moto G60
hardware support.

## Interfaces

- DisplayMode: validated logical width, height and refresh-rate metadata.
- PanelProfile: explicitly synthetic mode catalogue; rejects hardware claims
  and unverified component identifiers.
- DisplayTouchSubsystem: mode selection, synthetic frame sequence metadata,
  and normalized touch-coordinate conversion.
- TouchFrame and TouchPoint: timestamped, validated multi-pointer events.
- Rotation-aware conversion from normalized coordinates to logical pixels.

The frame method records metadata only; it does not allocate a framebuffer,
draw pixels, drive a panel, or synchronize with a display controller.

## Synthetic fixture

examples/display-touch-synthetic.json is deliberately 800 × 600. These
numbers are test data and must never be mistaken for Moto G60 panel timings.

## Moto G60 research status

The public hanoip Android device tree has a lineagehw/touch directory and
device-specific Android configuration. This establishes that the Android
tree contains touch integration code, but does not identify the physical
touch-controller part number or establish a reusable Darwin driver.

Public Moto G60-family summaries conflict on display resolution:
- 1080 × 2460 in one community device tree.
- 1080 × 2400 in the TeamWin device tree.

The exact panel model, panel revision, DSI timing set, touch-controller model,
bus address, interrupt/reset wiring, and firmware requirements remain
**unverified**. The moto-hanoip organization is archived (March 23, 2024),
so its contents are historical references rather than active maintenance.

## Next research evidence needed

1. Exact regional model number and board revision.
2. Device-specific panel compatible/model and display timing data.
3. Touch-controller compatible/model, bus and device-tree properties.
4. Licensing and provenance of reusable source or firmware.
5. Independent corroboration before promoting an identifier to confirmed.

## Future kernel-facing boundary

A real implementation would need a kernel display pipeline, panel power and
mode abstractions, an input subsystem, interrupt and bus abstractions, timing,
synchronization, error handling, and hardware-specific drivers. None of those
hardware-facing pieces is implemented here.
