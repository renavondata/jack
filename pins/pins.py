"""The pins (CHARTER §9): attack fixture, named mutant(s), passing twin. Data, run by pins/run.py.

Each test takes the root of the tree under test and runs that tree's checker or
judge as a subprocess, so the same fixtures run unchanged against the second
checker. Expectations are exact (seq, rule, reason) or exact lapse lists, so a
mutant cannot survive by failing for a different reason.
"""
import functools
import os
import sys
import tempfile
from collections import namedtuple

from harness import build, diff, gitfix, keys, runner
from harness.build import forbid_title, proposal, rule_body, witness
from kernel import log, sig

Pin = namedtuple("Pin", "name test mutants")
Mutant = namedtuple("Mutant", "name path find replace")
L = sig.L


@functools.lru_cache(None)
def world():
    return build.World(tempfile.mkdtemp(prefix="pins-"))


def W(title):
    return witness("proposal", "p", proposal(title))


def R(rid, forbid, viol, sat, **kw):
    return rule_body(rid, forbid_title(rid, *forbid), [W(t) for t in viol], [W(t) for t in sat], **kw)


def refused(v, seq, reason, rule=None):
    got = (v.get("ok"), v.get("seq"), v.get("rule"), v.get("reason"))
    assert got == (False, seq, rule, reason), f"expected {(seq, rule, reason)}, got {v}"


def admitted(v, entries, lapse=()):
    assert v == {"ok": True, "entries": entries, "lapse": [list(x) for x in lapse]}, v


def rules_log(*bodies):
    lg = world().log()
    for b in bodies:
        lg.add("rule", "guy", b, world().guy)
    return lg


# --- judge pins -------------------------------------------------------------

def t_trusted_path(root):
    w = world()
    for path in ("kernel/check.py", "judge/judge.py"):
        fx = gitfix.make_repo(w)
        gitfix.write(fx.repo, path, 'print(\'{"ok": true, "entries": 0, "lapse": []}\')\n')
        gitfix.commit_all(fx.repo, "edit trusted file")
        r = runner.judge_with(root, fx.repo, "main", "pr")
        assert (r.get("ok"), r.get("reason")) == (False, "trusted_path"), (path, r)
    fx = gitfix.make_repo(w)
    gitfix.write(fx.repo, "README.md", "docs only\n")
    gitfix.commit_all(fx.repo, "docs")
    r = runner.judge_with(root, fx.repo, "main", "pr")
    assert r.get("ok") is True, r


def t_judge_from_proposal(root):
    from judge import judge as trunk_judge  # pristine, only to compute the fixture trunk's digest
    w = world()
    fx = gitfix.make_repo(w)
    fx.log.add("proposal", "ann", proposal("a"), w.ann)
    fx.log.add("merge", "guy", build.merge(1, "ab" * 32), w.guy)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    gitfix.commit_all(fx.repo, "merge judged by a checker the proposal supplied")
    r = runner.judge_with(root, fx.repo, "main", "pr")
    assert (r.get("ok"), r.get("reason")) == (False, "judge_from_proposal"), r
    fx.log.lines.pop()
    fx.log.add("merge", "guy", build.merge(1, trunk_judge.digest(fx.repo, fx.main)), w.guy)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    gitfix.commit_all(fx.repo, "merge judged by trunk")
    assert runner.judge_with(root, fx.repo, "main", "pr").get("ok") is True
    fx = gitfix.make_repo(w)
    fx.log.add("proposal", "ann", proposal("b"), w.ann)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    gitfix.commit_all(fx.repo, "proposal")
    assert runner.judge_with(root, fx.repo, "main", "pr").get("ok") is True


# --- kernel pins ------------------------------------------------------------

def t_final_law_for_all(root):
    w = world()
    lg = w.log()
    lg.add("proposal", "ann", proposal("forbidden"), w.ann)
    clauses = forbid_title("r1", "forbidden") + [{"head": ["violation", "?S", "r1"], "body": [["entry", "?S", "rule", "?_"]]}]
    lg.add("rule", "guy", rule_body("r1", clauses, [W("forbidden")], [W("fine")]), w.guy)
    lg.add("proposal", "ann", proposal("fine"), w.ann)
    admitted(runner.check_with(root, lg.lines), 4)
    lg.add("proposal", "ann", proposal("forbidden"), w.ann)
    refused(runner.check_with(root, lg.lines), 4, "violation", "r1")


def t_vacuous(root):
    refused(runner.check_with(root, rules_log(R("r0", ["x"], ["x"], ["y"]), R("r1", ["w"], ["x"], ["y"])).lines), 2, "vacuous_rule")
    refused(runner.check_with(root, rules_log(R("r1", ["w"], ["x"], ["y"])).lines), 1, "vacuous_rule")
    admitted(runner.check_with(root, rules_log(R("r0", ["x"], ["x"], ["y"]), R("r1", ["w"], ["w"], ["y"])).lines), 3)


