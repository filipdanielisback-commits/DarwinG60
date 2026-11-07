# XNU feasibility checklist for hanoip

This is a planning and evidence checklist, not a hardware bring-up guide. It intentionally contains no device modification, boot-chain, flashing, or firmware replacement steps.

## Platform feasibility matrix

| Requirement | Why XNU needs it | Current hanoip evidence | Assessment |
|---|---|---|---|
| CPU architecture and supported execution state | Kernel must match the processor architecture and execution environment | Snapdragon 732G / SM7150 family is reported; exact XNU release/platform compatibility not established | Open |
| Early platform initialization | Kernel needs a supported way to discover and initialize the platform | No XNU platform implementation in this repository | Blocked |
| Memory map and MMU | Kernel needs correct physical memory layout and translation setup | No verified XNU memory map or MMU integration | Blocked |
| Interrupt controller and timers | Required for scheduling, clocks and device events | No XNU interrupt/timer platform layer verified | Blocked |
| SMP and CPU topology | Required for safe multi-core operation | No XNU SMP support for hanoip verified | Blocked |
| Console and display | Needed for useful diagnostics and graphical output | Existing DarwinG60 display code is a host-side synthetic prototype only | Blocked |
| Storage | Needed for persistent system state | Exact controller/protocol integration for XNU is unknown | Blocked |
| Wi-Fi and Bluetooth | Needed for network connectivity | Handset radio/module and XNU driver support not verified | Blocked |
| Audio and sensors | Needed for corresponding device features | Exact components and XNU drivers not verified | Blocked |
| Power management | Needed for reliable mobile operation | No XNU power-management integration verified | Blocked |
| Security and signing model | Kernel and system components require a coherent trust model | No DarwinG60 mobile trust chain or iOS 18 compatibility exists | Blocked |

## Decision rule

Do not call this a port until all of the following are demonstrated with reproducible evidence:

- A specific, legally reviewed upstream XNU revision is selected.
- Its architecture and platform assumptions are understood.
- A supported and maintainable platform integration path is identified.
- Required platform services and drivers have independently verified implementations.
- Host-side tests and a reviewed validation plan exist.
- Claims distinguish public XNU functionality from proprietary iOS components.

A successful compile by itself would not prove that the kernel can run on the Moto G60. A running kernel by itself would not prove iOS 18 compatibility.

## Recommended next research deliverables

1. Pin and review a specific public XNU source revision and its license notices.
2. Produce an architecture compatibility report for the selected XNU revision.
3. Map each required XNU platform service to documented hanoip evidence or an explicit unknown.
4. Make a written go/no-go decision before attempting implementation.

## Current decision

**NO-GO for claiming or attempting a complete iOS 18 port.**

**GO for source review, architecture research and a platform feasibility study.**

This decision can change only when new, reliable evidence resolves the blockers above.


## Selected upstream baseline

The official Apple XNU tag `xnu-11215.1.10` is now pinned in [UPSTREAM.lock](UPSTREAM.lock) as an iOS 18-era research baseline. Its tag object is recorded there. The precise iOS point-release mapping remains to be checked against primary Apple release metadata.

The upstream license text is preserved in [APPLE_LICENSE](APPLE_LICENSE). This is not a full source import.

## Build result

**Not built.** No compile was run, so there is no build result to report. The current repository integration environment can write GitHub files but cannot provide the matching Apple SDK/KDK environment needed to verify the upstream build. The public XNU README documents build variables and uses an internal SDK example; it does not establish a generic Linux/Android cross-build for hanoip.

Next safe engineering step: review the pinned revision's documented prerequisites and source configuration, then design a reproducible host-side source validation job. Do not claim a kernel build until a real compiler run produces a recorded result.
