"""C2a-prime v7 witnesses supplementing the builder's committed history fixtures."""
from unittest.mock import patch
from tests import test_c2a_prime as fx
from tools import status as st


def test_opening():
    es = fx.base() + [fx.e(368, "push", "guy", "2026-11-16T00:00:00Z"), fx.e(369, "push", "guy", fx.PUSH)]
    assert st.second_opening(es)["seq"] == 369


def test_offlog_and_promotion():
    es = fx.base() + [fx.e(368, "forecast", ts=fx.END, args={"id": "V5"}, resolves_by=fx.V5)]
    acts = list(st.csv.DictReader((fx.HEADER + fx.ROW * 9).splitlines()))
    def assess(entries, when):
        s = st.status(entries, "A3", 14, when, subject="C2a")
        s["checks"] = st.assess_value(s, dict(counted=8400, kernel=500, scope=True), True, st.ROOT, None, [], acts)
        s["checks"].append((not s["veto"], "criterion 7: veto"))
        s.update(subject="C2a", repairs=[])
        return s
    with patch.object(st, "c2a_tree_evidence", return_value=(True, True, True)), patch.object(st, "signer_blob", side_effect=lambda e: e["proposer"]):
        first = assess(es + [fx.e(369, "decision", "guy", fx.FIX, kind="promote", subject="C2a")], fx.FIX)
        assert first["window"] == "C2a" and "window: C2a-prime" not in st.render(first)
        assert "promote C2a: refused:" in st.render(first) and "criterion 7: off-log repairs: 9" in st.promotion_line(first)
        es += [fx.e(369, "decision", "guy", fx.FIX, kind="veto", subject="C2a"), fx.e(370, "push", "guy", fx.PUSH)]
        second = assess(es, fx.AFTER)
        assert second["window"] == "C2a-prime" and second["checks"][-2:] == [(True, "criterion 7: off-log repairs: 0"), (True, "criterion 7: veto")]
        vetoed = assess(es + [fx.e(371, "decision", "guy", fx.AFTER, kind="veto", subject="C2a-prime")], fx.AFTER)
        assert vetoed["veto"] and "criterion 7: veto" in st.promotion_line(vetoed)
        es[-1]["ts"] = "2026-11-18T00:00:30Z"
        acts[:] = [dict(repo="renavondata/jack", time_hkt="2026-11-18 08:00", **{"class": "repair"})]
        boundary = assess(es, "2026-11-18T00:00:31Z")
        assert boundary["checks"][-2] == (False, "criterion 7: off-log repairs: 1")


def test_contains_name(capsys):
    original = fixture_entry(fx.e)
    def entry(*args, **kwargs):
        if kwargs.get("subject") == "a free-text repair":
            kwargs["subject"] = "repair C2a: acts"
        return original(*args, **kwargs)
    with patch.object(fx, "e", side_effect=entry):
        fx.test_window_fix_is_decision("free", capsys)


def fixture_entry(original):
    def entry(seq, typ, who="counsel", ts=None, **body):
        kwargs = dict(body)
        if ts is not None:
            kwargs["ts"] = "2026-11-16T12:00:00Z" if ts == fx.LATE and typ == "decision" else fx.AFTER if ts == fx.PUSH and typ in ("resolution", "merge") else ts
        return original(seq, typ, "herald" if typ in ("resolution", "merge") else who, **kwargs)
    return entry


@fx.pytest.mark.parametrize("case", "decision stem free unnamed later-file raw-only raw-both outside partial-minute promoted early after-push second-fix history veto replacement bad-header bad-hash late-promote late-veto between veto-history wrong-classifier missing-raw missing-classifier".split())
def test_fix_cases(case, capsys):
    with patch.object(fx, "e", side_effect=fixture_entry(fx.e)):
        fx.test_window_fix_is_decision(case, capsys)


def test_nonretroactive_batches():
    with patch.object(fx, "e", side_effect=fixture_entry(fx.e)):
        fx.test_window_fix_not_retroactive()


def test_guard_tuple_and_dependency():
    # The listed tuple comes from the opening; dropping a root must not hide its edit.
    es = fx.base() + [fx.e(368, "forecast", ts=fx.END, args={"id": "V5"}, resolves_by=fx.V5), fx.e(369, "push", "guy", fx.PUSH)]
    source = st.tree_bytes(st.ROOT, None, "tools/status.py").decode()
    source = source.replace('qualified, seen = set(), set()', 'qualified, seen = set(), set()\n    fix_helper()')
    source += '\ndef fix_helper():\n    return fix_leaf()\ndef fix_leaf():\n    return 123\n'
    scope = fx.json.dumps({"cap": 8400, "counted": ["tools/"]})
    files = {"log.jsonl": fx.log(es), "tools/status.py": source, "tools/clerk.py": "", "judge/scope.json": scope,
             "SPEC.md": "at C1 it is:\n```\n" + scope + "\n```", "pins/pins.py": "\n".join(f'Pin("{p}"' for p in st.VALUE_PINS)}
    with fx.tree(files) as (root, opening):
        assert st.c2a_tree_evidence(root, opening, es, 369, True)[1] is True
        changed = source.replace('"attributed_failure", "window_fix_seqs")', '"window_fix_seqs",)').replace('r["class"] == "repair"', 'True')
        head = fx.commit(root, {"tools/status.py": changed})
        assert st.c2a_tree_evidence(root, head, es, 369, True)[1] is False
        head = fx.commit(root, {"tools/status.py": source.replace('return 123', 'return 124')})
        assert st.c2a_tree_evidence(root, head, es, 369, True)[1] is False


def test_cap_history():
    es = fx.base() + [fx.e(368, "forecast", ts=fx.END, args={"id": "V5"}, resolves_by=fx.V5), fx.e(369, "push", "guy", fx.PUSH)]
    def scope(cap):
        text = fx.json.dumps({"cap": cap, "counted": ["tools/"]})
        return {"judge/scope.json": text, "SPEC.md": "at C1 it is:\n```\n" + text + "\n```"}
    files = dict(scope(8400), **{"log.jsonl": fx.log(es), "tools/status.py": st.tree_bytes(st.ROOT, None, "tools/status.py").decode(),
                               "tools/clerk.py": "", "pins/pins.py": "\n".join(f'Pin("{p}"' for p in st.VALUE_PINS)})
    with fx.tree(files) as (root, opening):
        assert st.c2a_tree_evidence(root, opening, es, 369, True)[0] is True
        changed = fx.commit(root, scope(8401))
        assert st.c2a_tree_evidence(root, changed, es, 369, True)[0] is False
        reverted = fx.commit(root, scope(8400))
        assert st.c2a_tree_evidence(root, reverted, es, 369, True)[0] is False
