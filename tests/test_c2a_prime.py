"""BRIEF-C2a-prime v5: boundary witnesses, disposable history, and inert-prefix oracle."""
import hashlib
import json
from unittest.mock import patch
import pytest
from tests.clerk_fixture import commit, tree
from tests.test_value import e
from tools import status as st

OPEN, END, LATE = "2026-11-01T15:04:14Z", "2026-11-15T15:04:14Z", "2026-11-17T12:00:00Z"
FIX, PUSH, AFTER = "2026-11-17T12:00:01Z", "2026-11-17T12:00:02Z", "2026-11-17T12:00:03Z"
V5 = "2026-11-30T00:00:00Z"
HEADER = "repo,time_hkt,class,kind,ref,note\n"
ROW = "renavondata/jack,2026-11-02 22:11,repair,close,1,fixture\n"
PATH = "transcripts/evidence/acts"


def base():
    return [e(0, "genesis", keys=[{"pubkey": "ssh-ed25519 guy", "key_id": "guy", "principal": "guy", "powers": ["forecast"]}]),
            e(1, "forecast", args={"id": "L0"}, resolves_by=V5), e(2, "decision", "guy", kind="promote", subject="C1a"),
            e(3, "forecast", resolves_by=V5), e(4, "resolution", forecast=3, outcome=1), e(5, "merge"), e(6, "forecast", resolves_by=V5),
            e(360, "forecast", args={"id": "V0"}, resolves_by=LATE), e(367, "push", "guy", OPEN)]


def log(es):
    return "\n".join(map(json.dumps, es)) + "\n"


@pytest.mark.parametrize("case", ["decision", "stem", "free", "unnamed", "later-file", "raw-only", "outside", "partial-minute",
                                  "promoted", "early", "after-push", "second-fix", "history", "veto", "replacement", "bad-header", "bad-hash",
                                  "late-promote", "late-veto", "between", "veto-history", "wrong-classifier", "missing-raw", "missing-classifier"])
def test_window_fix_is_decision(case, capsys):
    es = base()
    subject = "a free-text repair" if case == "free" else "C2a: " + ("no file" if case in ("unnamed", "veto", "late-veto", "veto-history") else "(acts)" if case == "stem" else "acts.csv")
    kinds = {"promoted": "promote", "late-promote": "promote", "veto": "veto", "late-veto": "veto", "veto-history": "veto", "second-fix": "fix"}
    if case in kinds:
        es.append(e(368, "decision", "guy", LATE if case.startswith("late-") else END, kind=kinds[case], subject="C2a: earlier" if case == "second-fix" else "C2a"))
    fix = e(371 if case == "after-push" else 369, "decision", "guy", END if case == "early" else LATE if case == "between" else AFTER if case == "after-push" else FIX, kind="fix", subject=subject)
    es += sorted([fix, e(370, "push", "guy", PUSH)], key=lambda e: e["seq"])
    before = [e for e in es if e["seq"] < fix["seq"]]
    row = ROW.replace("2026-11-02 22:11", "2026-11-16 08:00" if case == "outside" else "2026-11-15 23:04") if case in ("outside", "partial-minute") else ROW
    table = HEADER + ("" if case == "raw-only" else row)
    files = {PATH + ".csv": "wrong,header\n" if case == "bad-header" else table, PATH + "-raw.csv": HEADER + ROW,
             PATH + "-classifier.sha256": "wrong" if case == "bad-hash" else hashlib.sha256(b"classifier").hexdigest(), "transcripts/evidence/guy_acts3.py": "classifier"}
    if case == "wrong-classifier":
        files.update({"transcripts/evidence/other.py": "classifier", "transcripts/evidence/guy_acts3.py": "different"})
    if case in ("missing-raw", "missing-classifier"):
        del files[PATH + "-raw.csv" if case == "missing-raw" else "transcripts/evidence/guy_acts3.py"]
    if case == "raw-only":
        fix["body"]["subject"] = "C2a: acts-raw.csv"
        files.update({PATH + "-raw-raw.csv": HEADER + ROW, PATH + "-raw-classifier.sha256": files[PATH + "-classifier.sha256"]})
    with tree(dict({} if case in ("later-file", "veto") else files, **{"log.jsonl": log(before)})) as (root, _):
        carrier = commit(root, {"log.jsonl": log([e for e in es if e["seq"] <= fix["seq"]])})
        es += [e(372, "resolution", ts=PUSH, forecast=6), e(373, "merge", ts=PUSH)]
        head = commit(root, dict(files if case == "later-file" else {PATH + ".csv": HEADER} if case == "replacement" else {}, **{"log.jsonl": log(es)}))
        with patch.object(st, "signer_blob", side_effect=lambda e: e["proposer"]):
            qualified = st.window_fix_seqs(es, root, "unreadable" if case in ("history", "veto-history") else head)
            result = st.item_process(es, 2, window_fixes=qualified)
            repair = st.item_process(es, 2)
        expected = case in ("decision", "stem", "veto", "replacement")
        assert (fix["seq"] in qualified) == expected
        assert (fix["seq"] in result["late_reports"]) != expected
        assert (fix["seq"] in result["items"][-1]["repairs"]) != expected
        assert result["items"][0] == repair["items"][0]
        assert fix["seq"] in repair["late_reports"]
        if case in ("history", "veto-history", "missing-raw", "missing-classifier"):
            assert f"window fix {fix['seq']}: unverified —" in capsys.readouterr().err
        assert st.carrying_commit(root, head, fix) == carrier


