#!/bin/sh
set -eu
dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"$dir/build.sh"
export GOENV=off GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off GOWORK=off GO111MODULE=off
export GOTELEMETRY=off GOFLAGS=
export GOCACHE="$dir/.cache/build" GOTMPDIR="$dir/.cache/tmp" TMPDIR="$dir/.cache/tmp"
export CGO_ENABLED=0
cd -- "$dir"
exec go test -count=1 -v "$@" .
