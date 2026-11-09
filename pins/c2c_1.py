"""C2c-1 reviewer pins reuse the builder's complete disposable-tree fixtures."""
import subprocess
import sys
import textwrap


def c2c_tests(*names):
    def test(root):
        result = subprocess.run([sys.executable, "-E", "-s", "-m", "unittest", "-q", *names],
                                cwd=root, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
        _run(root, '''
            import os, tempfile
            from tools import window
            with tempfile.TemporaryDirectory(dir="tools") as d:
                with open(os.path.join(d, "status.py"), "w") as f:
                    f.write('p = "transcripts/windows/C2c-1.json"\\n')
                found = window.scan_tools_window_paths(d)
                assert len(found) == 1 and found[0].endswith("/status.py"), found
            bad = {"numbers": {}, "processes": {}, "criteria": [{"kind": "x", "args": {}}]}
            try:
                window.check_window_file_numbers(bad)
            except ValueError:
                pass
            else:
                raise AssertionError("unknown window criterion kind was accepted")
            source = open("tools/window.py", encoding="utf-8").read()
            assert source.count('rb_dt = st.instant(e["body"]["resolves_by"])') == 2
        ''')
    return test


def courier_tests(*names):
    def test(root):
        result = subprocess.run([sys.executable, "-E", "-s", "-m", "unittest", "-q", *names],
                                cwd=root, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
    return test


def _run(root, source):
    result = subprocess.run([sys.executable, "-E", "-s", "-c", textwrap.dedent(source)],
                            cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def one_stated_end(root):
    """R3 selects the first matching counsel forecast before the opening."""
    _run(root, '''
        from tools import window
        w = {"promotion": {"proposer": "counsel", "type": "window.promotion", "forecast_id": "V0"}}
        def f(seq, proposer, resolves_by, typ="window.promotion", ident="V0"):
            return {"seq": seq, "type": "forecast", "proposer": proposer,
                    "body": {"resolves_by": resolves_by, "type": typ, "args": {"id": ident}}}
        entries = [
            f(1, "counsel", "2026-12-04T00:00:00Z", ident="other"),
            f(2, "reviewer", "2026-12-01T00:00:00Z"),
            f(3, "counsel", "2026-12-05T00:00:00Z", typ="other"),
            f(4, "counsel", "2026-12-03T00:00:00Z"),
            f(5, "counsel", "2026-12-02T00:00:00Z"),
            f(101, "counsel", "2026-12-06T00:00:00Z"),
        ]
        got = window.find_promotion_forecast(entries, 100, w)
        assert got and got["seq"] == 4 and got["body"]["resolves_by"] == "2026-12-03T00:00:00Z", got
        assert window.find_promotion_forecast(entries[5:], 100, w) is None
    ''')


def numerals_housed(root):
    """R1 keeps every window-file read and its numeric table at the assessed tree in window.py."""
    c2c_tests("tests.test_c2c_1.R1NumeralsAndR9Binding.test_r1_numerals_housed_twins_and_mutants")(root)
    _run(root, '''
        from pathlib import Path
        jack = Path("tools/jack").read_text(encoding="utf-8")
        assert "json.loads(wbytes)" not in jack, "tools/jack reads the window file"
    ''')


def one_writ_function(root):
    """R4 lists every unresolved forecast, including one before C1b's opening."""
    _run(root, '''
        from tools import clerk
        keys = [{"key_id": "resolver", "principal": "reviewer", "powers": ["resolution"]}]
        def e(seq, typ, ts, body, proposer="counsel"):
            return {"seq": seq, "type": typ, "ts": ts, "body": body, "proposer": proposer}
        entries = [
            e(0, "genesis", "2026-01-01T00:00:00Z", {"keys": keys}, "guy"),
            e(5, "forecast", "2026-01-01T00:01:00Z", {"resolves_by": "2026-01-02T00:00:00Z"}),
            e(6, "forecast", "2026-01-01T00:02:00Z", {"resolves_by": "2026-01-03T00:00:00Z", "type": "counsel.undertaking"}),
            e(7, "forecast", "2026-01-01T00:03:00Z", {"resolves_by": "2026-01-02T00:00:00Z"}),
            e(8, "resolution", "2026-01-01T00:04:00Z", {"forecast": 7}, "reviewer"),
        ]
        writs = clerk.forecast_writs(entries, [], "2026-01-02T12:00:00Z")
        by_seq = {w["seq"]: w for w in writs}
        assert set(by_seq) == {5, 6}, by_seq
        assert by_seq[5]["escalated"] is True
        assert by_seq[6]["escalated"] is False
    ''')
    _run(root, '''
        from tools import status
        entries = [
            {"seq": 0, "type": "genesis", "ts": "2026-01-01T00:00:00Z",
             "body": {"keys": [{"key_id": "resolver", "principal": "reviewer", "powers": ["resolution"]}]},
             "proposer": "guy"},
            {"seq": 5, "type": "forecast", "ts": "2026-01-01T00:01:00Z",
             "body": {"resolves_by": "2026-01-02T00:00:00Z"}, "proposer": "counsel"},
        ]
        rendered = status.render({"subject": "C2a", "start": "2026-01-01T00:00:00Z",
                                  "end": "2026-01-03T00:00:00Z", "as_of": "2026-01-02T12:00:00Z",
                                  "prefix_last_seq": 5, "checks": [], "map": {}, "overdue": [],
                                  "j7_unresolved_past_due": 0, "j7_denominator": 0,
                                  "es": entries, "repairs": []})
        assert "W1 forecast 5" in rendered, rendered
    ''')
    c2c_tests("tests.test_c2c_1.R2R4R8CriteriaAndWrits.test_r4_one_writ_function_and_r8_object_declared")(root)
    c2c_tests("tests.test_promotion.Promotion.test_w3_only_earlier_green_exact_workflow_and_commit_discharge",
              "tests.test_promotion.Promotion.test_historical_bad_promote_stays_repair_after_later_success")(root)


def undertakings_are_forecasts(root):
    """R5 requires inventory rows to be matched by a forecast already present at opening."""
    c2c_tests("tests.test_c2c_1.R5R6R7R10R11Criteria.test_r5_undertakings_are_forecasts_twins")(root)
    _run(root, '''
        from tools import window
        due = b'{"id":"u1","due":"2026-01-03T00:00:00Z","done":null}' + bytes([10])
        old_bytes, old_retired = window.tree_bytes_opt, window.retired_by_proposal
        try:
            window.tree_bytes_opt = lambda root, rev, path: due if rev == "open" else None
            window.retired_by_proposal = lambda *args: True
            post_opening = {"seq": 2, "type": "forecast", "proposer": "counsel", "ts": "2026-01-02T00:00:00Z",
                            "body": {"type": "counsel.undertaking", "resolves_by": "2026-01-03T00:00:00Z",
                                     "args": {"id": "u1", "window": "C2c-1"}}}
            ctx = {"root": ".", "rev": "head", "opening_rev": "open", "opening": 1, "wfile": {"numbers": {}},
                   "prefix": [post_opening], "inw": [post_opening], "as_of": "2026-01-02T12:00:00Z",
                   "start": "2026-01-01T00:00:00Z", "end": "2026-01-04T00:00:00Z", "run": None,
                   "runs": [], "subject": "C2c-1", "expired_undertakings": set()}
            criterion = {"kind": "undertakings_kept", "args": {"due_file": "transcripts/COUNSEL-DUE.jsonl",
                         "proposer": "counsel", "type": "counsel.undertaking"}}
            assert window.evaluate_criterion(criterion, ctx) == "unmet"
            base = {"root": ".", "rev": "head", "opening_rev": "open", "opening": 2, "wfile": {"numbers": {}},
                    "inw": [], "as_of": "2026-01-05T00:00:00Z", "start": "2026-01-01T00:00:00Z",
                    "end": "2026-01-06T00:00:00Z", "run": None, "runs": [], "subject": "C2c-1",
                    "expired_undertakings": set()}
            def forecast(seq, resolves_by, window="C2c-1"):
                return {"seq": seq, "type": "forecast", "proposer": "counsel", "ts": "2026-01-01T00:00:00Z",
                        "body": {"type": "counsel.undertaking", "resolves_by": resolves_by,
                                 "args": {"id": "u1", "window": window}}}
            late = forecast(1, "2026-01-02T00:00:00Z")
            late_resolution = {"seq": 2, "type": "resolution", "proposer": "reviewer", "ts": "2026-01-03T00:00:00Z",
                               "body": {"forecast": 1, "outcome": 1}}
            assert window.evaluate_criterion(criterion, dict(base, prefix=[late, late_resolution])) == "unmet"
            assert window.evaluate_criterion(criterion, dict(base, prefix=[forecast(1, "2026-01-02T00:00:00Z")])) == "unmet"
            window.tree_bytes_opt = lambda root, rev, path: due if rev == "open" else None
            wrong_window = forecast(1, "2026-01-02T00:00:00Z", "C2b")
            timely_resolution = {"seq": 2, "type": "resolution", "proposer": "reviewer", "ts": "2026-01-01T12:00:00Z",
                                 "body": {"forecast": 1, "outcome": 1}}
            assert window.evaluate_criterion(criterion, dict(base, prefix=[wrong_window, timely_resolution])) == "unmet"
        finally:
            window.tree_bytes_opt, window.retired_by_proposal = old_bytes, old_retired
    ''')
