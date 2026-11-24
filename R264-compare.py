#!/usr/bin/env python3
"""Adviser's comparison of the reviewer's second promotion replay table with the adviser's own rows.

usage: compare.py <table.json> <a clone of jack>
Every row of the table is compared with my row for the same commit: commit, log, argv, run (and its members' order),
exit and stdout; and, where my row is marked, the table's `marked` with the one I build from my two runs by the
brief's words: the second run's lines, with its `overdue forecast` lines after the `window C2a:` line taken out and
my own run's put where they stood, directly after the `J7:` line that follows that window line.
The header's spec, T and frozen are checked against the repository. `python` and `git` are not compared.
"""
import hashlib, json, os, subprocess, sys

ROWS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rows')
table, repo = json.load(open(sys.argv[1])), sys.argv[2]


def show(rev_path):
    return subprocess.run(['git', '-C', repo, 'show', rev_path], capture_output=True, check=True).stdout


def marked_from(R, V):
    w = [k for k, l in enumerate(V) if l.startswith('window C2a:')]
    wr = [k for k, l in enumerate(R) if l.startswith('window C2a:')]
    assert len(w) == 1 and len(wr) == 1, 'window lines'
    own = [l for k, l in enumerate(R) if k > wr[0] and l.startswith('overdue forecast')]
    j7 = [k for k, l in enumerate(V) if k > w[0] and l.startswith('J7:')]
    assert len(j7) == 1, 'J7 lines'
    out = []
    for k, l in enumerate(V):
        if k > w[0] and l.startswith('overdue forecast'):
            continue
        out.append(l)
        if k == j7[0]:
            out.extend(own)
    return out


T = table['T']
chain = subprocess.run(['git', '-C', repo, 'rev-list', '--first-parent', '--reverse', T], capture_output=True, check=True).stdout.decode().split()
print('T', T[:8], '| rows in the table', len(table['rows']), '| first-parent commits to T', len(chain),
      '| commits equal and in order:', [r['commit'] for r in table['rows']] == chain)
print('spec is the SHA-256 of SPEC.md at T:', table['spec'] == hashlib.sha256(show(f'{T}:SPEC.md')).hexdigest())
print('frozen holds the two files at T:', table['frozen'] == {p: hashlib.sha256(show(f'{T}:{p}')).hexdigest() for p in ('judge/status.py', 'judge/value.py')},
      list(table['frozen']))
agree, differ, pending, m_agree, m_table = 0, [], [], 0, 0
for i, tr in enumerate(table['rows']):
    p = os.path.join(ROWS, tr['commit'] + '.json')
    m_table += 'marked' in tr
    if not os.path.exists(p):
        pending.append(i)
        continue
    m = json.load(open(p))
    bad = [k for k in ('commit', 'log', 'argv', 'run', 'exit', 'stdout') if tr.get(k) != m.get(k)]
    if list(tr['run']) != list(m['run']):
        bad.append('run-order')
    if m['is_marked'] != ('marked' in tr):
        bad.append('marked-or-not')
    elif m['is_marked']:
        if tr['marked'] != marked_from(m['stdout'], m['v_stdout']):
            bad.append('marked')
        else:
            m_agree += 1
    if bad:
        differ.append((i, tr['commit'][:8], bad))
    else:
        agree += 1
print('rows that agree:', agree, '| rows that differ:', len(differ), '| rows I have not computed yet:', len(pending))
print('marked rows in the table:', m_table, '| marked rows whose `marked` agrees with mine:', m_agree)
for d in differ[:40]:
    print('  differs:', d)
if pending:
    print('  not yet computed: indices', pending[0], 'to', pending[-1], '(%d)' % len(pending))
