#!/usr/bin/env bash
# Post-install witness check for jack-runner on steel (transcripts/runner/host.md §2).
set -uo pipefail

NEW_HOME="${JACK_RUNNER_HOME:-/home/jack-runner}"
OLD_HOME="${JACK_OLD_HOME:-/home/g}"
RUNNER_USER="${JACK_RUNNER_USER:-jack-runner}"
UNITS_DIR="${JACK_UNITS_DIR:-/etc/systemd/system}"
 fail=0

report() {
  if [ "$1" -eq 0 ]; then
    echo "ok: $2"
  else
    echo "FAIL: $2"
    fail=1
  fi
}

run_as_runner() {
  if [ "$(id -un)" = "$RUNNER_USER" ]; then
    HOME="$NEW_HOME" "$@"
  elif command -v runuser >/dev/null 2>&1 && [ "$(id -u)" -eq 0 ]; then
    runuser -u "$RUNNER_USER" -- env HOME="$NEW_HOME" "$@"
  else
    sudo -u "$RUNNER_USER" env HOME="$NEW_HOME" "$@"
  fi
}

units=$(find "$UNITS_DIR" -maxdepth 1 -name 'actions.runner.renavondata-opencode-runner.*.service' -printf '%f\n' 2>/dev/null | sort || true)
if [ -z "$units" ]; then
  report 1 "runner units: none found under $UNITS_DIR"
else
  for u in $units; do
    u_user=$(sed -n 's/^User=//p' "$UNITS_DIR/$u" | head -1)
    [ "$u_user" = "$RUNNER_USER" ]
    report $? "unit $u User=${u_user:-unset}"
  done
fi

expected_ssh=$(printf '%s\n' config deploy-jack jack-builder jack-builder.pub jack-counsel-3 jack-counsel-3.pub jack-herald jack-herald.pub jack-reviewer jack-reviewer.pub known_hosts | sort)
actual_ssh=$(find "$NEW_HOME/.ssh" -mindepth 1 -printf '%P\n' 2>/dev/null | sort || true)
[ "$actual_ssh" = "$expected_ssh" ]
report $? ".ssh files match expected eleven names"

expected_cfg1=$(printf '%s\n' app-id app.pem gh-counsel | sort)
expected_cfg2=$(printf '%s\n' .token app-id app.pem gh-counsel | sort)
actual_cfg=$(find "$NEW_HOME/.config/jack" -mindepth 1 -printf '%P\n' 2>/dev/null | sort || true)
[ "$actual_cfg" = "$expected_cfg1" ] || [ "$actual_cfg" = "$expected_cfg2" ]
report $? ".config/jack files match expected names"

mode_err=""
for f in $(find "$NEW_HOME/.ssh" "$NEW_HOME/.config/jack" -mindepth 1 -type f 2>/dev/null | sort); do
  owner=$(stat -c '%U' "$f")
  mode=$(stat -c '%a' "$f")
  base=$(basename "$f")
  want="600"
  if [ "$base" = "config" ] || [ "$base" = "known_hosts" ]; then want="644"; fi
  if [ "$owner" != "$RUNNER_USER" ] || [ "$mode" != "$want" ]; then
    mode_err="$mode_err $f(owner=$owner,mode=$mode,want=$RUNNER_USER:$want)"
  fi
done
[ -z "$mode_err" ] && [ -d "$NEW_HOME/.ssh" ] && [ -d "$NEW_HOME/.config/jack" ]
report $? ".ssh and .config/jack ownership ($RUNNER_USER) and modes (600, config/known_hosts 644)${mode_err}"

! run_as_runner gh auth status >/dev/null 2>&1
report $? "gh auth status as $RUNNER_USER reports no login"

! run_as_runner test -r "$OLD_HOME/.config/gh/hosts.yml"
report $? "$OLD_HOME/.config/gh/hosts.yml unreadable to $RUNNER_USER"

run_as_runner git -C "$NEW_HOME/git/jack" fetch >/dev/null 2>&1
report $? "git -C ~/git/jack fetch as $RUNNER_USER"

run_as_runner git -C "$NEW_HOME/git/jack" push --dry-run origin HEAD:refs/heads/host-check >/dev/null 2>&1
report $? "git -C ~/git/jack push --dry-run origin HEAD:refs/heads/host-check as $RUNNER_USER"

exit "$fail"
