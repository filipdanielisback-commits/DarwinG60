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
# exact XNU private atomic header family without modifying the upstream source.
sudo mkdir -p "$SDKROOT/usr/local/include/os"
for header in atomic_private.h atomic_private_arch.h atomic_private_impl.h; do
  source="$ROOT/kernel/xnu/upstream/libkern/os/$header"
  test -f "$source"
  sudo cp "$source" "$SDKROOT/usr/local/include/os/$header"
done
test -f "$SDKROOT/usr/local/include/os/atomic_private.h"
echo "xnu_private_atomic_headers=staged" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "xnu_full_installhdrs=blocked_by_DriverKit_IOTypes.h_source_rule" >> "$EVIDENCE/dependency-prepare-status.txt"

# KDK must match the exact host macOS version/build. Never guess its name.
HOST_VERSION="$(sw_vers -productVersion)"
HOST_BUILD="$(sw_vers -buildVersion)"
KDK_ROOT=""
for candidate in /Library/Developer/KDKs/*.kdk; do
  [[ -d "$candidate" ]] || continue
  if [[ "$(basename "$candidate")" == *"$HOST_VERSION"*"$HOST_BUILD"* ]]; then
    KDK_ROOT="$candidate"
    break
  fi
done
if [[ -z "$KDK_ROOT" ]]; then
  echo "kdk_found=false" >> "$EVIDENCE/dependency-prepare-status.txt"
  echo "No KDK matching host $HOST_VERSION build $HOST_BUILD is installed." \
    | tee "$EVIDENCE/kdk-status.txt"
  exit 0
fi

echo "kdk_found=true" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "kdk_root=$KDK_ROOT" >> "$EVIDENCE/dependency-prepare-status.txt"
echo "KDK_ROOT=$KDK_ROOT" >> "$GITHUB_ENV"
echo "SDKROOT=$SDKROOT" >> "$GITHUB_ENV"
echo "RC_DARWIN_KERNEL_VERSION=24.0.0" >> "$GITHUB_ENV"
