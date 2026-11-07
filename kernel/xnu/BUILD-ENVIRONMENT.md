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
