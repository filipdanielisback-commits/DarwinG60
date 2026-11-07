# XNU source and build-readiness audit

## Purpose

`tools/xnu_readiness.py` reports what is and is not established for the DarwinG60 XNU research track. It is a local, non-destructive audit. It does not fetch upstream source, configure a kernel, compile binaries, install software, or interact with a phone.

Run it from the repository root:

```sh
python tools/xnu_readiness.py
```

The command prints a concise report and a JSON representation suitable for later automation.

## Four independent milestones

The audit deliberately reports four separate facts:

1. **Source reference pinned** — `kernel/xnu/UPSTREAM.lock` matches the reviewed repository, tag, tag-object identifier and license reference, and the Apple license file exists.
2. **Source tree imported** — the expected upstream tree is present under `kernel/xnu/upstream/`. The checker looks for `README.md`, `osfmk/`, `bsd/`, `iokit/` and `APPLE_LICENSE`. The research scaffold's own README does not count as imported XNU source.
3. **Build environment candidate** — the host is macOS, `make`, `clang`, `xcrun` and `xcodebuild` are available, and `SDKROOT` points to an existing directory. This is only a prerequisite signal; it does not prove that a matching public SDK/KDK or all required dependencies are present.
4. **Kernel build verified** — only `kernel/xnu/build-verification.json` with the exact pinned tag, tag object and source commit, plus existing build artifact and log files whose SHA-256 values match the record, can satisfy this milestone. The record also requires host, SDK, command and reviewer fields. Build artifacts and logs must remain inside `kernel/xnu/`, outside the upstream submodule. The audit never infers success from a compiler being present or from an arbitrary binary existing.

## Current baseline and limitations

The research baseline remains `xnu-11215.1.10`, tag object `d95cbeef34d1a9cca097b33d385db3b2aae1a755`. It is described as an iOS 18-era source reference; an exact iOS 18 point-release mapping has not been established.

The official XNU source is now represented in DarwinG60 as a Git submodule at the exact commit behind the pinned tag. GitHub Actions checks it out recursively, so the CI workspace materializes the upstream tree. A normal local checkout must initialize submodules with `git submodule update --init --recursive`. The audit does not check the network and therefore cannot decide whether the pin is the newest upstream revision or has been superseded. Consult Apple's official [XNU repository](https://github.com/apple-oss-distributions/xnu) and its [tags](https://github.com/apple-oss-distributions/xnu/tags) for upstream comparisons.

Apple's upstream README describes an XNU build using an SDK root and architecture/configuration variables; it also gives `macosx.internal` as an example SDK root. Availability of a local public SDK is not equivalent to access to Apple's internal SDK/KDK or proof that this particular historical source revision builds with a given toolchain. See the [official XNU build documentation](https://github.com/apple-oss-distributions/xnu/blob/main/README.md).

## Safety and scope

This audit is limited to source metadata and host environment inspection. It does not provide device installation, boot-chain changes, firmware replacement, partition modification, or physical-device testing instructions. No Moto G60 compatibility or hardware driver support is implied.


## Submodule checkout and build evidence

The root `.gitmodules` file maps `kernel/xnu/upstream` to Apple's official repository. The superproject records the exact upstream commit as a Git submodule gitlink. CI uses recursive submodule checkout. To materialize it in a local working copy:

```sh
git submodule update --init --recursive
```

A future successful build must retain its build log and output artifact under `kernel/xnu/`, then add `kernel/xnu/build-verification.json` with the pinned tag, tag-object ID, source commit, build host, SDK, exact build command, relative artifact/log paths, their SHA-256 hashes, and a reviewer. The audit verifies those files and hashes; it does not create the record or perform the build.


## First macOS ARM64 build trial (2026-11-07)

GitHub Actions checked out the exact upstream submodule commit `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585` and probed this host:

- macOS 15.8.2, ARM64
- Xcode 16.4 (build 16F6)
- Apple Clang 17.0.0
- GNU Make 3.81
- macOS SDK 15.5
- iOS SDK 18.5 was installed, but this is not a substitute for a matching XNU KDK

The trial command was:

```sh
make SDKROOT="$(xcrun --sdk macosx --show-sdk-path)" ARCH_CONFIGS=ARM64 KERNEL_CONFIGS=DEVELOPMENT -j2
```

It failed before compilation in `makedefs/MakeInc.kernel` because XNU could not obtain the kernel version from the public SDK/KDK and requested `RC_DARWIN_KERNEL_VERSION`. No kernel binary was generated. This establishes a macOS toolchain candidate, not a compatible build environment or successful kernel build.

The log and status file are retained in the GitHub Actions artifact [xnu-arm64-build-attempt](https://github.com/filipdanielisback-commits/DarwinG60/actions/runs/42374260258/artifacts/13575470511). The next build investigation must establish the correct kernel-version metadata and any matching KDK/header requirements for this exact XNU source. Do not infer an iOS point-release mapping from the tag name alone.


### Second build attempt with an explicit version override

A second attempt set `RC_DARWIN_KERNEL_VERSION=24.0.0` (an experimental build metadata override, not a claim that this tag maps to a particular iOS point release). It advanced beyond the kernel-version lookup and compiled several setup tools, but then stopped because the public macOS SDK did not contain:

```text
usr/local/libexec/availability.pl
```

No kernel binary was produced. The public SDK is therefore still not a verified compatible build environment for this XNU revision. A matching KDK or SDK containing the required Apple build utilities/headers must be identified before another build attempt.
