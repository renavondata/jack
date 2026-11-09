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
    c2c_tests("tests.test_c2c_1.R2R4R8CriteriaAndWrits.test_r4_one_writ_function_and_r8_object_declared")(root)