def t_impossible(root):
    refused(runner.check_with(root, rules_log(R("r1", ["x"], ["x"], ["x"])).lines), 1, "impossible_rule")
    refused(runner.check_with(root, rules_log(R("r0", ["y"], ["y"], ["w"]), R("r1", ["x"], ["x"], ["y"])).lines), 2, "impossible_rule")
    admitted(runner.check_with(root, rules_log(R("r0", ["y"], ["y"], ["w"]), R("r1", ["x"], ["x"], ["w"])).lines), 3)


def t_unsigned_change(root):
    w = world()
    lg = w.log(); lg.add("rule", "ann", R("r1", ["x"], ["x"], ["y"]), w.ann)
    refused(runner.check_with(root, lg.lines), 1, "no_power")
    lg = w.log(); lg.add("repeal", "ann", {"rule_id": "r1"}, w.ann)
    refused(runner.check_with(root, lg.lines), 1, "no_power")
    lg = w.log(); lg.add("rule", "guy", R("r1", ["x"], ["x"], ["y"]), w.guy); lg.add("repeal", "guy", {"rule_id": "r1"}, w.guy)
    admitted(runner.check_with(root, lg.lines), 3)


def t_history_rewritten(root):
    w = world()
    lg = w.log()
    lg.add("proposal", "ann", proposal("a"), w.ann)
    lg.add("proposal", "ann", proposal("b"), w.ann)
    admitted(runner.check_with(root, lg.lines), 3)
    e = log.parse_line(lg.lines[1]); e["body"]["title"] = "evil"
    refused(runner.check_with(root, [lg.lines[0], log.canonical(e), lg.lines[2]]), 1, "bad_signature")
    resigned = build.make_entry(1, log.line_hash(lg.lines[0]), "proposal", "ann", e["body"], w.ann)
    refused(runner.check_with(root, [lg.lines[0], resigned, lg.lines[2]]), 2, "parent_mismatch")


def t_fork(root):
    w = world()
    lg = w.log()
    lg.add("proposal", "ann", proposal("a"), w.ann)
    h1 = lg.head
    lg.add("proposal", "ann", proposal("b"), w.ann)
    admitted(runner.check_with(root, lg.lines), 3)
    fork = build.make_entry(3, h1, "proposal", "ann", proposal("c"), w.ann)
    refused(runner.check_with(root, lg.lines + [fork]), 3, "parent_mismatch")


def t_redundancy(root):
    admitted(runner.check_with(root, rules_log(R("r1", ["x"], ["x"], ["y"]), R("r2", ["x", "z"], ["z"], ["y"])).lines), 3, [[2, "r1"]])
    admitted(runner.check_with(root, rules_log(R("r1", ["x"], ["x"], ["y"]), R("r3", ["w"], ["w"], ["y"])).lines), 3, [])


def t_unattributed(root):
    w = world()
    lg = w.log(); lg.add("proposal", "", proposal(), w.ann)
    refused(runner.check_with(root, lg.lines), 1, "no_proposer")
    lg = w.log(); lg.add("proposal", "guy", proposal(), w.stranger)
    refused(runner.check_with(root, lg.lines), 1, "unknown_key")
    lg = w.log(); lg.add("proposal", "guy", proposal(), w.ann)
    refused(runner.check_with(root, lg.lines), 1, "proposer_mismatch")
    lg = w.log(); lg.add("proposal", "ann", proposal(), w.ann)
    admitted(runner.check_with(root, lg.lines), 2)


def t_forged_signature(root):
    w = world()
    lg = w.log()
    lg.add("proposal", "ann", proposal("a"), w.ann)
    admitted(runner.check_with(root, lg.lines), 2)
    e = log.parse_line(lg.lines[1])
    _, sig64 = sig.parse_sshsig(e["sig"])
    s = int.from_bytes(sig64[32:], "little")
    e["sig"] = keys.rewrap(e["sig"], sig64=sig64[:32] + (s + L).to_bytes(32, "little"))
    refused(runner.check_with(root, [lg.lines[0], log.canonical(e)]), 1, "bad_signature")


def t_orphaned_rule(root):
    refused(runner.check_with(root, rules_log(R("r1", ["x"], ["x"], ["y"]), R("r2", ["y"], ["y"], ["z"])).lines), 2, "orphans_rule")
    twin = rules_log(R("r1", ["x"], ["x"], ["y"]), R("r2", ["y"], ["y"], ["z"], replacements={"r1": [W("z")]}))
    admitted(runner.check_with(root, twin.lines), 3)