def test_second_window():
    es = base() + [e(368, "forecast", ts=END, args={"id": "V5"}, resolves_by=V5), e(369, "push", "guy", PUSH)]
    assert st.prime_window(es) == (369, PUSH, V5)
    assert st.second_opening(base() + [e(368, "push", "guy", END), e(369, "push", "guy", LATE), e(370, "push", "guy", PUSH)])["seq"] == 370
    longer = base() + [e(368, "forecast", ts=END, args={"id": "V5"}, resolves_by="2026-12-30T00:00:00Z"), es[-1]]
    assert st.prime_window(longer)[2] == longer[-2]["body"]["resolves_by"]
    assert st.status(es[:-1], "A3", 14, END, subject="C2a")["window"] == "C2a"
    s = st.status(es, "A3", 14, PUSH, subject="C2a")
    assert (s["window"], s["opening"], s["start"]) == ("C2a-prime", 369, PUSH)
    acts = list(st.csv.DictReader((HEADER + ROW).splitlines()))
    assert st.off_log_repairs(acts, OPEN, END) == 1 and st.off_log_repairs(acts, s["start"], V5) == 0
    for invalid in (es[:9] + es[10:], es[:9] + [es[10], dict(es[9], seq=370)]):
        with pytest.raises(ValueError, match="C2a-prime has no promotion forecast before its opening"):
            st.prime_window(invalid)
    assert st.second_opening(es[:9] + [e(368, "decision", "guy", LATE, kind="promote", subject="C2a")] + es[9:]) is None
    for kind in ("promote", "veto"):
        assert st.decision_window(e(370, "decision", "guy", V5, kind=kind, subject="C2a"), es) == "C2a-prime"
        assert st.decision_window(e(370, "decision", "guy", PUSH, kind=kind, subject="C2a"), es) == "C2a"
    assert st.decision_window(e(370, "decision", "guy", AFTER, kind="veto", subject="C2a-prime"), es) == "C2a-prime"
    assert st.decision_window(e(370, "decision", "guy", PUSH, kind="veto", subject="C2a-prime"), es) is None
    assert st.decision_window(e(370, "decision", "guy", AFTER, kind="promote", subject="C2a-prime"), es) is None
    vetoed = st.status(es + [e(370, "decision", "guy", AFTER, kind="veto", subject="C2a-prime")], "A3", 14, AFTER, subject="C2a")
    assert vetoed["veto"]


