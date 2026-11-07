# Apple upstream source inventory

**Research status: official source repositories identified; no upstream source imported or built yet.**

This inventory records public Apple source locations relevant to DarwinG60's XNU research. The existence of public source code is confirmed; compatibility with the Moto G60 is a separate engineering question.

## Primary upstream sources

| Component | Official source | Potential relevance | Important limitation |
|---|---|---|---|
| XNU | https://github.com/apple-oss-distributions/xnu | Mach kernel, BSD subsystems, IOKit, platform-dependent kernel code | Public source does not include every platform driver, firmware component, SDK or internal build dependency |
| dyld | https://github.com/apple-oss-distributions/dyld | Dynamic linker and loader research | Not a complete userspace runtime; version and ABI compatibility matter |
| WebKit | https://github.com/apple-oss-distributions/WebKit | Browser/web rendering engine research | Does not provide iOS UI frameworks or the complete browser app |
| Apple iOS source distribution manifest | https://github.com/apple-oss-distributions/distribution-iOS | Release-level inventory of selected open-source components | It is a manifest, not a complete iOS source tree |

Apple's official source portal: https://opensource.apple.com/releases/

## What the official XNU repository confirms

The upstream XNU README describes XNU as part of Darwin used in macOS and iOS. It identifies the hybrid Mach/FreeBSD/IOKit structure and documents ARM64 among its supported architecture families.

The same README's example build environment refers to Apple's `macosx.internal` SDK. This is a warning that a public source checkout is not automatically a reproducible, turnkey build using only ordinary public tools and headers. The README's example configurations are not proof that a generic ARM64 device such as hanoip is supported.

## iOS 18 source availability: careful distinction

The current `distribution-iOS` repository's `release.json` identifies its current manifest as iOS 26.0 and lists selected projects such as WebKit and libiconv. It does **not** establish that a complete iOS 18 source tree is published.

Apple does publish selected open-source components used by its operating systems. That is different from publishing all of iOS 18, including its proprietary frameworks, private services, firmware, device-specific drivers, signing infrastructure and complete platform build environment.

A community project may combine a public XNU revision with separately obtained operating-system components and substantial device-specific engineering. Such a project is not evidence that Apple released the entire iOS source tree, and it does not establish compatibility with another phone.

## DarwinG60 source-handling policy

1. Prefer official Apple repositories and release manifests for upstream source.
2. Record exact tags/commits and license notices before importing any source.
3. Do not copy an entire upstream tree into DarwinG60 until its size, provenance, license obligations, build dependencies and maintenance plan have been reviewed.
4. Keep original DarwinG60 code clearly separated from third-party source.
5. Never describe an upstream source checkout, a successful host compile, or a simulated subsystem as a working Moto G60 port.
6. Treat XNU-to-hanoip compatibility as unproven until there is a documented platform implementation and independent evidence for each required subsystem.
7. Do not describe public XNU as a complete iOS 18 implementation.

## Current source-review findings

- [x] Official Apple XNU repository located.
- [x] Official Apple OSS distribution organization located.
- [x] Official iOS distribution manifest inspected.
- [x] Official dyld repository located.
- [x] Official WebKit repository located.
- [ ] Select and pin an exact XNU source revision for deeper review.
- [ ] Review the exact revision's license and build prerequisites.
- [ ] Compare the revision's ARM64 platform assumptions against documented hanoip evidence.
- [ ] Make a documented feasibility decision before any platform implementation.

## References

- XNU README: https://github.com/apple-oss-distributions/xnu/blob/main/README.md
- iOS distribution manifest: https://github.com/apple-oss-distributions/distribution-iOS/blob/main/release.json
- Apple OSS organization: https://github.com/apple-oss-distributions
- Apple OSS releases: https://opensource.apple.com/releases/
