#!/usr/bin/env bash
# Prepare the public source dependencies documented for the macOS 15.0 XNU release.
# Runs only on an ephemeral macOS CI runner. Does not install or alter a phone.
set -euo pipefail

ROOT="$GITHUB_WORKSPACE"
WORK="$RUNNER_TEMP/darwing60-xnu-dependencies"
SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
EVIDENCE="$ROOT/kernel/xnu/build-evidence"
mkdir -p "$WORK" "$EVIDENCE"

clone_pin() {
  local repo="$1" tag="$2" commit="$3" dir="$4"
  if [[ ! -d "$dir/.git" ]]; then
    git clone --filter=blob:none --no-checkout "$repo" "$dir"
  fi
  git -C "$dir" fetch --depth 1 origin "refs/tags/$tag:refs/tags/$tag"
  git -C "$dir" checkout --detach "$tag"
  local actual
  actual="$(git -C "$dir" rev-parse HEAD)"
  if [[ "$actual" != "$commit" ]]; then
    echo "Pinned source mismatch for $tag: expected $commit got $actual" >&2
    return 1
  fi
  printf '%s %s\n' "$tag" "$actual"
}

{
  echo "host_version=$(sw_vers -productVersion)"
  echo "host_build=$(sw_vers -buildVersion)"
  echo "host_model=$(sysctl -n hw.model 2>/dev/null || true)"
  echo "host_target=$(sysctl -n hw.target 2>/dev/null || true)"
  echo "sdkroot=$SDKROOT"
  echo "sdk_version=$(xcodebuild -showsdks | tr '\n' ';')"
  echo "xcode_version=$(xcodebuild -version | tr '\n' ';')"
} > "$EVIDENCE/dependency-prepare-host.txt"

AV="$WORK/AvailabilityVersions"
DISPATCH="$WORK/libdispatch"
clone_pin "https://github.com/apple-oss-distributions/AvailabilityVersions.git" \
  "AvailabilityVersions-143.3" "b687146a07d05ab281d25a94114addba4ce6cc76" "$AV" \
  | tee "$EVIDENCE/availabilityversions-pin.txt"
clone_pin "https://github.com/apple-oss-distributions/libdispatch.git" \
  "libdispatch-1502.0.1" "bd82a60ee6a73b4eca50af028b48643d51aaf1ea" "$DISPATCH" \
  | tee "$EVIDENCE/libdispatch-pin.txt"

# Build AvailabilityVersions to a staging root, then install its required script
# into this disposable runner's selected macOS SDK.
AV_DST="$WORK/availability-dst"
make -C "$AV" install DSTROOT="$AV_DST" 2>&1 | tee "$EVIDENCE/availabilityversions-build.log"
AV_SCRIPT="$AV_DST/usr/local/libexec/availability.pl"
if [[ ! -f "$AV_SCRIPT" ]]; then
  AV_SCRIPT="$(find "$AV_DST" -type f -name availability.pl -print -quit)"
fi
if [[ -z "$AV_SCRIPT" || ! -f "$AV_SCRIPT" ]]; then
  echo "AvailabilityVersions build did not produce availability.pl" >&2
  exit 1
fi
sudo ditto "$AV_DST" "$SDKROOT"
test -f "$SDKROOT/usr/local/libexec/availability.pl"

# The full upstream installhdrs target currently fails in the public source
# tree's DriverKit header export (IOTypes.h is listed as a local source but only
# exists under iokit/IOKit). For libdispatch's immediate dependency, stage the
# exact XNU private atomic and CPU capability header families without modifying
# the upstream source.
KERNEL_PRIVATE="$SDKROOT/System/Library/Frameworks/Kernel.framework/PrivateHeaders"
KERNEL_PRIVATE_OS="$KERNEL_PRIVATE/os"
sudo mkdir -p "$KERNEL_PRIVATE_OS"
for header in atomic_private.h atomic_private_arch.h atomic_private_impl.h; do
  source="$ROOT/kernel/xnu/upstream/libkern/os/$header"
  test -f "$source"
  sudo cp "$source" "$KERNEL_PRIVATE_OS/$header"
done
test -f "$KERNEL_PRIVATE_OS/atomic_private.h"
sudo mkdir -p "$KERNEL_PRIVATE/machine" "$KERNEL_PRIVATE/arm"
sudo cp "$ROOT/kernel/xnu/upstream/osfmk/machine/cpu_number.h" "$KERNEL_PRIVATE/machine/cpu_number.h"
sudo cp "$ROOT/kernel/xnu/upstream/osfmk/arm/cpu_number.h" "$KERNEL_PRIVATE/arm/cpu_number.h"
sudo cp "$ROOT/kernel/xnu/upstream/osfmk/machine/cpu_capabilities.h" "$KERNEL_PRIVATE/machine/cpu_capabilities.h"
sudo cp "$ROOT/kernel/xnu/upstream/osfmk/arm/cpu_capabilities.h" "$KERNEL_PRIVATE/arm/cpu_capabilities.h"
test -f "$KERNEL_PRIVATE/machine/cpu_capabilities.h"
test -f "$KERNEL_PRIVATE/arm/cpu_capabilities.h"

