# XNU build environment and dependency requirements

## Scope and pinned source

This investigation concerns upstream XNU tag xnu-11215.1.10 (tag object d95cbeef34d1a9cca097b33d385db3b2aae1a755), pinned to source commit 8d741a5de7ff4191bf97d57b9f54c2f6d4a15585. The tag is an iOS 18-era research baseline; an exact iOS point-release mapping has not been established.

This document distinguishes:
- **Host toolchain candidate:** Xcode, Clang, make and an SDK are present.
- **Compatible build environment:** required KDK and dependency versions are matched to the host and this XNU source, and the build prerequisites pass.
- **Verified kernel build:** a successful build exits cleanly and produces an expected ARM64 kernel artifact whose metadata and hash are recorded.

A host candidate is not a successful or compatible XNU build.

## Evidence from Apple's build documentation

The README at the exact pinned XNU tag documents the generic make interface and says the kernel version is read from System.kext metadata in the SDK or KDK. It does not, by itself, specify a complete external Apple-Silicon dependency matrix.

The official Apple OSS `distribution-macOS` manifest at commit `fafa0d30e9943c16e82740488dc0750c24355562` identifies this XNU tag as the macOS 15.0 source release and pins the matching public source dependencies in [DEPENDENCIES.lock](DEPENDENCIES.lock): AvailabilityVersions 143.3 and libdispatch 1502.0.1. Their exact annotated tag objects and peeled commits are recorded there.

The following external-build procedure is documented in the `apple-open-source/macos` XNU README mirror; treat it as build guidance to validate against the pinned tag, not as a guarantee that all details match every XNU release. It identifies the following for Apple-Silicon hosts:

- A Kernel Debug Kit (KDK) matching the exact macOS version/build of the build host.
- AvailabilityVersions `AvailabilityVersions-143.3`, which supplies `availability.pl` for the macOS 15.0 source release.
- XNU headers generated from the pinned XNU source and installed into the SDK.
- libdispatch `libdispatch-1502.0.1`, providing the `libfirehose_kernel` build product.
- DTrace CTF tools are optional.

References:
- Exact pinned XNU README: https://github.com/apple-oss-distributions/xnu/blob/xnu-11215.1.10/README.md
- Apple Open Source XNU external build guidance: https://github.com/apple-open-source/macos/blob/master/xnu/README.md
- Apple KDK overview: https://developer.apple.com/documentation/apple-silicon/debugging-a-custom-kernel-extension
- Apple Xcode/SDK version matrix: https://developer.apple.com/xcode/system-requirements/

The external-build guide says the KDK is selected for the build host's macOS version. That is a different compatibility question from the XNU source tag's Darwin kernel version. Do not select a KDK merely because its version number resembles the XNU tag or an iOS release.

## Current CI host candidate

The previous GitHub-hosted runner inventory reported:

- macOS 15.8.2, ARM64
- Xcode 16.4 (build 16F6)
- Apple Clang 17.0.0
- GNU Make 3.81
- macOS SDK 15.5
- iOS SDK 18.5

The host build number must be captured from sw_vers -buildVersion on each run. The Xcode 16.4 SDK version does not establish that the SDK is aligned with the runner's current macOS build, and the previous job did not find a KDK.

## Observed build blockers

1. Without a kernel-version metadata override, XNU stopped before compilation because it could not read System.kext/Info.plist CFBundleVersion from the public SDK/KDK.
2. With the experimental RC_DARWIN_KERNEL_VERSION=24.0.0 override, the build passed that check and built some bootstrap utilities, then stopped because usr/local/libexec/availability.pl was absent.
3. Neither attempt produced a kernel artifact.

The override was diagnostic only. 24.0.0 is not asserted to be the correct source-matched Darwin kernel version.

## What remains to identify

- The exact macOS host build number for the runner used by the next attempt.
- A KDK package whose version/build matches that host, including its System.kext metadata. The macOS 15.0 XNU release manifest does not identify this host KDK; it is a separate host-side dependency.
- Build/install validation of AvailabilityVersions `143.3` and the exact `availability.pl` install location.
- Build/install validation of libdispatch `1502.0.1` and its `libfirehose_kernel` product.
- Whether the pinned XNU source can export and install the required headers against the chosen SDK.
- Whether any additional Apple-Silicon TARGET_CONFIGS platform selection is required by this XNU revision and runner hardware.

