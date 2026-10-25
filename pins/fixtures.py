"""Judge fixtures founded against their actual trusted-base content."""
from harness import build, gitfix
from judge import judge


def bind_genesis(repo, lg, world):
    entry = build.log.parse_line(lg.lines[0])
    body = dict(entry["body"], checker=judge.digest(repo, "HEAD"))
    lg.lines[0] = build.make_entry(0, build.log.GENESIS_PARENT, "genesis", "guy", body, world.guy)
    gitfix.write(repo, "log.jsonl", lg.text())
    return gitfix.commit_all(repo, "Found against the trusted base")


def propose(repo, lg, world, party="builder", msg="change", key=None):
    """Commit the working tree as the proposal's work, then a `proposal` entry naming that commit, signed by
    `party`'s genesis key (or `key`), in a commit touching log.jsonl only (SPEC §10.7). Returns the work's sha."""
    work = gitfix.commit_all(repo, msg)
    lg.add("proposal", party, build.proposal(msg, commit=work), key or world.parties[party])
    gitfix.write(repo, "log.jsonl", lg.text())
    gitfix.commit_all(repo, "Record the proposal")
    return work


def make_repo(world, with_log=True, **kwargs):
    fx = gitfix.make_repo(world, with_log=with_log, **kwargs)
    gitfix.git(fx.repo, "checkout", "-q", "main")
    main = bind_genesis(fx.repo, fx.log, world) if with_log else fx.main
    gitfix.git(fx.repo, "checkout", "-q", "pr")
    gitfix.git(fx.repo, "reset", "-q", "--hard", "main")
    return gitfix.Fixture(fx.repo, fx.log, main)


# --- the ledger (C1a): the reviewer's signed logs, spec/vectors/logs/40-49 and the pins' twins ---------------------

def at(minute, second=0):
    return f"2026-10-26T09:{minute:02}:{second:02}Z"


def signer(w, who):
    """ann holds two keys (ann-1, ann-2) of one principal; bob is a second party; guy the master key."""
    return {"guy": ("guy", w.guy), "ann": ("ann", w.ann), "ann-2": ("ann", w.parties["counsel"]), "bob": ("bob", w.stranger)}[who]


def ledger(w):
    lg = build.Log()
    lg.add("genesis", "guy", build.genesis_body([build.decl("guy-master", "guy", w.guy, build.ALL)] + [
        build.decl(k, p, key, ["forecast", "resolution"]) for k, p, key in
        (("ann-1", "ann", w.ann), ("ann-2", "ann", w.parties["counsel"]), ("bob-1", "bob", w.stranger))]), w.guy, ts=at(0))
    return lg


def fc(lg, w, who="ann", ts=None, **body):
    proposer, key = signer(w, who)
    n = len(lg.lines)
    lg.add("forecast", proposer, dict({"claim": f"claim {n}", "p": 600, "resolves_by": "2026-11-09T09:00:00Z"}, **body), key,
           ts=ts or at(n))
    return lg


def rs(lg, w, f, who="bob", ts=None, **body):
    proposer, key = signer(w, who)
    lg.add("resolution", proposer, dict({"forecast": f, "outcome": 1, "evidence": f"run {f}"}, **body), key,
           ts=ts or at(len(lg.lines)))
    return lg


def tampered(lg, **body):
    """The last line with its body edited after signing."""
    e = build.log.parse_line(lg.lines[-1])
    e["body"].update(body)
    lg.lines[-1] = build.log.canonical(e)
    return lg