def test_assessment_cap_and_first_window_refusal():
    es = base() + [e(368, "forecast", ts=END, args={"id": "V5"}, resolves_by=V5), e(369, "push", "guy", PUSH)]
    acts = list(st.csv.DictReader((HEADER + ROW).splitlines()))
    with patch.object(st, "c2a_tree_evidence", return_value=(True, True, True)), patch.object(st, "signer_blob", side_effect=lambda e: e["proposer"]):
        first = st.status(es, "A3", 14, END, subject="C2a")
        first["checks"] = st.assess_value(first, dict(counted=7800, kernel=500, scope=True), True, st.ROOT, None, [], acts)
        first.update(subject="C2a", repairs=[])
        assert not first["checks"][-1][0] and "window: C2a-prime" not in st.render(first)
        assert "promote C2a: refused:" in st.render(first) and "criterion 7: off-log repairs: 1" in st.promotion_line(first)
        for count, permitted in [(st.C2A_PRIME_CAP, True), (st.C2A_PRIME_CAP + 1, False)]:
            second = st.status(es, "A3", 14, PUSH, subject="C2a")
            checks = st.assess_value(second, dict(counted=count, kernel=500, scope=True), True, st.ROOT, None, [], acts)
            assert checks[2][0] == permitted and checks[-1][0]
        with patch.object(st, "c2a_tree_evidence", return_value=(True, None, True)):
            checks = st.assess_value(second, dict(counted=st.C2A_PRIME_CAP, kernel=500, scope=True), True, st.ROOT, None, [], acts)
            assert not checks[5][0] and "unchanged: pending the window code's merge" in checks[5][1]


def test_process_unchanged_from_window_code():
    es = base() + [e(368, "forecast", ts=END, args={"id": "V5"}, resolves_by=V5), e(369, "push", "guy", PUSH)]
    scope = json.dumps({"cap": st.C2A_PRIME_CAP, "counted": ["tools/"]})
    source = st.tree_bytes(st.ROOT, None, "tools/status.py").decode()
    files = {"judge/scope.json": scope, "SPEC.md": "at C1 it is:\n```\n" + scope + "\n```", "tools/clerk.py": "",
             "pins/pins.py": "\n".join(f'Pin("{p}"' for p in st.VALUE_PINS), "log.jsonl": log(es), "tools/status.py": "def item_process(): pass\n"}
    with tree(files) as (root, opening):
        assert st.c2a_tree_evidence(root, opening, es, 369, True) == (True, None, True)
        code = commit(root, {"tools/status.py": source})
        es.append(e(370, "proposal", ts=PUSH, title="C2a-prime window code: fixture", commit=code))
        es.append(e(371, "proposal", ts=PUSH, title="unrelated later proposal", commit=opening))
        proposal = commit(root, {"log.jsonl": log(es)})
        es.append(e(372, "merge", ts=PUSH, proposal=999, commit=opening))
        unrelated = commit(root, {"log.jsonl": log(es)})
        assert st.c2a_tree_evidence(root, unrelated, es, 369, True)[1] is None
        es.append(e(373, "merge", ts=PUSH, proposal=999, commit=proposal))
        merged = commit(root, {"log.jsonl": log(es)})
        assert st.c2a_tree_evidence(root, merged, es, 369, True) == (True, True, True)
        for before, after in [('r["class"] == "repair"', 'True'), ('end, fixes)', 'end, fixes | {999})'),
                              ('dt.datetime.strptime(s, FMT)', 'dt.datetime.strptime(s, FMT) + dt.timedelta(seconds=1)')]:
            changed = commit(root, {"tools/status.py": source.replace(before, after)})
            assert st.c2a_tree_evidence(root, changed, es, 369, True)[1] is False
        changed = commit(root, {"tools/status.py": source, "judge/scope.json": scope.replace(str(st.C2A_PRIME_CAP), str(st.C2A_PRIME_CAP + 1))})
        assert st.c2a_tree_evidence(root, changed, es, 369, True)[0] is False
        reverted = commit(root, {"judge/scope.json": scope})
        assert st.c2a_tree_evidence(root, reverted, es, 369, True)[0] is False
    files["judge/scope.json"] = scope.replace(str(st.C2A_PRIME_CAP), "7800")
    files["SPEC.md"] = "at C1 it is:\n```\n" + files["judge/scope.json"] + "\n```"
    with tree(files) as (root, _):
        changed = commit(root, {"judge/scope.json": scope, "SPEC.md": "at C1 it is:\n```\n" + scope + "\n```"})
        assert st.c2a_tree_evidence(root, changed, es[:11], 369, True)[0] is False


def test_nonretroactivity():
    es = []
    with open(st.ROOT + "/log.jsonl") as stream:
        for line in stream:
            es.append(json.loads(line))
    with patch.object(st, "git_bytes", side_effect=AssertionError("inertness must read no git history")):
        assert st.item_process(es, st.c1b_window(es)[0], window_fixes=st.window_fix_seqs(es, st.ROOT, "HEAD")) == st.item_process(es, st.c1b_window(es)[0])
