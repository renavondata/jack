#!/bin/sh
set -eu
dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$dir/.cache/build" "$dir/.cache/tmp"
# Build/runtime artifacts stay in kernel2; toolchain downloads are disabled.
export GOENV=off GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOWORK=off GO111MODULE=off
export GOTELEMETRY=off GOFLAGS=
export GOCACHE="$dir/.cache/build" GOTMPDIR="$dir/.cache/tmp" TMPDIR="$dir/.cache/tmp"
export CGO_ENABLED=0
go build -trimpath -ldflags="-X main.badSignatureReason=${1:-bad_signature}" \
    -o "$dir/.cache/check" \
    "$dir/main.go" "$dir/canonical.go" "$dir/ed25519.go" \
    "$dir/signature.go" "$dir/checker.go"
