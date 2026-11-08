#!/usr/bin/env bash
# Installer for the jack-runner host user on steel (transcripts/runner/host.md §1-§2).
set -euo pipefail

STAGING="/root/jack-host"
OLD="/home/g"
ROOT_DIR=""

while [ $# -gt 0 ]; do
  case "$1" in
    --staging) STAGING="${2%/}"; shift 2 ;;
    --staging=*) STAGING="${1#*=}"; STAGING="${STAGING%/}"; shift ;;
    --old-home) OLD="${2%/}"; shift 2 ;;
    --old-home=*) OLD="${1#*=}"; OLD="${OLD%/}"; shift ;;
    --root) ROOT_DIR="${2%/}"; shift 2 ;;
    --root=*) ROOT_DIR="${1#*=}"; ROOT_DIR="${ROOT_DIR%/}"; shift ;;
    *) echo "refused: unknown option: $1" >&2; exit 1 ;;
  esac
done

NEW_HOME="${ROOT_DIR}/home/jack-runner"
STAGED_FILES=".ssh/jack-builder .ssh/jack-builder.pub .ssh/jack-reviewer .ssh/jack-reviewer.pub .ssh/jack-herald .ssh/jack-herald.pub .ssh/jack-counsel-3 .ssh/jack-counsel-3.pub .ssh/deploy-jack .ssh/deploy-jack.pub .config/jack/app-id .config/jack/app.pem .config/jack/gh-counsel"

! pgrep -f "$OLD/.local/share/actions-runner-[^/]*/bin/Runner.Worker" >/dev/null 2>&1 || { echo "refused: Runner.Worker is running under $OLD" >&2; exit 1; }
ahead=$(git -C "$OLD/git/jack" for-each-ref --format='%(refname:short)' refs/heads/ | while read -r b; do if [ -n "$(git -C "$OLD/git/jack" rev-list "origin/$b..$b" 2>/dev/null || git -C "$OLD/git/jack" rev-list "$b" --not --remotes=origin)" ]; then echo "$b"; fi; done); [ -z "$ahead" ] || { echo "refused: local branch ahead of origin: $ahead" >&2; exit 1; }
[ -d "$STAGING" ] || { echo "refused: staging directory $STAGING does not exist" >&2; exit 1; }
for rel in $(find "$STAGING" -mindepth 1 \( -type f -o -type l \) -printf '%P\n' | sort); do case " $STAGED_FILES " in *" $rel "*) ;; *) echo "refused: unexpected staged file: $rel" >&2; exit 1 ;; esac; done
for rel in $STAGED_FILES; do [ -f "$STAGING/$rel" ] || { echo "refused: missing staged file: $rel" >&2; exit 1; }; done

if [ -n "$ROOT_DIR" ]; then
  echo "useradd --system --home-dir /home/jack-runner --create-home --shell /usr/sbin/nologin jack-runner"
  echo "chmod 700 /home/jack-runner"
  echo "for d in $OLD/.local/share/actions-runner-*; do (cd \"\$d\" && ./svc.sh stop && ./svc.sh uninstall); done"
else
  id -u jack-runner >/dev/null 2>&1 || useradd --system --home-dir /home/jack-runner --create-home --shell /usr/sbin/nologin jack-runner
  mkdir -p /home/jack-runner && chmod 700 /home/jack-runner
  for d in "$OLD"/.local/share/actions-runner-*; do
    if [ -d "$d" ] && [ -x "$d/svc.sh" ]; then (cd "$d" && ./svc.sh stop || true; ./svc.sh uninstall || true); fi
  done
fi

mkdir -p -m 700 "$NEW_HOME" "$NEW_HOME/.ssh" "$NEW_HOME/.config/jack"
for rel in $(find "$STAGING" -mindepth 1 \( -type f -o -type l \) -printf '%P\n' | sort); do
  if [ "$rel" = ".ssh/deploy-jack.pub" ]; then continue; fi
  dst="$NEW_HOME/$rel"
  mkdir -p "$(dirname "$dst")"
  if [ ! -f "$dst" ] || ! cmp -s "$STAGING/$rel" "$dst"; then
    install -m 600 "$STAGING/$rel" "$dst"
  else
    chmod 600 "$dst"
  fi
