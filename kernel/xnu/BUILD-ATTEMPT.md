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


## Exact CI host and KDK result (2026-11-07)

A subsequent probe established the exact runner identity:

- Host: macOS 15.8.2, build 24H232
- Virtual model: VirtualMac2,1
- Platform token: VMA2MACOSAP
- Xcode: 16.4 (16F6)
- SDK: macOS 15.5 (24F74)
- Apple Clang: 17.0.0
- KDK inventory: none installed

The expected filename pattern for a matching KDK is `KDK_15.8.2_24H232.kdk`, but this is not proof that Apple currently offers that package. The actual KDK must be obtained through an authorized Apple developer download and its System.kext metadata verified. The CI job deliberately does not use third-party KDK binaries or stored personal credentials.

The runner's virtual platform token `VMA2MACOSAP` is not present in the pinned XNU public machine-configuration tree, so it is not accepted as a target configuration. The source has explicit Mac ARM64 configurations including T8112 and T8132; selecting one for a cross-build must be documented as a macOS reference target, not as Moto G60 support.

AvailabilityVersions 143.3 builds and produces `availability.pl`. Full XNU header export has a separate DriverKit source-rule failure: the DriverKit makefile lists `IOTypes.h` as a local source, while the public source tree places it in `iokit/IOKit/IOTypes.h`. The workflow records this limitation. No XNU kernel artifact has been generated, and kernel build verification remains false.


## Follow-up: exact ATM header dependency and documented ARM64 configuration (2026-11-07)

The pinned XNU source tree locates `atm_internal.h` at `osfmk/atm/atm_internal.h`. Its direct XNU dependencies are `osfmk/atm/atm_types.h` and `libkern/os/refcnt.h`; the latter includes `libkern/os/refcnt_internal.h`. The dependency preparation script now stages those exact source-pinned headers into the corresponding Kernel.framework private-header directories before building `libfirehose_kernel`. This only addresses the observed missing-header chain; success of the dependency build is pending CI.

The build workflow also stopped using `TARGET_CONFIGS` and the runner's `hw.target` token. The pinned XNU README documents `ARCH_CONFIGS` and `KERNEL_CONFIGS`; the selected reference configuration is `ARCH_CONFIGS=ARM64 KERNEL_CONFIGS=DEVELOPMENT`. This is not a Moto G60 configuration. A matching host KDK is still required, and the previously observed macOS 15.8.2 / build 24H232 runner had none installed. No XNU kernel artifact has yet been produced.
