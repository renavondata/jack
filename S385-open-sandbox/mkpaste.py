import re,sys
s=open('/tmp/q/open4.sh').read()
a=s.index('replay_next() {'); b=s.index('  case $? in 0) return 0;; 10) return 1;; 3) return 3;; *) return 4;; esac\n}\n')+len('  case $? in 0) return 0;; 10) return 1;; 3) return 3;; *) return 4;; esac\n}\n')
stub='replay_next() {  # SANDBOX STUB: codes from $SB_CTL/replay, default 1 (caught up)\n  git fetch -q origin main || return 2\n  local c; c=$(head -1 "$SB_CTL/replay" 2>/dev/null); [ -n "$c" ] && sed -i 1d "$SB_CTL/replay"; echo "replay: ${c:-1}" >> "$SB_CTL/calls"; return ${c:-1}\n}\n'
s=s[:a]+stub+s[b:]
assert s.count('END=1795996800')==1; s=s.replace('END=1795996800','END=1   # SANDBOX: the stated end taken as passed')
assert s.count('    sleep 30\n')==1; s=s.replace('    sleep 30\n','    sleep 2   # SANDBOX\n')
open('/tmp/q/sb/paste-sb.sh','w').write(s)
