# DarwinG60 XNU research track

**Status: upstream XNU is pinned as a Git submodule; no DarwinG60 XNU build or device port is verified.**

This directory tracks whether and how the public XNU kernel source could inform a future DarwinG60 kernel experiment.

## Important scope

XNU is the open-source kernel at the core of several Apple operating systems. It is not the complete iOS operating system. In particular, an iOS 18 installation also depends on proprietary Apple components, platform-specific drivers, firmware, services, frameworks, signing and security infrastructure that are not supplied by the public XNU source release.

DarwinG60 is an independent research project. This directory does not claim to reproduce iOS 18, provide Apple's private components, or make an iOS 18 image for the Moto G60.

## Current facts

- Target device under study: Motorola Moto G60 (codename `hanoip`).
- Publicly reported platform: Qualcomm Snapdragon 732G / SM7150 family.
- Existing DarwinG60 work is host-side simulation and architecture research.
- No verified XNU port exists in this repository.
- No verified XNU support for this exact handset/platform has been established.
- Existing Android/Linux device-tree observations are research evidence, not XNU drivers.

## Research gates

1. **Source and licensing review** — identify the relevant public XNU release, its license obligations, source provenance and supported build environments before considering any import.
2. **Architecture assessment** — document CPU architecture, exception levels, MMU assumptions, interrupt model, timers, SMP expectations and platform interfaces at a conceptual level.
3. **Kernel/platform boundary** — define the minimum platform abstraction XNU would require and compare it with evidence available for hanoip. Keep unknowns explicitly unknown.
4. **Driver feasibility** — assess each required subsystem independently. Do not treat Linux drivers, Android HALs, sysfs nodes or device-tree labels as directly reusable XNU drivers.
5. **Host-only validation** — use documentation checks and non-destructive host-side tests first. No physical-device installation or firmware/boot-chain modification is part of this research scaffold.
6. **Go/no-go decision** — only propose implementation after source compatibility, platform feasibility, licensing and a safe test strategy are independently reviewed.

## What “iOS 18 support” would mean

There is no complete, public iOS 18 source tree that can simply be compiled for this phone. Public XNU code alone would not provide the iOS 18 user interface, Apple frameworks, proprietary services, device drivers or a complete iOS 18 system. DarwinG60 must not label an XNU experiment as “iOS 18” or “iOS 18 port”.

A future independent DarwinG60 userspace and interface may borrow general operating-system design ideas, but it must use original implementation and properly licensed components.

## Current implementation status

| Area | Status |
|---|---|
| XNU upstream source pinned/importable | Yes — Git submodule at exact upstream commit |
| XNU source materialized in CI | Yes — recursive submodule checkout |
| XNU source materialized in a local checkout | Run `git submodule update --init --recursive` |
| XNU configured for hanoip | No |
| XNU build verified | No |
| XNU platform layer | Not implemented |
| XNU drivers for hanoip | Not verified |
| iOS 18 compatibility | Not available |
| Research documentation | Started |

## Build environment investigation

See [BUILD-ENVIRONMENT.md](BUILD-ENVIRONMENT.md) for Apple's external-build prerequisites, KDK matching criteria, the two observed SDK blockers, and the evidence required before declaring a kernel build verified. The macOS CI probe inventories KDK and SDK dependency paths without modifying the host.

See [BUILD-ATTEMPT.md](BUILD-ATTEMPT.md) for actual build attempt results. The current host is only a toolchain candidate; no compatible KDK/dependency set or successful kernel build has been verified.

## Upstream references

- XNU source: https://github.com/apple-oss-distributions/xnu
- Apple Open Source: https://opensource.apple.com/
- Apple OSS distributions: https://github.com/apple-oss-distributions

Consult the license and notices for the exact upstream release before redistributing or modifying any source. This repository's top-level license applies only to original DarwinG60 contributions, not Apple's or other third-party material.

## Source inventory

See [UPSTREAM-SOURCES.md](UPSTREAM-SOURCES.md) for the official Apple source repositories reviewed so far, including XNU, dyld, WebKit and the iOS distribution manifest. The inventory distinguishes selected open-source components from the complete proprietary iOS 18 operating system.


## Pinned research baseline

The project has selected the official Apple XNU tag `xnu-11215.1.10` as an **iOS 18-era research baseline**. The exact tag object is recorded in [UPSTREAM.lock](UPSTREAM.lock). The tag is pinned for repeatable source review; this does not establish an exact iOS 18 point-release mapping or hanoip compatibility.

The upstream Apple Public Source License 2.0 text is preserved in [APPLE_LICENSE](APPLE_LICENSE). Review and retain the applicable upstream notices for any source files before redistribution.

**Source import:** `upstream/` is a Git submodule pointing to the exact commit behind the selected Apple tag. Clone with `git clone --recurse-submodules` or run `git submodule update --init --recursive` after cloning to materialize the complete source tree. Git stores the upstream source as a pinned external repository reference rather than duplicating Apple's full history in DarwinG60.

**Build status:** the first ARM64 `DEVELOPMENT` build was attempted on a GitHub-hosted macOS 15.8.2 ARM64 runner with Xcode 16.4, Apple Clang 17 and macOS SDK 15.5. The attempt stopped in `makedefs/MakeInc.kernel` because the public SDK/KDK did not provide `System.kext/Info.plist` `CFBundleVersion`; XNU asked for `RC_DARWIN_KERNEL_VERSION`. No kernel artifact was produced. The host is a **toolchain candidate**, not yet a confirmed compatible XNU build environment. See [BUILD-ATTEMPT.md](BUILD-ATTEMPT.md) and the [CI run](https://github.com/filipdanielisback-commits/DarwinG60/actions/runs/42374260258).
