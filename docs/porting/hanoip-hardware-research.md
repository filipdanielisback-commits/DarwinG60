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

**Known:** Community device-tree summaries describe a 6.8/6.81-inch IPS LCD with high-refresh-rate support. The published community summaries conflict on the exact resolution (1080 × 2460 versus 1080 × 2400). The hanoip tree has a dedicated touch configuration area.

**Unknown:** Exact LCD panel part number and revision, display bridge/controller details, DSI mode/timings, touch-controller manufacturer/model, bus address, interrupt/reset wiring, firmware requirements, and panel variation across regional batches.

**DarwinG60 implication:** Keep panel and touch identification as unresolved. A generic display abstraction and host-side touch-event model can be designed independently, but no physical panel or touch driver is implemented.

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