The macOS probe in tools/xnu_macos_environment.py now inventories the installed KDKs and selected SDK for several known missing dependency paths. It is read-only and does not install packages, change the SDK, or compile XNU.

## Access and provenance

Apple's KDK downloads are distributed through Apple's developer downloads. Do not embed account credentials in CI, commit KDK packages, or substitute an unverified third-party binary. If a KDK requires an authenticated download, use an authorized local environment and keep credentials outside the repository and logs.

Prefer source dependencies from Apple's official open-source release repositories. Record each dependency's repository, release/tag, commit, license, archive checksum and installation path before using it. Do not copy dependencies into the SDK until their versions and licensing are reviewed.

## Verification gate

A future build is only eligible for kernel_build_verified when all of the following are recorded and independently checked:

- Exact XNU tag, tag object and submodule commit.
- Host macOS version and build number.
- Xcode, Clang and SDK versions.
- KDK path, package version/build, and System.kext CFBundleVersion.
- Exact dependency source tags/commits and licenses.
- Exact build command and successful exit code.
- A non-empty ARM64 kernel artifact produced by that build.
- SHA-256 hashes for the artifact and complete build log.

A successful CI workflow or a compiler being present is not sufficient. No output from these host builds is to be installed or booted on a phone.


## Source-release dependency pins

The official Apple OSS release manifest at commit `fafa0d30e9943c16e82740488dc0750c24355562` declares the macOS 15.0 source set:

| Component | Pinned tag | Peeled source commit |
|---|---|---|
| XNU | `xnu-11215.1.10` | `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585` |
| AvailabilityVersions | `AvailabilityVersions-143.3` | `b687146a07d05ab281d25a94114addba4ce6cc76` |
| libdispatch | `libdispatch-1502.0.1` | `bd82a60ee6a73b4eca50af028b48643d51aaf1ea` |
| dtrace (optional) | `dtrace-409` | not needed for the initial kernel compile |

This is a better source-dependency baseline than taking the newest versions of these projects. The tag and commit pins are independently recorded in `DEPENDENCIES.lock`.

## KDK identification rule

The KDK is **not** selected by matching its name to `xnu-11215.1.10`. The external-build guidance requires the KDK matching the exact macOS version/build of the Apple-Silicon build host. Therefore the workflow must first record `sw_vers -productVersion` and `sw_vers -buildVersion`, then inspect `/Library/Developer/KDKs` and verify the selected KDK's `System.kext/Info.plist:CFBundleVersion`. The GitHub-hosted runner currently has no confirmed KDK, so an exact package name cannot honestly be stated yet.

Apple distributes KDKs through its developer downloads. The project will not fetch an authenticated package using stored personal credentials or use an unverified third-party binary. A KDK must be provided through an authorized, controlled build environment before the ARM64 build can be marked verified.


## Observed GitHub-hosted macOS runner (2026-11-07)

The CI probe identified the actual build host:

- macOS 15.8.2, build `24H232`
- Virtual model `VirtualMac2,1`
- `hw.target=VMA2MACOSAP`
- Xcode 16.4, build 16F6
- Apple Clang 17.0.0
- GNU Make 3.81
- macOS SDK 15.5 (SDK build 24F74)
- No KDK installed under `/Library/Developer/KDKs`

The KDK package filename expected by Apple's usual naming pattern would be `KDK_15.8.2_24H232.kdk`. This is a **filename candidate only**: its availability and contents have not been verified against Apple's developer downloads. A matching KDK must be checked for `System.kext/Info.plist:CFBundleVersion` before use.

The runner reports the virtual platform `VMA2MACOSAP`. That token does not appear in the pinned public XNU source's machine configuration files; the source does contain explicit Mac configurations such as `MASTER.arm64.t8112.MacOSX` and `MASTER.arm64.t8132.MacOSX`. Do not pass the virtual host token as a kernel target without proving that the source supports it. A host-side compile target must be selected explicitly from the pinned source's supported configurations.

AvailabilityVersions 143.3 now builds successfully and stages `availability.pl`. The full XNU `installhdrs` path currently fails in the DriverKit export because its makefile expects `iokit/DriverKit/IOTypes.h` as a local source, while the public tree contains that file under `iokit/IOKit/IOTypes.h`. The workflow records this separately rather than claiming a complete XNU header installation.

The KDK is still the decisive blocker for a complete, verified ARM64 build on this runner. No kernel artifact has been produced.


## ATM header dependency traced in the pinned source (2026-11-07)

