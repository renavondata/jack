#!/usr/bin/env python3
"""Adviser's test of the hashes that freshness resolutions cite (ADVISER.md entry 297).

usage: R297-hashes.py <a clone of jack with origin/main fetched>
For every resolution on main's log with ts from 2026-11-22T00:00:00Z whose evidence names a saved page under
transcripts/evidence/renavon-freshness/ and a sha256, the SHA-256 of that file on origin/main is compared with the one cited.
"""
import collections, hashlib, json, re, subprocess, sys
repo = sys.argv[1]
show = lambda p: subprocess.run(['git', '-C', repo, 'show', 'origin/main:' + p], capture_output=True)
L = [json.loads(l) for l in show('log.jsonl').stdout.decode().splitlines()]
n, bad, day, tot = 0, [], collections.Counter(), collections.Counter()
for e in L:
    if e['type'] != 'resolution' or e['ts'] < '2026-11-22T00:00:00Z':
        continue
    m = re.search(r'(transcripts/evidence/renavon-freshness/\S+?\.html) sha256:([0-9a-f]+)', e['body']['evidence'])
    if not m:
        continue
    n += 1
    tot[e['ts'][:10]] += 1
    r = show(m.group(1))
    if r.returncode or hashlib.sha256(r.stdout).hexdigest() != m.group(2):
        bad.append(e['seq'])
        day[e['ts'][:10]] += 1
print('cite a file and a hash:', n, '| not the file\'s:', len(bad), '| by day:', {d: f'{day[d]} of {tot[d]}' for d in sorted(tot)})
print('seqs:', bad)
