# XNU ARM64 build attempt

Date: 2026-11-07

## Result

**Result: Not verified.**

The upstream XNU source was checked out from the pinned submodule commit:

- Tag: `xnu-11215.1.10`
- Annotated tag object: `d95cbeef34d1a9cca097b33d385db3b2aae1a755`
- Commit: `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`

## Host inventory

- macOS 15.8.2, ARM64
- Xcode 16.4 (build 16F6)
- Apple Clang 17.0.0
- GNU Make 3.81
- macOS SDK 15.5
- iOS SDK 18.5 also present

This is a promising Apple toolchain candidate, not proof of compatibility with the pinned XNU revision.

## Attempted command

```sh
make SDKROOT="$(xcrun --sdk macosx --show-sdk-path)" ARCH_CONFIGS=ARM64 KERNEL_CONFIGS=DEVELOPMENT -j2
```

## Failure

The build stopped in `makedefs/MakeInc.kernel` before compilation:

```text
Could not determine xnu version from SDK or KDK!
Set RC_DARWIN_KERNEL_VERSION environment variable.
```

No kernel artifact was generated. The public macOS SDK did not provide the kernel-version metadata expected by this XNU build system. A matching KDK or a verified, source-appropriate version override and any additional required headers must be established before retrying.

## Evidence

- [GitHub Actions run](https://github.com/filipdanielisback-commits/DarwinG60/actions/runs/42374260258)
- [Build-attempt artifact](https://github.com/filipdanielisback-commits/DarwinG60/actions/runs/42374260258/artifacts/13575470511)

This was a host-side compile attempt only. Nothing was installed, booted, or tested on a phone. It does not establish Moto G60 compatibility.


## Second attempt with an explicit kernel-version override

A second run set `RC_DARWIN_KERNEL_VERSION=24.0.0` as an experimental build metadata override. This value was used only to test whether the build could pass the missing-version lookup; it does not assert an exact iOS point-release mapping.

The build passed the version lookup and compiled several bootstrap utilities, then stopped because the public SDK did not contain:

```text
usr/local/libexec/availability.pl
```

No kernel artifact was produced. The public SDK is not yet a confirmed compatible environment for this XNU source. A matching KDK or complete SDK with the required Apple build utility and headers remains necessary.

Evidence: [second GitHub Actions run](https://github.com/filipdanielisback-commits/DarwinG60/actions/runs/42374501882), artifact [xnu-arm64-override-build-attempt](https://github.com/filipdanielisback-commits/DarwinG60/actions/runs/42374501882/artifacts/13575640445).


## Follow-up: missing external-build prerequisites

Apple's external-build guidance identifies a matching host KDK for Apple-Silicon build hosts, plus AvailabilityVersions, libdispatch's kernel firehose library and installed XNU headers. DTrace CTF tools are optional. The missing availability.pl observed above is supplied by the AvailabilityVersions dependency; it is not evidence that a random SDK version override fixes the environment.

See [BUILD-ENVIRONMENT.md](BUILD-ENVIRONMENT.md) for the source references, KDK matching criteria and remaining verification checklist. The new read-only CI probe inventories installed KDKs and relevant SDK paths. No KDK has yet been confirmed on the runner, and no dependency versions have yet been pinned for this XNU tag.