def ledger_cases(w):
    """name → (lines, expected): (seq, reason), or the entry count admitted. Names with a number are spec/vectors/logs."""
    one = lambda: fc(ledger(w), w)  # noqa: E731  genesis and ann's open forecast at seq 1
    c = {
        "40_forecast_valid": (fc(fc(fc(ledger(w), w, p=1, resolves_by=at(1)), w, "bob", p=999, type="world.screen",
                                    args={"screen": 3, "a.b": [None]}), w, "guy", p=500, type=7, note="x"), 4),
        "41_resolution_valid": (rs(rs(fc(fc(ledger(w), w), w, "bob"), w, 1, outcome=0), w, 2, "guy"), 5),
        "42_resolution_self_bad": (rs(one(), w, 1, "ann-2"), (2, "self_judged")),
        "43_resolution_dangling_bad": (rs(one(), w, 0), (2, "schema")),
        "44_resolution_double_bad": (rs(rs(one(), w, 1), w, 1, "guy", outcome=0), (3, "schema")),
        "45_forecast_past_bad": (fc(ledger(w), w, resolves_by=at(0, 59), ts=at(1)), (1, "schema")),
        "46a_forecast_permille_0_bad": (fc(ledger(w), w, p=0), (1, "schema")),
        "46b_forecast_permille_1000_bad": (fc(ledger(w), w, p=1000), (1, "schema")),
        "47_forecast_boolean_bad": (fc(ledger(w), w, p=True), (1, "schema")),
        "48_ts_decreased_bad": (fc(fc(ledger(w), w, ts=at(5)), w, "bob", ts=at(4, 59)), (2, "ts_decreased")),
        "49_self_resolution_bad_signature": (tampered(rs(one(), w, 1, "ann"), evidence="run 2"), (2, "bad_signature")),
        "ts_equal": (fc(fc(ledger(w), w, ts=at(5)), w, "bob", ts=at(5)), 3),
        "ts_back_and_bad_seq": (build.Log(one().lines + [build.make_entry(9, build.log.line_hash(one().lines[1]), "forecast", "bob",
                                {"claim": "c", "p": 5, "resolves_by": at(9)}, w.stranger, ts=at(0, 30))]), (2, "ts_decreased")),
        "self_same_key": (rs(one(), w, 1, "ann"), (2, "self_judged")),
        "other_party": (rs(one(), w, 1, "bob"), 3),
        "self_of_resolved": (rs(rs(one(), w, 1), w, 1, "ann"), (3, "schema")),
        "second_open_forecast": (rs(rs(fc(one(), w, "bob"), w, 1), w, 2, "ann"), 5),
        "past_by_400_days": (fc(ledger(w), w, resolves_by="2025-09-21T09:01:00Z"), (1, "schema")),
        "resolves_by_equal_ts": (fc(ledger(w), w, resolves_by=at(1)), 2),
        "p_1": (fc(ledger(w), w, p=1), 2),
        "p_999": (fc(ledger(w), w, p=999), 2),
        "p_false": (fc(ledger(w), w, p=False), (1, "schema")),
        "outcome_true": (rs(one(), w, 1, outcome=True), (2, "schema")),
        "outcome_false": (rs(one(), w, 1, outcome=False), (2, "schema")),
        "forecast_true": (rs(one(), w, 1, forecast=True), (2, "schema")),
        "outcome_0": (rs(one(), w, 1, outcome=0), 3),
    }
    for target in (2, 3, 2**53 - 1):  # its own seq, a later one, the largest; then a resolution's seq
        c[f"dangling_{target}"] = (rs(one(), w, target), (2, "schema"))
    c["dangling_resolution_seq"] = (rs(rs(one(), w, 1), w, 2, "guy"), (3, "schema"))
    return c


WITNESS_FORECASTS = [("counsel", "world.screen", 600), ("builder", "pins_green", 800), ("counsel", "world.screen", 300),
                     ("reviewer", "pins_green", 700), ("builder", "world.delivery", 900), ("counsel", "pins_green", 500),
                     ("builder", "pins_green", 650), ("counsel", "world.screen", 400), ("guy", "world.race", 200),
                     ("reviewer", "world.screen", 550)]  # BRIEF-C1.md, F1..F10 at seqs 1..10
WITNESS_RESOLUTIONS = [(2, 1, "counsel"), (1, 1, "reviewer"), (4, 0, "guy"), (3, 0, "builder"), (6, 1, "reviewer"), (5, 0, "guy")]


def witness(w):
    """The score witness, rebuilt by the reviewer from the brief's text alone: F → (forecast seq, outcome), each resolver
    a party other than the forecaster (the resolvers, claims, instants and evidence are the brief's free choices)."""
    key = dict(w.parties, guy=w.guy)
    lg = build.Log()
    lg.add("genesis", "guy", build.genesis_body([build.decl("guy-master", "guy", w.guy, build.ALL)] + [
        build.decl(f"{p}-1", p, w.parties[p], ["proposal", "forecast", "resolution"]) for p in ("builder", "reviewer", "counsel")]),
        w.guy, ts="2026-10-26T08:00:00Z")
    for i, (who, type_, p) in enumerate(WITNESS_FORECASTS, 1):
        lg.add("forecast", who, {"claim": f"F{i}: a {type_} claim at {p} per mille", "p": p, "resolves_by": "2026-11-09T08:00:00Z",
                                 "type": type_}, key[who], ts=f"2026-10-26T08:{i:02}:00Z")
    for j, (f, o, who) in enumerate(WITNESS_RESOLUTIONS, 1):
        lg.add("resolution", who, {"forecast": f, "outcome": o, "evidence": f"F{f} resolved {o} (witness)"}, key[who],
               ts=f"2026-10-27T08:{j:02}:00Z")
    return lg


def write_vectors(root):
    """python3 -m pins.fixtures: rewrite the reviewer's vectors from fresh throwaway keys, each checked against its required verdict."""
    import json, os, tempfile  # noqa: E401
    from kernel import check
    vec = os.path.join(root, "spec", "vectors")
    with open(os.path.join(vec, "verdicts.json")) as f:
        doc = json.load(f)
    with tempfile.TemporaryDirectory() as tmp:
        w = build.World(tmp)
        for name, (lg, want) in ((n, c) for n, c in ledger_cases(w).items() if n[0].isdigit()):
            want = {"ok": True, "entries": want} if isinstance(want, int) else {"ok": False, "seq": want[0], "reason": want[1]}
            got = {k: v for k, v in check.check(lg.lines).items() if k != "detail"}
            assert got == want, (name, got, want)
            with open(os.path.join(vec, "logs", name + ".jsonl"), "w") as f:
                f.write(lg.text())
            doc["verdicts"][name + ".jsonl"] = want
        with open(os.path.join(vec, "score.jsonl"), "w") as f:
            f.write(witness(w).text())
    with open(os.path.join(vec, "verdicts.json"), "w") as f:
        json.dump(doc, f, indent=1)


if __name__ == "__main__":
    import os
    write_vectors(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
