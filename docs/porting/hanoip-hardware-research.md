# Moto G60 (hanoip) Hardware Research Dossier

**Research status:** Initial public-source review  
**Target:** Motorola Moto G60 / shared hanoip device family  
**Important:** This is desk research from public documentation and community source repositories. It is not a physical-device inspection, driver validation, or certification of DarwinG60 compatibility.

## Executive findings

The Moto G60 is consistently identified by community device trees as part of the `hanoip` family, shared with the Moto G40 Fusion. The platform is identified as Qualcomm Snapdragon 732G, with Kryo 470 CPU cores and Adreno 618 graphics. The community device tree also lists 4/6 GB RAM, 64/128 GB storage variants, microSD support, a 6000 mAh battery, and a 120 Hz IPS LCD.

Some public sources disagree on display dimensions/resolution (1080 × 2460 versus 1080 × 2400, and 6.8 versus 6.81 inches). Treat the exact panel configuration as **unresolved** until a primary Motorola document or device-specific panel source is found. Do not hard-code the disputed values into a driver.

## Source register

| ID | Source | What it supports | Limitations |
|---|---|---|---|
| S1 | [Qualcomm Snapdragon 732G platform](https://www.qualcomm.com/smartphones/products/7-series/snapdragon-732g-mobile-platform) | Kryo 470, Adreno 618, up to 2.3 GHz, FastConnect 6200, Wi-Fi 6-ready features, Bluetooth 5.1, 8 nm, SM7150-AA | Platform-level capability, not proof of the exact radio module, firmware, board wiring, or enabled features in every handset |
| S2 | [Bhawesh hanoip Android device tree](https://github.com/bhawesh2002/android_device_motorola_hanoip) | Shared Moto G40 Fusion/G60 family, codename, community hardware summary, separate audio/Bluetooth/touch/Wi-Fi configuration areas | Community-maintained; not an official Motorola specification. Tree presence is not proof of DarwinG60 driver support |
| S3 | [Motorola SM6150 developers device tree](https://github.com/motorola-sm6150-devs/device_motorola_hanoip) | Independent community device-tree identification of Moto G40 Fusion/Moto G60 (hanoip) | Android device configuration, not a hardware validation report |
| S4 | [Motorola SM6150 developers Android device tree](https://github.com/motorola-sm6150-devs/android_device_motorola_hanoip) | Additional device-specific Android configuration and proprietary component inventory references | Proprietary files may be blobs; names alone do not establish source availability or license to reuse |
| S5 | [CosmicFresh-Hanoip kernel repository](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip) | A community CAF-rebased Linux kernel source repository described for Moto G40 Fusion/G60; includes standard kernel driver areas | Archived in April 2023; Linux/Android kernel source is not an XNU port and does not provide ready-made DarwinG60 drivers |
| S6 | [Motorola official specifications document](https://p1-ofp.static.pub/MOTO/Columbia/Motorola_Informacion_fichas_tecnicas_2024.99ff3703fd4516c1.pdf) | Motorola-published specification material; used as a primary-source lead for model-level specifications | The document should be checked against the exact regional model number before treating variant-specific values as final |
| S7 | [PhoneArena Moto G60 overview](https://www.phonearena.com/phones/Motorola-Moto-G60_id11684) | Secondary cross-check for general model specifications | Secondary source; not sufficient for low-level driver identification |

## Findings by driver category

### 1. Display and touchscreen

**Known from device-specific archived kernel DTS:** `hanoi-panel.dtsi` includes `dsi-panel-mot-tianma-ili7807s-678-1080x2460-video.dtsi`. The panel configuration is labelled `mipi_mot_vid_tm_ili7807s_fhd_678`, declares 1080 × 2460 timing, and the hanoip overlay enables dynamic 60/120 Hz modes. This is substantially stronger evidence for the 1080 × 2460 configuration than generic spec summaries, but the DTS label is not necessarily the exact LCD module SKU or glass part number.

The same kernel tree's `sdmmagpie-hanoi-touchscreen.dtsi` declares a touchscreen node with `compatible = "tchip,ilitek"` on the QUPv3 SE6 SPI bus. It specifies a 12 MHz maximum SPI frequency and reset/interrupt GPIO references. The matching kernel driver source defines `DTS_OF_NAME` as `tchip,ilitek` and identifies itself as an ILITEK touch IC driver. This supports an ILITEK driver-family identification, **not an exact controller IC model**.

**Source discrepancy:** The Android device tree's `BoardConfig.mk` separately sets the tap-to-wake sysfs path to `/sys/class/touchscreen/NVT-ts/double_click`. That NVT-labelled path does not match the ILITEK SPI node in the archived kernel DTS. These may represent different source revisions, branches, or stale configuration; do not silently choose one as definitive. Resolve against the exact regional handset/board revision before promoting the touch-controller identification.

**Still unknown:** Exact LCD module SKU/revision, exact ILITEK controller part number, whether all Moto G60 revisions use the same panel/touch assembly, and the firmware/licensing requirements for the touch implementation.

**DarwinG60 implication:** Record the panel configuration as a device-tree-supported lead and the touch IC family as a provisional source finding. No physical display or touch driver is implemented, and no proprietary firmware or Android code is reused.

### 2. GPU

**Known:** Qualcomm identifies the Snapdragon 732G platform GPU as Adreno 618. Qualcomm lists platform graphics API capabilities.

**Unknown:** Exact GPU firmware package/version used by the target build, kernel/userspace interface compatibility, memory-management requirements, and whether any reusable open driver path covers the exact device configuration.

**DarwinG60 implication:** The GPU model is documented; working acceleration is not. Research the open graphics stack and licensing before designing a backend. Do not treat Android userspace blobs as portable drivers.

### 3. Wi-Fi and Bluetooth

**Known:** Qualcomm's Snapdragon 732G platform page describes FastConnect 6200 and platform-level Wi-Fi 6-ready features and Bluetooth 5.1. The community hanoip tree has separate Wi-Fi and Bluetooth configuration areas.

**Unknown:** Exact handset radio/chip module and revision, board connection, regulatory configuration, firmware filenames/versions, coexistence setup, and which platform features are actually enabled on this model/region.

**DarwinG60 implication:** Record FastConnect 6200 as a platform-level lead, not as a verified exact handset component. No DarwinG60 wireless stack or driver exists.

### 4. Battery and charging

**Known:** Community device-tree specification summaries list a non-removable 6000 mAh battery.

**Unknown:** Exact battery pack/thermistor identifiers, fuel-gauge and charger IC models, charging protocol configuration, power-supply interfaces, thermal policy, and device-specific telemetry mapping.

**DarwinG60 implication:** Capacity is a model-level reference only. It does not tell us how to read charge percentage or control charging. No battery telemetry or charging driver exists.

### 5. Audio

**Known:** The hanoip community device tree contains an audio configuration area, indicating device-specific Android audio configuration exists.

**Unknown:** Exact codec/PMIC audio part, amplifier, microphone routing, speaker routing, DSP firmware dependencies, calibration data, and which pieces are proprietary.

**DarwinG60 implication:** Do not guess a codec from the SoC. The next research task is to trace public configuration references and distinguish hardware identifiers from Android-specific policy/blobs. No DarwinG60 audio driver exists.

### 6. Sensors

**Known:** The community device tree contains location/GPS-related configuration areas. Qualcomm lists platform-level location and sensing capabilities for Snapdragon 732G.

**Unknown:** Exact physical sensor inventory and part numbers (accelerometer, gyroscope, proximity, ambient light, compass, etc.), bus topology, calibration, and which sensors are fitted to each regional variant.

**DarwinG60 implication:** Platform capability is not a confirmed handset sensor bill of materials. No DarwinG60 sensor driver exists.

### 7. Storage

**Known:** Community device-tree summaries list 64/128 GB storage variants and microSD expansion.

**Unknown:** Exact internal storage technology/controller and revision, partition layout for each model/region, filesystem choices, and card-reader interface details.

**DarwinG60 implication:** Capacity does not identify the storage controller. Keep controller and partition details unknown. No DarwinG60 storage driver or filesystem integration exists.

## Confidence and unresolved items

| Item | Finding | Confidence |
|---|---|---|
| Device family/codename | Moto G60 belongs to hanoip family with Moto G40 Fusion | High (multiple community trees) |
| SoC platform | Snapdragon 732G / Qualcomm SM7150 family | High |
| CPU | Kryo 470, up to 2.3 GHz | High at platform level |
| GPU | Adreno 618 | High |
| Platform connectivity | FastConnect 6200; platform page lists Wi-Fi 6-ready and Bluetooth 5.1 features | High at platform level; exact handset module unconfirmed |
| Display exact resolution/panel | Conflicting public summaries; panel part number not identified | Low / unresolved |
| Touch-controller model | Not identified | Unknown |
| Audio codec | Not identified | Unknown |
| Sensor part numbers | Not identified | Unknown |
| Battery capacity | 6000 mAh in community summaries | Medium-high; verify exact regional model |
| Charging/fuel-gauge IC | Not identified | Unknown |
| Storage technology/controller | Not identified | Unknown |

## Recommended next research work

1. Identify the exact regional model number and hardware revision represented by the target `hanoip` profile.
2. Review the public device-tree configuration files for hardware identifiers and cite exact file paths/lines in follow-up research.
3. Compare those identifiers with the archived community kernel source and upstream Linux driver documentation.
4. Separate open-source code, Android-specific configuration, and proprietary firmware/blobs; review licenses before any reuse.
5. Keep every unknown explicitly unknown until supported by a primary or device-specific source.

## Driver implementation boundary

This dossier does not authorize or describe device flashing, bootloader changes, partition writes, firmware replacement, or physical-device modification. Initial implementation work should remain host-side: metadata parsers, interface specifications, mock devices, and tests. A real hardware driver requires a real kernel/platform foundation, verified interfaces, suitable licensing, and a safe, documented validation environment.

## Display/touch follow-up (2026-11-07)

A fresh public-source review confirms that the community hanoip Android tree
contains a `lineagehw/touch` integration directory. This is evidence of
Android-side touch integration, not proof of a physical controller identity
or a DarwinG60 driver. The moto-hanoip GitHub organization is marked archived
by its administrator (March 23, 2024).

The resolution conflict remains unresolved: the community device tree lists
1080 × 2460, while the TeamWin TWRP tree lists 1080 × 2400. The exact panel
part number, revision, DSI timings, touch-controller part number, bus address,
interrupt/reset wiring and firmware requirements have not been verified.

Sources:
- [Community hanoip device tree](https://github.com/bhawesh2002/android_device_motorola_hanoip)
- [TeamWin hanoip device tree](https://github.com/TeamWin/android_device_motorola_hanoip)
- [Archived moto-hanoip organization](https://github.com/moto-hanoip/)
- [Linux common touchscreen binding](https://android.googlesource.com/kernel/common/+/02d6eeedbc36d4b309d5518778071a749ef79c4e/Documentation/devicetree/bindings/input/touchscreen/touchscreen.yaml)

A synthetic host-side interface prototype now exists at
`src/darwing60/display_touch.py`. Its 800 × 600 fixture is invented test data,
not a proposed Moto G60 mode or panel configuration.


## Device-tree identifier follow-up (2026-11-07)

A deeper review of the archived `CosmicFresh-Hanoip` kernel repository found the following device-specific files:

- [`hanoi-panel.dtsi`](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip/blob/main/arch/arm64/boot/dts/qcom/hanoi-panel.dtsi) includes the Tianma/ILI7807S panel definition and enables dynamic 60/120 Hz modes.
- [`dsi-panel-mot-tianma-ili7807s-678-1080x2460-video.dtsi`](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip/blob/main/arch/arm64/boot/dts/qcom/dsi-panel-mot-tianma-ili7807s-678-1080x2460-video.dtsi) declares the panel label `mipi_mot_vid_tm_ili7807s_fhd_678` and 1080 × 2460 timing. This supports the 2460-pixel height in this kernel source, but does not prove the exact retail LCD module SKU.
- [`sdmmagpie-hanoi-touchscreen.dtsi`](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip/blob/main/arch/arm64/boot/dts/qcom/sdmmagpie-hanoi-touchscreen.dtsi) declares `compatible = "tchip,ilitek"` on SPI, with reset and IRQ GPIO properties.
- [`ilitek_v3_qcom.c`](https://github.com/Dark-Matter7232/CosmicFresh-Hanoip/blob/main/drivers/input/touchscreen/ilitek_v3_mmi/ilitek_v3_qcom.c) matches the same `tchip,ilitek` compatible string. The driver identifies the controller family as ILITEK but does not, from these declarations alone, establish the exact IC part number.
- [`BoardConfig.mk`](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/BoardConfig.mk) points tap-to-wake at `/sys/class/touchscreen/NVT-ts/double_click`, which conflicts with the ILITEK SPI device-tree declaration. This discrepancy is recorded as unresolved rather than assuming either source is universally correct.

The kernel repository is an archived community source, not an official Motorola hardware bill of materials. The evidence is therefore useful for source-level research but still needs correlation with the exact regional model and board revision. No kernel code, firmware, or Android blobs were copied into DarwinG60.


## Android touch-path discrepancy review (2026-11-07)

The Android device-tree repository was inspected beyond its directory listing:

- `lineagehw/touch/TouchscreenGesture.cpp` defines a single-tap gesture node at `/sys/class/touchscreen/NVT-ts/single_click`.
- `BoardConfig.mk` sets the tap-to-wake node to `/sys/class/touchscreen/NVT-ts/double_click`.
- `lineagehw/touch/service.cpp` registers a LineageOS touchscreen-gesture HIDL service. This is a gesture-control service, not the low-level touchscreen bus driver.
- `lineagehw/touch/Android.bp` builds that service from the gesture implementation and service entry point.

These files confirm that this Android configuration expects an NVT-labelled sysfs interface for gesture control. The string `NVT-ts` is suggestive, but these user-space paths alone do **not** prove the physical controller vendor or exact IC model. In particular, they do not resolve the conflict with the archived kernel DTS that declares `compatible = "tchip,ilitek"` on SPI.

Current interpretation:
- **Panel configuration lead:** Tianma/ILI7807S-labelled DSI configuration, 1080 × 2460, dynamic 60/120 Hz in the archived kernel source; exact module SKU and applicability to each regional revision remain unverified.
- **Touch interface evidence:** archived kernel DTS declares an ILITEK-family SPI binding; Android gesture configuration refers to an NVT-labelled sysfs node.
- **Exact touch IC:** unresolved. Do not rename the hardware profile to Novatek or ILITEK as a definitive physical component until the source trees are reconciled against a device-specific primary source.
- **DarwinG60:** no hardware driver was added; the existing interface remains synthetic and host-side.

Additional source files:
- [TouchscreenGesture.cpp](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/lineagehw/touch/TouchscreenGesture.cpp)
- [service.cpp](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/lineagehw/touch/service.cpp)
- [Android.bp](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/lineagehw/touch/Android.bp)
- [BoardConfig.mk](https://github.com/bhawesh2002/android_device_motorola_hanoip/blob/default/BoardConfig.mk)
