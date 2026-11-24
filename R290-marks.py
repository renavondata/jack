#!/usr/bin/env python3
"""Adviser's check of the brief's conditions at the marked rows of the second promotion replay table (ADVISER.md entry 290).

usage: R290-marks.py <table.json> <the directory of my rows, as R264-driver.py writes them>
At each row the table marks, from my own two runs (R as the row's arguments stand, V with --as-of 2026-11-22T11:44:05Z):
the exit statuses are equal; the lines before the one that begins `window C2a:` are equal (the history); the lines that
begin `sovereign REPAIR` are equal; and the table's `marked` differs from its `stdout` in no line before that window line.
It also counts the rows where the two runs' `overdue forecast` lines after the window line differ.
"""
import json, os, sys
table, rows = json.load(open(sys.argv[1])), sys.argv[2]
n = exits = hist = rep = pre = over = 0
first = last = None
for i, tr in enumerate(table['rows']):
    if 'marked' not in tr:
        continue
    m = json.load(open(os.path.join(rows, tr['commit'] + '.json')))
    R, V = m['stdout'], m['v_stdout']
    wr = next(k for k, l in enumerate(R) if l.startswith('window C2a:'))
    wv = next(k for k, l in enumerate(V) if l.startswith('window C2a:'))
    n += 1
    first = i if first is None else first
    last = i
    exits += m['exit'] == m['v_exit'] == tr['exit']
    hist += R[:wr] == V[:wv]
    rep += [l for l in R if l.startswith('sovereign REPAIR')] == [l for l in V if l.startswith('sovereign REPAIR')]
    pre += tr['marked'][:wr] == tr['stdout'][:wr]
    over += [l for l in R[wr:] if l.startswith('overdue forecast')] != [l for l in V[wv:] if l.startswith('overdue forecast')]
print('marked rows', n, '| indices', first, 'to', last, '| exits equal', exits, '| history equal', hist,
      '| sovereign REPAIR lines equal', rep, '| marked equals stdout before the window line', pre,
      '| rows whose overdue lines differ between the runs', over)
