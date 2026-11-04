"""BRIEF-C2a-prime v7: boundary witnesses, disposable history, and inert-prefix oracle."""
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


@pytest.mark.parametrize("case", ["decision", "stem", "free", "unnamed", "later-file", "raw-only", "raw-both", "outside", "partial-minute",
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
    if case in ("raw-only", "raw-both"):
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


def test_window_fix_not_retroactive():
    es = base() + [e(368, "forecast", ts=END, resolves_by=V5)]
    es.insert(8, e(361, "resolution", ts=OPEN, forecast=360))  # V0 leaves the open set before the boundary.
    files = {"log.jsonl": log(es), PATH + ".csv": HEADER + ROW, PATH + "-raw.csv": HEADER + ROW,
             PATH + "-classifier.sha256": hashlib.sha256(b"classifier").hexdigest(), "transcripts/evidence/guy_acts3.py": "classifier"}
    with tree(files) as (root, _), patch.object(st, "signer_blob", side_effect=lambda e: e["proposer"]):
        es.append(e(369, "decision", "guy", FIX, kind="fix", subject="C2a: acts"))
        commit(root, {"log.jsonl": log(es)})
        es += [e(370, "resolution", ts=FIX, forecast=6), e(371, "merge", ts=FIX), e(372, "push", "guy", PUSH),
               e(373, "resolution", ts=AFTER, forecast=368), e(374, "merge", ts=AFTER)]
        head = commit(root, {"log.jsonl": log(es)})
        for stop in range(12, len(es) + 1):
            prefix = es[:stop]
            fixes = st.window_fix_seqs(prefix, root, head)
            assert fixes == {369}
            result = st.item_process(prefix, 2, window_fixes=fixes)
            old = st.item_process(prefix, 2)
            assert result["items"][:2] == old["items"][:2]  # Y, repairs, stake and wealth before push
            assert result["late_reports"] == [] and old["late_reports"] == [369]
        assert [i["Y"] for i in result["items"]] == [1, 0, 1]
        assert [i["repairs"] for i in result["items"]] == [(), (369,), ()]
        assert old["items"][-1]["repairs"] == (369,) and old["items"][-1]["Y"] == 0
        assert [i["stake"] for i in result["items"]] == [0, st.Fraction(22, 45), 0]
        assert result["E"] == st.Fraction(11, 15)


@pytest.mark.parametrize("subject, expected", [("(acts-20261103)", True), ("acts-20261103.csv", True),
    ("acts-20261103-raw", False), ("acts-20261103-raw.csv", False), ("acts-20261103T2144.csv", False),
    ("xacts-20261103", False), ("1acts-20261103", False), ("_acts-20261103", False), ("-acts-20261103", False),
    ("acts-20261103_x", False), ("éacts-20261103", False), ("acts-20261103é", False)])
def test_file_name_boundaries(subject, expected):
    stem = PATH + "-20261103"
    with tree({stem + ".csv": HEADER + ROW, stem + "-raw.csv": HEADER + ROW,
               stem + "-classifier.sha256": hashlib.sha256(b"classifier").hexdigest(), "transcripts/evidence/guy_acts3.py": "classifier"}) as (root, head):
        if expected:
            assert st.attributed_failure(root, head, subject, OPEN, END)
        else:
            with pytest.raises(ValueError, match="named attributed acts file missing"):
                st.attributed_failure(root, head, subject, OPEN, END)


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
    for subject in ("C2a", "C2a-prime"):
        for when in (END, PUSH, AFTER):
            veto = e(370, "decision", "guy", when, kind="veto", subject=subject)
            assert st.status(es + [veto], "A3", 14, AFTER, subject="C2a")["veto"] == (when == AFTER)


@pytest.mark.parametrize("case", ["veto", "late-veto", "late-promote", "between", "acts", "late-acts", "short"])
def test_c2b_stated_ends(case):
    es = base() + [e(368, "forecast", ts=OPEN, args={"id": "X7"}, resolves_by=END if case == "short" else LATE),
                   e(369, "decision", "guy", OPEN, kind="promote", subject="C2a"), e(370, "push", "guy", OPEN)]
    assert st.fix_window(es, "C2b") == (370, OPEN, END)
    assert st.fix_window(es, "C2b", late=True)[2] == (END if case == "short" else LATE)
    es.append(e(371, "decision", "guy", LATE if case == "late-veto" else END, kind="veto", subject="C2b"))
    if case == "late-promote":
        es.append(e(372, "decision", "guy", LATE, kind="promote", subject="C2b"))
    if case.endswith("acts"):
        es.pop()
    fix = e(373, "decision", "guy", END if case == "between" else FIX, kind="fix", subject="C2b: " + ("acts" if case.endswith("acts") else "no file"))
    row = ROW.replace("2026-11-02 22:11", "2026-11-16 08:00") if case == "late-acts" else ROW
    files = {"log.jsonl": log(es), PATH + ".csv": HEADER + row, PATH + "-raw.csv": HEADER + row,
             PATH + "-classifier.sha256": hashlib.sha256(b"classifier").hexdigest(), "transcripts/evidence/guy_acts3.py": "classifier"}
    with tree(files) as (root, _), patch.object(st, "signer_blob", side_effect=lambda e: e["proposer"]):
        es.append(fix)
        head = commit(root, {"log.jsonl": log(es)})
        assert st.window_fix_seqs(es, root, head) == ({373} if case in ("veto", "acts", "short") else set())
    for name in ("C1a", "C1b", "C2b", "later-window"):
        for kind in ("promote", "veto"):
            assert st.decision_window(e(374, "decision", "guy", AFTER, kind=kind, subject=name), es) == name


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
        es[-1]["ts"] = "2026-11-18T00:00:30Z"
        second = st.status(es, "A3", 14, "2026-11-18T00:05:00Z", subject="C2a")
        boundary = [dict(repo="renavondata/jack", **{"class": "repair", "time_hkt": "2026-11-18 08:00"})]
        checks = st.assess_value(second, dict(counted=st.C2A_PRIME_CAP, kernel=500, scope=True), True, st.ROOT, None, [], boundary)
        assert not checks[-1][0] and checks[-1][1] == "criterion 7: off-log repairs: 1"
        assert st.off_log_repairs(boundary, second["start"], second["as_of"]) == 0  # first-window rule unchanged
        assert st.off_log_repairs(boundary, second["start"], second["start"], minute_overlap=True) == 0
        for minute, expected in [("07:59", 0), ("08:00", 1), ("08:05", 1), ("08:06", 0)]:
            boundary[0]["time_hkt"] = "2026-11-18 " + minute
            assert st.off_log_repairs(boundary, second["start"], second["as_of"], minute_overlap=True) == expected
        boundary[0]["time_hkt"] = "2026-11-18 07:59"
        assert st.off_log_repairs(boundary, "2026-11-18T00:00:00Z", second["as_of"], minute_overlap=True) == 0


def test_process_unchanged_from_opening():
    es = base() + [e(368, "forecast", ts=END, args={"id": "V5"}, resolves_by=V5), e(369, "push", "guy", PUSH)]
    scope = json.dumps({"cap": st.C2A_PRIME_CAP, "counted": ["tools/"]})
    source = st.tree_bytes(st.ROOT, None, "tools/status.py").decode()
    source += "\nFIX_TOGGLE = 0\ndef fix_caller(es, root, rev):\n    qualified = window_fix_seqs(es, root, rev)\n    return qualified if FIX_TOGGLE == 0 else set()\n"
    files = {"judge/scope.json": scope, "SPEC.md": "at C1 it is:\n```\n" + scope + "\n```", "tools/clerk.py": "",
             "pins/pins.py": "\n".join(f'Pin("{p}"' for p in st.VALUE_PINS), "log.jsonl": log(es),
              "tools/status.py": source}
    with tree(files) as (root, opening):
        assert st.c2a_tree_evidence(root, opening, es, 369, True) == (True, True, True)
        for before, after in [('r["class"] == "repair"', 'True'), ('end, fixes)', 'end, fixes | {999})'),
                              ('fixes = window_fix_seqs(s["prefix"], root, rev)', 'fixes = window_fix_seqs(s["prefix"], root, rev) | {999}'),
                              ('return qualified if', 'return qualified | {999} if'),
                              ('dt.datetime.strptime(s, FMT)', 'dt.datetime.strptime(s, FMT) + dt.timedelta(seconds=1)'),
                              ('capture_output=True', 'capture_output=False'),
                              ('"attributed_failure", "window_fix_seqs")', '"window_fix_seqs",)'),
                              ('FIX_TOGGLE = 0', 'FIX_TOGGLE = 1'), ('C2A_PRIME_CAP = 8400', 'C2A_PRIME_CAP = 8401'),
                              ('FMT = "%Y-%m-%dT%H:%M:%SZ"', 'FMT = "%Y-%m-%dT%H:%M:%S%z"')]:
            assert before in source
            changed = commit(root, {"tools/status.py": source.replace(before, after)})
            assert st.c2a_tree_evidence(root, changed, es, 369, True)[1] is False
        for node in st.ast.parse(source).body:
            if isinstance(node, st.ast.FunctionDef) and node.name in st.WINDOW_FIX_FUNCTIONS + ("item_process",):
                lines = source.splitlines(keepends=True)
                lines.insert(node.lineno, "    pass\n")
                changed = commit(root, {"tools/status.py": "".join(lines)})
                assert st.c2a_tree_evidence(root, changed, es, 369, True)[1] is False
        for before, after in [('Fraction(6, 11)', 'Fraction(1, 2)'), ('successes += item["Y"]', 'successes += 1'),
                              ('d["pubkey"].split()[1]', 'd["pubkey"].split()[0]'), ('"tools/clerk.py"', 'clerk changed')]:
            edits = {"tools/status.py": source.replace(before, after), "tools/clerk.py": ""}
            if before == '"tools/clerk.py"':
                edits = {"tools/status.py": source, "tools/clerk.py": after}
            changed = commit(root, edits)
            assert st.c2a_tree_evidence(root, changed, es, 369, True)[1] is False
        restored = commit(root, {"tools/status.py": source, "tools/clerk.py": ""})
        assert st.c2a_tree_evidence(root, restored, es, 369, True)[1] is True
        missing = commit(root, {"pins/pins.py": ""})
        assert st.c2a_tree_evidence(root, missing, es, 369, True)[2] is False
        changed = commit(root, {"judge/scope.json": scope.replace(str(st.C2A_PRIME_CAP), str(st.C2A_PRIME_CAP + 1))})
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
            entry = json.loads(line)
            if entry["type"] == "decision" and entry["body"].get("kind") == "fix":
                break
            es.append(entry)
    with patch.object(st, "git_bytes", side_effect=AssertionError("inertness must read no git history")):
        assert st.item_process(es, st.c1b_window(es)[0], window_fixes=st.window_fix_seqs(es, st.ROOT, "HEAD")) == st.item_process(es, st.c1b_window(es)[0])