# tracepoint_private.h includes atm/atm_internal.h when KERNEL is defined.
# These are the exact header paths and dependencies from the pinned XNU tree:
# osfmk/atm/atm_internal.h -> osfmk/atm/atm_types.h, libkern/os/refcnt.h
# libkern/os/refcnt.h -> libkern/os/refcnt_internal.h.
ATM_HEADERS="$KERNEL_PRIVATE/atm"
sudo mkdir -p "$ATM_HEADERS"
sudo cp "$ROOT/kernel/xnu/upstream/osfmk/atm/atm_internal.h" "$ATM_HEADERS/atm_internal.h"
sudo cp "$ROOT/kernel/xnu/upstream/osfmk/atm/atm_types.h" "$ATM_HEADERS/atm_types.h"
sudo cp "$ROOT/kernel/xnu/upstream/libkern/os/refcnt.h" "$KERNEL_PRIVATE_OS/refcnt.h"
sudo cp "$ROOT/kernel/xnu/upstream/libkern/os/refcnt_internal.h" "$KERNEL_PRIVATE_OS/refcnt_internal.h"
test -s "$ATM_HEADERS/atm_internal.h"
test -s "$ATM_HEADERS/atm_types.h"
test -s "$KERNEL_PRIVATE_OS/refcnt.h"
test -s "$KERNEL_PRIVATE_OS/refcnt_internal.h"

echo "xnu_private_atomic_headers=staged" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "xnu_private_cpu_capability_headers=staged_from_pinned_xnu_source" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "xnu_atm_headers=staged_from_pinned_xnu_source" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "xnu_refcnt_header_pair=staged_from_pinned_xnu_source" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "xnu_full_installhdrs=blocked_by_DriverKit_IOTypes.h_source_rule" >> "$EVIDENCE/dependency-prepare-status.txt"
FIREHOSE_HEADERS="$SDKROOT/usr/local/include/firehose"
sudo mkdir -p "$FIREHOSE_HEADERS"
sudo cp "$ROOT/kernel/xnu/upstream/libkern/firehose/firehose_types_private.h" "$FIREHOSE_HEADERS/firehose_types_private.h"
sudo cp "$ROOT/kernel/xnu/upstream/libkern/firehose/tracepoint_private.h" "$FIREHOSE_HEADERS/tracepoint_private.h"
sudo cp "$ROOT/kernel/xnu/upstream/libkern/firehose/chunk_private.h" "$FIREHOSE_HEADERS/chunk_private.h"
test -s "$FIREHOSE_HEADERS/firehose_types_private.h"
test -s "$FIREHOSE_HEADERS/tracepoint_private.h"
test -s "$FIREHOSE_HEADERS/chunk_private.h"
echo "xnu_firehose_private_headers=staged_from_pinned_xnu_source" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "xnu_firehose_chunk_header=staged_from_pinned_xnu_source" >> "$EVIDENCE/dependency-prepare-status.txt"

# Build the kernel firehose library from the release-manifest-pinned libdispatch.
DISPATCH_DST="$WORK/libdispatch-dst"
xcodebuild -project "$DISPATCH/libdispatch.xcodeproj" \
  -target libfirehose_kernel -configuration Release -sdk macosx \
  ARCHS="arm64 arm64e" VALID_ARCHS="arm64 arm64e" \
  PRODUCT_NAME=firehose_kernel DSTROOT="$DISPATCH_DST" install \
  2>&1 | tee "$EVIDENCE/libdispatch-build.log"
if [[ ! -d "$DISPATCH_DST/usr/local" ]]; then
  echo "libdispatch build did not stage usr/local" >&2
  exit 1
fi
sudo mkdir -p "$SDKROOT/usr/local"
sudo ditto "$DISPATCH_DST/usr/local" "$SDKROOT/usr/local"
echo "availabilityversions=installed" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "libdispatch=installed" >> "$EVIDENCE/dependency-prepare-status.txt"

# KDK must match the exact host macOS version/build. Never guess its name.
HOST_VERSION="$(sw_vers -productVersion)"
HOST_BUILD="$(sw_vers -buildVersion)"
KDK_ROOT=""
KDK_INFO_PLIST=""
KDK_BUNDLE_VERSION=""
for candidate in /Library/Developer/KDKs/*.kdk; do
  [[ -d "$candidate" ]] || continue
  if [[ "$(basename "$candidate")" == *"$HOST_VERSION"*"$HOST_BUILD"* ]]; then
    info_plist="$(find "$candidate" -path '*/System.kext/Info.plist' -print -quit)"
    [[ -n "$info_plist" ]] || continue
    bundle_version="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' "$info_plist" 2>/dev/null || true)"
    [[ -n "$bundle_version" ]] || continue
    KDK_ROOT="$candidate"
    KDK_INFO_PLIST="$info_plist"
    KDK_BUNDLE_VERSION="$bundle_version"
    break
  fi
done
if [[ -z "$KDK_ROOT" ]]; then
  echo "kdk_found=false" >> "$EVIDENCE/dependency-prepare-status.txt"
  echo "No KDK matching host $HOST_VERSION build $HOST_BUILD with readable System.kext CFBundleVersion metadata is installed." \
    | tee "$EVIDENCE/kdk-status.txt"
  exit 0
fi

echo "kdk_found=true" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "kdk_root=$KDK_ROOT" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "kdk_system_info_plist=$KDK_INFO_PLIST" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "kdk_system_bundle_version=$KDK_BUNDLE_VERSION" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "KDK_ROOT=$KDK_ROOT" >> "$GITHUB_ENV"
echo "SDKROOT=$SDKROOT" >> "$GITHUB_ENV"
echo "RC_DARWIN_KERNEL_VERSION=24.0.0" >> "$GITHUB_ENV"
