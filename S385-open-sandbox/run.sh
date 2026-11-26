#!/bin/bash
# usage: run.sh CASE [keep]   controls in env: C_REPLAY C_TIMER C_PUSH C_FIX C_LANE NOV8
SB=/tmp/q/sb; C=$1; R=$SB/cases/$C
if [ "${2:-}" != keep ]; then
  rm -rf "$R"; mkdir -p "$R/home/git" "$R/home/.cache" "$R/ctl"
  git -C $SB/base/origin.git update-ref refs/heads/main "$(cat $SB/base/main0)"
  [ -n "${NOV8:-}" ] && git -C $SB/base/origin.git update-ref refs/heads/main 283b71ff979e82142abb659a5757b1795035937b
  git clone -q -b main $SB/base/origin.git "$R/home/git/jack-guy"
  git -C "$R/home/git/jack-guy" config user.name sb; git -C "$R/home/git/jack-guy" config user.email sb@invalid
  cp $SB/paste-sb.sh "$R/home/.cache/jack-paste-open.sh"
fi
printf '%s\n' ${C_REPLAY:-} > "$R/ctl/replay"; printf '%s\n' ${C_TIMER:-} > "$R/ctl/timer"; printf '%s\n' ${C_PUSH:-} > "$R/ctl/push"; printf '%s\n' ${C_FIX:-} > "$R/ctl/fix"; echo ${C_LANE:-0} > "$R/ctl/lanebusy"
cd "$R/home" && HOME="$R/home" SB_CTL="$R/ctl" PATH="$SB/bin:$PATH" GIT_CONFIG_GLOBAL=/dev/null bash "$R/home/.cache/jack-paste-open.sh" > "$R/out${2:+.2}.txt" 2>&1; echo "exit $?" >> "$R/out${2:+.2}.txt"
