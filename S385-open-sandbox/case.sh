#!/bin/bash
# case.sh NAME [keep] ; then copies results and removes the case unless NOCLEAN
SB=/tmp/q/sb; $SB/run.sh "$@"; R=$SB/cases/$1
cp "$R/out${2:+.2}.txt" "$SB/res/$1${2:+.2}.out"; cp "$R/ctl/calls" "$SB/res/$1${2:+.2}.calls" 2>/dev/null
[ -n "${NOCLEAN:-}" ] || rm -rf "$R"