done
[ -f "$NEW_HOME/.gitconfig" ] || printf '[user]\n\tname = jack-runner\n\temail = jack-runner@steel\n' > "$NEW_HOME/.gitconfig"
printf 'Host github-jack\n  HostName github.com\n  IdentityFile ~/.ssh/deploy-jack\n' > "$NEW_HOME/.ssh/config"
chmod 644 "$NEW_HOME/.ssh/config"
meta_keys=$(curl -fsSL --max-time 5 https://api.github.com/meta 2>/dev/null | python3 -c 'import json,sys; [print("github.com", k) for k in json.load(sys.stdin)["ssh_keys"]]' 2>/dev/null || true)
if [ -z "$meta_keys" ]; then
  meta_keys=$(printf '%s\n' \
    "github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl" \
    "github.com ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5YRrYMjNuG5N87uRgg6CLrbo5wAdT/y6v0mKV0U2w0WZ2YB/++Tpockg=" \
    "github.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz0wQZ75XK5tKSb7FNyeIEs4TT4jk+S4dhPeAUC5y+bDYirYgM4GC7uEnztnZyaVWQ7B381AK4Qdrwt51ZqExKbQpTUNn+EjqoTwvqNj4kqx5QUCI0ThS/YkOxJCXmPUWZbhjpCg56i+2aB6CmK2JGhn57K5mj0MNdBXA4/WnwH6XoPWJzK5Nyu2zB3nAZp+S5hpQs+p1vN1/wsjk=")
fi
printf '%s\n' "$meta_keys" > "$NEW_HOME/.ssh/known_hosts"
chmod 644 "$NEW_HOME/.ssh/known_hosts"

if [ -n "$ROOT_DIR" ]; then
  echo "git clone git@github-jack:renavondata/jack.git /home/jack-runner/git/jack && git -C /home/jack-runner/git/jack fetch origin"
  echo "mkdir -p /home/jack-runner/git/worktrees/jack"
  echo "cp -a $OLD/.npm-global /home/jack-runner/.npm-global"
  echo "cp -a $OLD/.config/opencode /home/jack-runner/.config/opencode"
  echo "chown -R jack-runner:jack-runner /home/jack-runner"
  echo "mv $OLD/.local/share/actions-runner-* /home/jack-runner/.local/share/ && write .path && chown -R jack-runner:jack-runner"
  echo "for d in /home/jack-runner/.local/share/actions-runner-*; do (cd \"\$d\" && ./svc.sh install jack-runner && ./svc.sh start); done"
  echo "chmod 700 $OLD"
  exit 0
fi

mkdir -p /home/jack-runner/git/worktrees/jack /home/jack-runner/.config /home/jack-runner/.local/share
if [ -d "$OLD/.npm-global" ] && [ ! -d /home/jack-runner/.npm-global ]; then cp -a "$OLD/.npm-global" /home/jack-runner/.npm-global; fi
if [ -d "$OLD/.config/opencode" ] && [ ! -d /home/jack-runner/.config/opencode ]; then cp -a "$OLD/.config/opencode" /home/jack-runner/.config/opencode; fi
chown -R jack-runner:jack-runner /home/jack-runner
if [ ! -d /home/jack-runner/git/jack/.git ]; then
  runuser -u jack-runner -- env HOME=/home/jack-runner git clone git@github-jack:renavondata/jack.git /home/jack-runner/git/jack
fi
runuser -u jack-runner -- env HOME=/home/jack-runner git -C /home/jack-runner/git/jack fetch origin
for d in "$OLD"/.local/share/actions-runner-*; do
  if [ ! -d "$d" ]; then continue; fi
  mv "$d" "/home/jack-runner/.local/share/$(basename "$d")"
done
for d in /home/jack-runner/.local/share/actions-runner-*; do
  if [ ! -d "$d" ]; then continue; fi
  printf '/home/jack-runner/.npm-global/bin:%s\n' "${PATH}" > "$d/.path"
  chown -R jack-runner:jack-runner "$d"
  unit=""
  if [ -f "$d/.service" ]; then unit=$(tr -d '[:space:]' < "$d/.service"); fi
  if [ -z "$unit" ] || [ "$(systemctl show -p User --value "$unit" 2>/dev/null || true)" != "jack-runner" ]; then
    (cd "$d" && PATH="/home/jack-runner/.npm-global/bin:$PATH" ./svc.sh install jack-runner && ./svc.sh start)
    printf '/home/jack-runner/.npm-global/bin:%s\n' "${PATH}" > "$d/.path"
    chown -R jack-runner:jack-runner "$d"
  elif ! systemctl is-active --quiet "$unit"; then
    (cd "$d" && ./svc.sh start)
  fi
done
chmod 700 "$OLD"