The previous `libfirehose_kernel` attempt stopped because `tracepoint_private.h` includes `<atm/atm_internal.h>` when `KERNEL` is defined. The exact pinned XNU tree places that header at `osfmk/atm/atm_internal.h` (not `libkern/atm`). Its direct XNU header dependencies are:

- `osfmk/atm/atm_types.h`
- `libkern/os/refcnt.h`
- `libkern/os/refcnt_internal.h` (included by `refcnt.h`)

The dependency-preparation script now stages these exact files from the checked-out XNU submodule into the matching `Kernel.framework/PrivateHeaders/atm` and `Kernel.framework/PrivateHeaders/os` directories. It checks each file is non-empty and records the staging status. This is a narrow, source-pinned workaround for the currently failing public-tree `installhdrs` path; it is not a claim that the complete XNU header export has succeeded.

Exact source references at commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`:
- https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/atm/atm_internal.h
- https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/osfmk/atm/atm_types.h
- https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/libkern/os/refcnt.h
- https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/libkern/os/refcnt_internal.h

## ARM64 reference build configuration

The pinned XNU README documents `ARCH_CONFIGS` and `KERNEL_CONFIGS`, with the generic syntax `make SDKROOT=<sdkroot> ARCH_CONFIGS=<arch> KERNEL_CONFIGS=<variant>`. The workflow now uses `ARCH_CONFIGS=ARM64 KERNEL_CONFIGS=DEVELOPMENT`. It no longer passes the GitHub VM's `hw.target` token through the unsupported `TARGET_CONFIGS` variable. This is a generic ARM64 DEVELOPMENT reference build, not a Moto G60 target and not proof of support for any particular ARM64 SoC.

The exact host-matching KDK remains mandatory for the Apple-Silicon external build path. The previously observed runner had macOS 15.8.2 build `24H232` and no matching KDK installed. The candidate package name is not evidence of availability; CI must still detect and verify an actual matching KDK before attempting the kernel build.


## Firehose chunk header dependency traced (2026-11-07)

After the ATM/refcount headers were staged, the pinned libdispatch `libfirehose_kernel` build advanced to `src/firehose/firehose_buffer.c` and failed on `<chunk_private.h>`. The exact pinned XNU source contains `libkern/firehose/chunk_private.h`. Its direct includes are `<sys/param.h>`, `firehose_types_private.h`, and `tracepoint_private.h`; the latter two are already staged beside it under the SDK's `usr/local/include/firehose` directory. The preparation script now stages this exact header from the pinned XNU submodule and verifies it is non-empty. This resolves the observed missing-file path only; the next CI run must determine whether further compile issues remain.

Source: https://github.com/apple-oss-distributions/xnu/blob/8d741a5de7ff4191bf97d57b9f54c2f6d4a15585/libkern/firehose/chunk_private.h


## Successful libfirehose dependency build; KDK remains blocking (2026-11-07)

CI run [42391235120](https://github.com/filipdanielisback-commits/DarwinG60/actions/runs/42391235120) completed the dependency-preparation step successfully. AvailabilityVersions produced and staged `availability.pl`. The pinned libdispatch `libfirehose_kernel` target compiled and linked a universal `libfirehose_kernel.a` containing both `arm64` and `arm64e` slices, and the script staged it into the SDK. The exact ATM/refcount and firehose chunk headers were sufficient to get past the missing-header errors observed in earlier attempts.

The subsequent XNU kernel build step did **not** run. The runner inventory still found no KDK matching macOS 15.8.2 build `24H232`, so the build gate correctly stopped before invoking `make`. The workflow now selects the pinned XNU README's documented generic reference configuration `ARCH_CONFIGS=ARM64 KERNEL_CONFIGS=DEVELOPMENT`; this configuration has not yet been exercised because the KDK gate blocks it. No XNU kernel binary exists yet.

The KDK is an Apple-distributed, separate download. Apple's documentation directs developers to download the KDK for the macOS version being debugged and links to the authenticated More Downloads page: https://developer.apple.com/documentation/apple-silicon/debugging-a-custom-kernel-extension and https://developer.apple.com/download/more/. The CI workflow will not use an unverified third-party mirror or store developer credentials. A matching kit must be supplied in an authorized macOS build environment and checked for its `System.kext` metadata before the kernel build can proceed.

Evidence artifact from this run: [xnu-arm64-build-evidence](https://github.com/filipdanielisback-commits/DarwinG60/actions/runs/42391235120/artifacts/13581053391).
