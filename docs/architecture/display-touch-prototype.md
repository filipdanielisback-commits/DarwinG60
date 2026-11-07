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

A deeper review of an archived hanoip kernel tree found a Tianma/ILI7807S
panel configuration labelled `mipi_mot_vid_tm_ili7807s_fhd_678`, with 1080 ×
2460 timing and 60/120 Hz mode support. The exact retail LCD module SKU and
revision are still unverified.

The same tree declares `compatible = "tchip,ilitek"` on the QUPv3 SE6 SPI bus,
and its matching driver identifies the ILITEK family. The exact ILITEK IC
part number is not established. An Android `BoardConfig.mk` separately
references an `NVT-ts` tap-to-wake sysfs path, conflicting with the ILITEK
DTS declaration. This may reflect different revisions or stale configuration
and must be resolved before treating the touch family as definitive.

Sources: [panel DTS](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip/blob/main/arch/arm64/boot/dts/qcom/hanoi-panel.dtsi), [panel mode definition](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip/blob/main/arch/arm64/boot/dts/qcom/dsi-panel-mot-tianma-ili7807s-678-1080x2460-video.dtsi), [touch DTS](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip/blob/main/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-touchscreen.dtsi), [matching ILITEK driver](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip/blob/main/drivers/input/touchscreen/ilitek_v3_mmi/ilitek_v3_qcom.c), and [Android BoardConfig](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/BoardConfig.mk).

The kernel source is an archived community tree, not an official Motorola
hardware bill of materials. Its identifiers are source-level evidence only.
The moto-hanoip organization is also archived (March 23, 2024).

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
