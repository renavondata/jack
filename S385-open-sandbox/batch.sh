#!/bin/bash
cd /tmp/q/sb
( exec -a "bash /x/.cache/jack-paste-open.sh" sleep 200 ) & F1=$!
./case.sh B; kill $F1 2>/dev/null
NOV8=1 ./case.sh C
C_TIMER=stopped ./case.sh D
C_PUSH="moved ok" ./case.sh E
C_PUSH=other NOCLEAN=1 ./case.sh F
C_PUSH=ok ./case.sh F keep
C_TIMER="far far far near" ./case.sh H
C_REPLAY=3 ./case.sh I
C_LANE=2 ./case.sh J
C_FIX=refuse ./case.sh K
C_REPLAY="1 1 1 0 1" ./case.sh L
echo BATCHDONE > res/done
