"""BRIEF-C2a-3 §Pins: behavioural witnesses without the runner's git history."""
import copy
import json
from unittest.mock import patch

from harness.gitfix import git
from judge import status as st
from tests.clerk_fixture import commit, tree
from tests.test_status import e
from tests.test_status_third import ThirdWindowTest


class Cases(ThirdWindowTest):
    def test_opening(self):
        self.test_change_1_window_and_acts()
        later = dict(self.es[-1], seq=self.op + 1, ts='2026-12-01T00:00:00Z')
        self.assertEqual(st.c2a_third_window(self.es + [later])[0], self.op)
        before = copy.deepcopy(self.es)
        before[-1]['ts'] = '2026-11-29T23:59:59Z'
        self.assertIsNone(st.c2a_third_window(before))

    def value_checks(self, s=None, counted=0, acts=()):
        with patch.object(st, 'c2a_tree_evidence', return_value=(True, True, True)), \
                patch.object(st, 'attack_start', return_value=None):
            return st.assess_value(s or self.status(), dict(counted=counted, kernel=0, scope=True),
                                   True, st.ROOT, None, [], list(acts))

    def test_cap(self):
        self.test_change_2_cap_scope_and_new_pins()
        for cap in (8400, 7800, 9101):
            files = self.files(st.THIRD_WINDOW_PINS)
            for path in ('judge/scope.json', 'SPEC.md'):
                files[path] = files[path].replace('9100', str(cap))
            with tree(files) as (root, head):
                self.assertFalse(st.c2a_tree_evidence(root, head, self.es, self.op)[0])
        self.assertTrue(self.value_checks(counted=9100)[2][0])
        self.assertFalse(self.value_checks(counted=9101)[2][0])

    def test_scope(self):
        files = self.files(st.THIRD_WINDOW_PINS)
        before = dict(files)
        before['log.jsonl'] = ''.join(json.dumps(x) + '\n' for x in self.es[:-2])
        for path in ('judge/scope.json', 'SPEC.md'):
            before[path] = before[path].replace('9100', '8400')
        with tree(before) as (root, base):
            trunk = git(root, 'symbolic-ref', '--short', 'HEAD')
            git(root, 'branch', 'preopening', base)
            commit(root, files)
            git(root, 'checkout', '-q', 'preopening')
            commit(root, {'side.txt': 'old-scope branch\n'})
            git(root, 'checkout', '-q', trunk)
            git(root, '-c', 'user.name=t', '-c', 'user.email=t@t', 'merge', '-q', '--no-ff', '--no-edit', 'preopening')
            self.assertTrue(st.c2a_tree_evidence(root, git(root, 'rev-parse', 'HEAD'), self.es, self.op)[0])
        for path in ('judge/scope.json', 'SPEC.md'):
            with tree(files) as (root, start):
                commit(root, {path: files[path].replace('9100', '8400')})
                restored = commit(root, {path: files[path]})
                self.assertFalse(st.c2a_tree_evidence(root, restored, self.es, self.op)[0])

    def test_names(self):
        self.assertIn('C2a-3', st.WINDOW_NAMES)
        self.assertEqual(st.window_bounds(self.es, 'C2a-3'),
                         ('2026-11-30T00:00:30Z', '2026-12-07T00:00:00Z', '2026-12-07T00:00:00Z'))
        for subject, ts, name in [('C2a-prime', '2026-11-29T00:00:00Z', 'C2a-prime'),
                                  ('C2a', '2026-11-29T00:00:00Z', 'C2a-prime'),
                                  ('C2a', '2026-12-01T00:00:00Z', 'C2a-3'),
                                  ('C2a-3', '2026-12-01T00:00:00Z', 'C2a-3'),
                                  ('C2a-prime', '2026-12-01T00:00:00Z', None)]:
            veto = e(self.op + 1, ts, 'decision', 'guy', kind='veto', subject=subject)
            self.assertEqual([n for n in ('C2a', 'C2a-prime', 'C2a-3')
                              if st.names_window(self.es, veto, 'veto', n)], [name] if name else [])
            with patch.object(st, 'tree_facts', return_value=dict(counted=0, kernel=0, scope=True)), \
                    patch.object(st, 'assess_value', return_value=[]):
                s = st.assess(self.es + [veto], 'C2a', '2026-12-01T00:00:00Z', None, None)
            self.assertEqual(s['checks'][0][0], name != 'C2a-3')

    def test_acts(self):
        row = lambda minute: dict(repo='renavondata/jack', time_hkt=minute, **{'class': 'repair'})
        old = [row('2026-11-18 08:00'), row('2026-11-29 08:00'), row('2026-11-30 07:59')]
        self.assertEqual(self.value_checks(acts=old)[-1], (True, 'criterion 7: off-log repairs: 0'))
        self.assertEqual(self.value_checks(acts=old + [row('2026-11-30 08:00')])[-1],
                         (False, 'criterion 7: off-log repairs: 1'))

    def test_veto_end(self):
        self.test_change_6_veto_reads_prefix_but_keeps_current_overdue()
        veto = next(x for x in self.record if x['seq'] == 7180)
        prefix = [x for x in self.record if x['seq'] <= veto['seq']]
        context = dict(es=prefix, subject='C2a', as_of=veto['ts'], root=st.ROOT, rev=None)
        with patch.object(st, 'tree_facts', return_value=dict(counted=9000, kernel=0, scope=True)), \
                patch.object(st, 'c2a_tree_evidence', return_value=(True, True, True)), \
                patch.object(st, 'attack_start', return_value=None), \
                patch.object(st, 'prefix_tree', return_value=None):
            at_veto = st.report(**context)
            self.assertEqual(at_veto['as_of'], veto['ts'])
            self.assertEqual(at_veto['prefix_last_seq'], veto['seq'])
            for entries in (prefix, self.record):
                now = dict(context, es=entries, as_of='2026-11-29T00:00:00Z')
                ended, current = st.report(**now), st.assess(**now)
                expected = dict(at_veto)
                expected.update({k: current[k] for k in ('overdue',)})
                self.assertEqual(ended, expected)
                self.assertTrue(ended['overdue'])
            third = st.report(**dict(context, es=self.es, as_of='2026-12-01T00:00:00Z'))
            self.assertEqual((third['window'], third['as_of']), ('C2a-3', '2026-12-01T00:00:00Z'))
