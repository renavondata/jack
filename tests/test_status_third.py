"""C2a-3's pre-stated window, process continuity and ending-veto readings."""
import copy
import json
import os
import types
import unittest
from unittest.mock import patch

from judge import status as st
from tests.clerk_fixture import commit, tree
from tests.test_status import e


class ThirdWindowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(st.ROOT, 'log.jsonl')) as f:
            cls.record = [json.loads(line) for line in f]

    def setUp(self):
        self.es = list(self.record)
        self.add('forecast', '2026-11-29T00:00:00Z', args={'id': 'V8'}, resolves_by='2026-12-07T00:00:00Z')
        self.op = self.add('push', '2026-11-30T00:00:30Z')

    def add(self, typ, ts, **body):
        seq = self.es[-1]['seq'] + 1
        self.es.append(e(seq, ts, typ, 'counsel' if typ == 'forecast' else 'guy', **body))
        self.es[-1]['sig'] = next(x['sig'] for x in self.record if x['proposer'] == self.es[-1]['proposer'])
        return seq

    def status(self, es=None):
        return st.status(self.es if es is None else es, 'A3', 14, '2026-12-01T00:00:00Z', subject='C2a')

    def test_change_1_window_and_acts(self):
        self.assertEqual(self.status()['window'], 'C2a-3')
        self.assertEqual(self.status()['end'], '2026-12-07T00:00:00Z')
        self.assertEqual(self.status(self.es[:-1])['window'], 'C2a-prime')
        at_end = copy.deepcopy(self.es)
        at_end[-1]['ts'] = '2026-11-30T00:00:00Z'
        self.assertIsNone(st.c2a_third_window(at_end))
        promoted = self.es[:-1] + [e(self.op, '2026-11-30T00:00:00Z', 'decision', 'guy', kind='promote', subject='C2a'),
                                  dict(self.es[-1], seq=self.op + 1)]
        self.assertIsNone(st.c2a_third_window(promoted))
        no_v8 = self.es[:-2] + self.es[-1:]
        self.assertEqual(st.promotion_line(st.assess(no_v8, 'C2a', '2026-12-01T00:00:00Z', None, None)),
                         'promote C2a: refused: C2a-3 has no promotion forecast before its opening')
        self.assertFalse(st.status(no_v8 + [dict(self.es[-2], seq=self.op + 1)], 'A3', 14,
                                   '2026-12-01T00:00:00Z', subject='C2a')['v5'])
        s = self.status()
        with patch.object(st, 'c2a_tree_evidence', return_value=(True, True, True)), \
                patch.object(st, 'attack_start', return_value=None):
            checks = st.assess_value(s, dict(counted=9000, kernel=0, scope=True), True, st.ROOT, None, [],
                                     [dict(repo='renavondata/jack', time_hkt='2026-11-30 08:00', **{'class': 'repair'})])
        self.assertTrue(checks[2][0])
        self.assertEqual(checks[-1], (False, 'criterion 7: off-log repairs: 1'))
        s.update(subject='C2a', checks=checks)
        self.assertIn(f'window: C2a-3 (third window of C2a, opened seq {self.op})', st.render(s))

    def files(self, pins=()):
        scope = json.dumps(dict(counted=['tests/'], cap=9100))
        with open(st.__file__) as f, open(os.path.join(st.ROOT, 'tools/clerk.py')) as cf:
            src, clerk = f.read(), cf.read()
        return {'judge/scope.json': scope, 'SPEC.md': 'at C1 it is:\n```\n' + scope + '\n```\n',
                'log.jsonl': ''.join(json.dumps(e) + '\n' for e in self.es), 'judge/status.py': src,
                'tools/clerk.py': clerk, 'pins/pins.py': '\n'.join(f'Pin("{n}", t, m)' for n in (*st.VALUE_PINS, *pins))}

    def test_change_2_cap_scope_and_new_pins(self):
        files = self.files(st.THIRD_WINDOW_PINS)
        with tree(files) as (root, start):
            self.assertEqual(st.c2a_tree_evidence(root, start, self.es, self.op), (True, True, True))
            bad = commit(root, {'judge/scope.json': files['judge/scope.json'].replace('9100', '8400')})
            self.assertFalse(st.c2a_tree_evidence(root, bad, self.es, self.op)[0])
            restored = commit(root, {'judge/scope.json': files['judge/scope.json']})
            self.assertFalse(st.c2a_tree_evidence(root, restored, self.es, self.op)[0])
        with tree(self.files()) as (root, start):
            self.assertEqual(st.c2a_tree_evidence(root, start, self.es, self.op), (True, True, False))
            self.add('push', '2026-12-01T00:00:00Z')
            later = commit(root, {'log.jsonl': ''.join(json.dumps(e) + '\n' for e in self.es)})
            self.assertFalse(st.c2a_tree_evidence(root, later, self.es, self.op)[0])

    def test_change_3_names_and_real_process_unchanged(self):
        self.assertIn('C2a-3', st.WINDOW_NAMES)
        self.assertEqual(st.window_bounds(self.es, 'C2a-3'),
                         ('2026-11-30T00:00:30Z', '2026-12-07T00:00:00Z', '2026-12-07T00:00:00Z'))
        for subject, ts, name in [('C2a', '2026-11-29T00:00:00Z', 'C2a-prime'),
                                  ('C2a', '2026-12-01T00:00:00Z', 'C2a-3'),
                                  ('C2a-3', '2026-12-01T00:00:00Z', 'C2a-3'),
                                  ('C2a-prime', '2026-12-01T00:00:00Z', None)]:
            veto = e(self.op + 1, ts, 'decision', 'guy', kind='veto', subject=subject)
            self.assertEqual([n for n in ('C2a', 'C2a-prime', 'C2a-3') if st.names_window(self.es, veto, 'veto', n)],
                             [name] if name else [])
        old = types.ModuleType('previous_status')
        old.__file__ = st.__file__
        exec(compile(st.git_bytes(st.ROOT, 'show', 'cbdac17b:judge/status.py'), old.__file__, 'exec'), old.__dict__)
        before, after = old.window_fixes(self.record), st.window_fixes(self.record)
        self.assertEqual(after, before)
        opening = st.c1b_window(self.record)[0]
        self.assertEqual(st.item_process(self.record, opening, window_fixes=after),
                         old.item_process(self.record, opening, window_fixes=before))

    def test_change_4_process_reads_judge_source(self):
        files = self.files(st.THIRD_WINDOW_PINS)
        with tree(files) as (root, start):
            self.assertTrue(st.c2a_tree_evidence(root, start, self.es, self.op)[1])
            changed = files['judge/status.py'].replace('P0 = Fraction(6, 11)', 'P0 = Fraction(1, 2)')
            head = commit(root, {'judge/status.py': changed})
            self.assertFalse(st.c2a_tree_evidence(root, head, self.es, self.op)[1])