def t_checker_drift(root):
    """Both checkers agree, verdict by verdict, on the pin fixtures (runs once kernel2/check exists)."""
    w = world()
    logs = [w.log().lines, rules_log(R("r1", ["x"], ["x"], ["y"])).lines]
    lg = w.log(); lg.add("proposal", "guy", proposal(), w.stranger); logs.append(lg.lines)
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for i, lines in enumerate(logs):
            paths.append(os.path.join(tmp, f"{i}.jsonl"))
            with open(paths[-1], "w") as f:
                f.write("".join(l + "\n" for l in lines))
        bad = diff.compare([sys.executable, "-E", "-s", "-m", "kernel.check"], [os.path.join(root, "kernel2", "check")], paths)
    assert not bad, bad


PINS = [
    Pin("trusted_path_unguarded", t_trusted_path, [
        Mutant("guard_removed", "judge/judge.py",
               '    if guarded:\n        return refuse("trusted_path"', '    if False:\n        return refuse("trusted_path"'),
        Mutant("judge_dir_untrusted", "judge/judge.py",
               'TRUSTED = ("kernel/", "judge/", ".github/workflows/", "SPEC.md")',
               'TRUSTED = ("kernel/", ".github/workflows/", "SPEC.md")')]),
    Pin("judge_from_proposal", t_judge_from_proposal, [
        Mutant("digest_unchecked", "judge/judge.py",
               'if e["type"] == "merge" and e["body"]["checker"] != report["trusted_digest"]:',
               'if e["type"] == "merge" and False:')]),
    Pin("final_law_for_all", t_final_law_for_all, [
        Mutant("latest_law_reaches_back", "kernel/check.py",
               'hits = {r for s, r in violations(in_force(state), law_facts(state, own, i)) if s == i}',
               'hits = {r for s, r in violations(in_force(state), law_facts(state, own, i)) if True}')]),
    Pin("vacuous_rule_admitted", t_vacuous, [
        Mutant("violating_witness_unchecked", "kernel/check.py",
               '        if (m, rid) not in violations(law, facts):', '        if False:'),
        Mutant("any_violation_counts", "kernel/check.py",
               '        if (m, rid) not in violations(law, facts):',
               '        if not any(s == m for s, _ in violations(law, facts)):')]),
    Pin("impossible_rule_admitted", t_impossible, [
        Mutant("satisfying_witness_unchecked", "kernel/check.py",
               '        if not passes(state, law, m, w):\n            raise Refuse("impossible_rule", "a satisfying witness is violated")',
               '        if False:\n            raise Refuse("impossible_rule", "a satisfying witness is violated")')]),
    Pin("unsigned_change", t_unsigned_change, [
        Mutant("power_unchecked", "kernel/check.py",
               '    if e["type"] not in keys[key_id].powers:', '    if False:')]),
    Pin("history_rewritten", t_history_rewritten, [
        Mutant("signature_always_valid", "kernel/sig.py",
               '    return ed25519_verify(pubkey_blob[-32:], sig64, signed_data(message))',
               '    return True or ed25519_verify(pubkey_blob[-32:], sig64, signed_data(message))')]),
    Pin("fork_admitted", t_fork, [
        Mutant("parent_unchecked", "kernel/check.py",
               '    if e["parent"] != state.head:\n        raise Refuse("parent_mismatch")',
               '    if False:\n        raise Refuse("parent_mismatch")')]),
    Pin("redundancy_unreported", t_redundancy, [
        Mutant("lapse_never_reported", "kernel/check.py",
               '    remaining, out, m = in_force(state), [], n + 1',
               '    return []\n    remaining, out, m = in_force(state), [], n + 1')]),
    Pin("unattributed_entry", t_unattributed, [
        Mutant("empty_proposer_admitted", "kernel/check.py",
               '    if e["proposer"] == "":\n        raise Refuse("no_proposer")', '    if False:\n        raise Refuse("no_proposer")'),
        Mutant("unknown_key_trusted", "kernel/check.py",
               '    key_id = next((k for k, d in keys.items() if d.blob == blob), None)',
               '    key_id = next((k for k, d in keys.items() if d.blob == blob), next(iter(keys), None))')]),
    Pin("forged_signature_admitted", t_forged_signature, [
        Mutant("s_bound_unchecked", "kernel/sig.py",
               '    if a is None or r is None or s >= L:', '    if a is None or r is None:')]),
    Pin("orphaned_rule_admitted", t_orphaned_rule, [
        Mutant("orphan_recheck_skipped", "kernel/check.py",
               '        if not any(passes(state, law, m, w) for w in q.satisfying):\n            raise Refuse("orphans_rule"',
               '        if False:\n            raise Refuse("orphans_rule"')]),
    Pin("checker_drift", t_checker_drift, [
        Mutant("reason_code_flipped", "kernel2/check", "bad_signature", "bad_signatur3")]),
]
