"""The pins (CHARTER §9): attack fixture, named mutant(s), passing twin. Data, run by pins/run.py.

Each test takes the root of the tree under test and runs that tree's checker or
judge as a subprocess, so the same fixtures run unchanged against the second
checker. Expectations are exact (seq, reason) or exact acceptance, so a mutant
cannot survive by failing for a different reason. C0 is the record only: the
rule pins of §9 (final_law_for_all, vacuous_rule_admitted,
impossible_rule_admitted, redundancy_unreported) return with the law language
in C1; unsigned_change reads over `key` entries, the change entries of C0. The
differential pins of SPEC §9a.7 run the tree's harness/diff.py over shell-script checkers.
"""
import functools
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import namedtuple

from harness import build, diff, gitfix, keys, runner
from harness.build import proposal
from kernel import log, sig
from pins.fixtures import bind_genesis, ledger_cases, make_repo, propose

Pin = namedtuple("Pin", "name test mutants")
Mutant = namedtuple("Mutant", "name path find replace")
L = sig.L


@functools.lru_cache(None)
def world():
    return build.World(tempfile.mkdtemp(prefix="pins-"))


def refused(v, seq, reason):
    got = (v.get("ok"), v.get("seq"), v.get("reason"))
    assert got == (False, seq, reason), f"expected {(seq, reason)}, got {v}"


def admitted(v, entries):
    assert v == {"ok": True, "entries": entries}, v


def judged(root, fx):
    return runner.judge_with(root, fx.repo, "main", "pr")


def commit(repo, msg, proposer="builder pin-model pin-session"):
    return gitfix.commit_all(repo, msg + (f"\n\nProposer: {proposer}" if proposer else ""))


def proposal_touching(root, path, party="builder", data="x\n", key=None):
    fx = make_repo(world(), root=root)  # trunk's judge/scope.json is the tree's, so a scope.json mutant reaches the judge
    gitfix.write(fx.repo, path, data)
    propose(fx.repo, fx.log, world(), party, key=key)
    return judged(root, fx)


def judge_refuses(r, reason):
    assert (r.get("ok"), r.get("reason")) == (False, reason), r


# --- judge pins -------------------------------------------------------------

def t_trusted_path(root):
    w = world()
    for path in ("kernel/check.py", "judge/judge.py", "kernel2/check"):
        fx = make_repo(w)
        gitfix.write(fx.repo, path, 'print(\'{"ok": true, "entries": 0}\')\n')
        commit(fx.repo, "edit trusted file")
        r = judged(root, fx)
        assert (r.get("ok"), r.get("reason")) == (False, "trusted_path"), (path, r)
    fx = make_repo(w)
    gitfix.write(fx.repo, "README.md", "docs only\n")
    propose(fx.repo, fx.log, w, "counsel", "docs")
    assert judged(root, fx).get("ok") is True


def t_trusted_rename(root):
    w = world()
    for old, new in (("SPEC.md", "docs/SPEC.md"), ("CHARTER.md", "CHARTER.old.md"), ("kernel/sig.py", "kernel/sig_.py")):
        fx = make_repo(w)
        gitfix.move(fx.repo, old, new)
        commit(fx.repo, "rename")
        r = judged(root, fx)
        assert old not in r.get("touched", [old]), f"fixture: git must report the rename under its new name only: {r}"
        assert (r.get("ok"), r.get("reason")) == (False, "trusted_path"), (old, new, r)
    fx = make_repo(w)
    gitfix.move(fx.repo, "README.md", "transcripts/README.md")
    propose(fx.repo, fx.log, w, "counsel", "rename docs")
    assert judged(root, fx).get("ok") is True


def t_judge_from_proposal(root):
    from judge import judge as trunk_judge  # pristine, only to compute the fixture trunk's digest
    w = world()
    fx = make_repo(w)
    propose(fx.repo, fx.log, w)
    fx.log.add("merge", "guy", build.merge(1, "ab" * 32), w.guy)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    commit(fx.repo, "merge judged by a checker the proposal supplied")
    r = judged(root, fx)
    assert (r.get("ok"), r.get("reason")) == (False, "judge_from_proposal"), r
    fx.log.lines.pop()
    fx.log.add("merge", "guy", build.merge(1, trunk_judge.digest(fx.repo, fx.main)), w.guy)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    commit(fx.repo, "merge judged by trunk")
    assert judged(root, fx).get("ok") is True
    fx = make_repo(w)
    propose(fx.repo, fx.log, w)
    assert judged(root, fx).get("ok") is True


def t_unattributed_proposal(root):
    """SPEC §10.7: the party is the principal of the key that signed the last appended proposal entry naming a
    commit of the proposal, under the law in force at that entry; no later commit changes more than log.jsonl."""
    w = world()
    judge_refuses(judged(root, trailer_only(w)), "unattributed_proposal")  # a Proposer trailer, no entry
    fx = make_repo(w)  # a signed entry, but naming trunk's commit, not one of the proposal's
    fx.log.add("proposal", "builder", proposal("a", commit=fx.main), w.parties["builder"])
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    commit(fx.repo, "entry")
    judge_refuses(judged(root, fx), "unattributed_proposal")
    fx = make_repo(w)  # a commit after the named one changes more than log.jsonl
    gitfix.write(fx.repo, "sim/x.py", "x\n")
    propose(fx.repo, fx.log, w)
    gitfix.write(fx.repo, "sim/y.py", "y\n")
    commit(fx.repo, "after the entry")
    judge_refuses(judged(root, fx), "unattributed_proposal")
    fx = make_repo(w)  # the key re-declared to another principal after the entry: the party is the law's at the entry
    gitfix.write(fx.repo, "sim/x.py", "x\n")
    propose(fx.repo, fx.log, w)
    fx.log.add("key", "guy", build.decl("builder-1", "reviewer", w.parties["builder"], ["proposal"]), w.guy)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    commit(fx.repo, "re-declare")
    r = judged(root, fx)
    assert (r.get("ok"), r.get("proposer")) == (True, "builder"), r
    fx = make_repo(w)  # two entries name the work, ann's then builder's, on a path both may touch: the last attributes
    gitfix.write(fx.repo, "transcripts/t.txt", "x\n")
    work = commit(fx.repo, "work")
    fx.log.add("proposal", "ann", proposal("ann", commit=work), w.ann)
    fx.log.add("proposal", "builder", proposal("builder", commit=work), w.parties["builder"])
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    commit(fx.repo, "entries")
    r = judged(root, fx)
    assert (r.get("ok"), r.get("proposer")) == (True, "builder"), r
    assert proposal_touching(root, "sim/x.py").get("ok") is True


def trailer_only(w):
    fx = make_repo(w)
    gitfix.write(fx.repo, "README.md", "x\n")
    commit(fx.repo, "change", "builder m s")
    return fx


def t_counsel_builds(root):
    """SPEC §10.8: counsel touches documents only."""
    judge_refuses(proposal_touching(root, "sim/gen.py", "counsel"), "party_scope")
    assert proposal_touching(root, "transcripts/t.txt", "counsel").get("ok") is True
    assert proposal_touching(root, "sim/gen.py", "builder").get("ok") is True


def t_builder_pin(root):
    """SPEC §10.8: a builder may not touch the pins that judge it, though a reviewer's entry naming the same commit precedes its own."""
    w = world()
    fx = make_repo(w, root=root)
    gitfix.write(fx.repo, "pins/p.py", "x\n")
    work = commit(fx.repo, "work")
    for party in ("reviewer", "builder"):
        fx.log.add("proposal", party, proposal(party, commit=work), w.parties[party])
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    commit(fx.repo, "entries")
    judge_refuses(judged(root, fx), "party_scope")
    assert proposal_touching(root, "pins/p.py", "reviewer").get("ok") is True
    assert proposal_touching(root, "tests/t.py", "builder").get("ok") is True


def t_reviewer_code(root):
    """SPEC §10.8: a reviewer touches pins and vectors, never code; the party is the key's principal, not its key_id."""
    judge_refuses(proposal_touching(root, "sim/x.py", "reviewer"), "party_scope")
    assert proposal_touching(root, "spec/vectors/v.json", "reviewer").get("ok") is True


def t_scope(root):
    """SPEC §10.9: every touched path, both sides of a rename included, is under judge/scope.json's paths."""
    w = world()
    judge_refuses(proposal_touching(root, "docs/x.md", "ann", key=w.ann), "out_of_scope")
    fx = make_repo(w)
    gitfix.git(fx.repo, "checkout", "-q", "main")
    gitfix.write(fx.repo, "notes.txt", "trunk's\n")
    commit(fx.repo, "trunk note")
    gitfix.git(fx.repo, "checkout", "-q", "pr")
    gitfix.git(fx.repo, "reset", "-q", "--hard", "main")
    gitfix.move(fx.repo, "notes.txt", "transcripts/notes.txt")
    propose(fx.repo, fx.log, w, "ann", "move a file into scope", w.ann)
    judge_refuses(judged(root, fx), "out_of_scope")
    assert proposal_touching(root, "transcripts/notes.txt", "ann", key=w.ann).get("ok") is True


def t_code_cap(root):
    """SPEC §10.10: counted python lines at the head stay within the cap."""
    with open(os.path.join(root, "judge", "scope.json")) as f:
        cap = json.load(f)["cap"]
    judge_refuses(proposal_touching(root, "sim/big.py", data="x = 1\n" * (cap + 1)), "code_cap")
    assert proposal_touching(root, "sim/big.py", data="x = 1\n" * cap).get("ok") is True


def t_shebang_counted(root):
    """SPEC §10.10: a file whose first line is a #! line naming python is counted, .py or not."""
    with open(os.path.join(root, "judge", "scope.json")) as f:
        cap = json.load(f)["cap"]
    judge_refuses(proposal_touching(root, "tools/big", data="#!/usr/bin/env python3\n" + "x = 1\n" * cap), "code_cap")
    assert proposal_touching(root, "tools/big", data="#!/usr/bin/env python3\n" + "x = 1\n" * (cap - 1)).get("ok") is True
    assert proposal_touching(root, "tools/big", data="#!/bin/sh\n" + "x\n" * cap).get("ok") is True


def t_foreign_object(root):
    """SPEC §10.9: a symbolic link, or a submodule whose commit is present or absent, under paths is refused out_of_scope
    and named, whatever it points to; a regular file at the same path is admitted. SPEC §10.1: under a trusted path,
    a submodule is trusted_path at either commit, before any digest: trunk holding one fails its own self-check (a regular
    file there passes it), and a proposal adding one whose commit is absent is refused, not crashed on."""
    def place(repo, kind, rel):
        if kind == "link":
            gitfix.write(repo, "transcripts/long", "#!/usr/bin/env python3\n" + "x = 1\n" * 9000)
            gitfix.link(repo, rel, "../transcripts/long")
        elif kind == "file":
            gitfix.write(repo, rel, "x = 1\n")
        else:
            gitfix.gitlink(repo, rel, None if kind == "present" else "12" * 20)
    for kind, rel in (("link", "tools/script"), ("present", "tools/vendor.py"), ("absent", "transcripts/sub")):
        for k in (kind, "file"):
            fx = make_repo(world(), root=root)
            place(fx.repo, k, rel)
            propose(fx.repo, fx.log, world())
            r = judged(root, fx)
            if k == "file":
                assert r.get("ok") is True, (rel, r)
            else:
                judge_refuses(r, "out_of_scope")
                assert rel in r["detail"], r
    for kind in ("present", "file"):
        fx = make_repo(world(), root=root)
        gitfix.git(fx.repo, "checkout", "-q", "main")
        gitfix.place(fx.repo, kind, "kernel/vendor")
        commit(fx.repo, "trunk's trusted base")  # bind_genesis digests HEAD, so the object is committed first
        bind_genesis(fx.repo, fx.log, world())
        r = runner.judge_with(root, fx.repo, "main", "main")
        if kind == "file":
            assert r.get("ok") is True, r
        else:
            judge_refuses(r, "trusted_path")
            assert "kernel/vendor" in r["detail"], r
    fx = make_repo(world(), root=root)
    gitfix.place(fx.repo, "absent", "kernel/vendor")
    propose(fx.repo, fx.log, world())
    r = judged(root, fx)
    judge_refuses(r, "trusted_path")
    assert "kernel/vendor" in r["detail"], r


def t_push_unrecorded(root):
    """A trusted-base change must be recorded, on proposals and the self-check."""
    from judge import judge as trusted_judge
    fx = make_repo(world())
    gitfix.git(fx.repo, "checkout", "-q", "main")
    gitfix.write(fx.repo, "SPEC.md", "changed trusted text\n")
    commit(fx.repo, "Guy changes the trusted base")
    for head in ("main", "pr"):
        if head == "pr":
            gitfix.git(fx.repo, "checkout", "-q", "pr")
            gitfix.git(fx.repo, "reset", "-q", "--hard", "main")
            gitfix.write(fx.repo, "README.md", "docs\n")
            propose(fx.repo, fx.log, world(), "counsel", "docs")
        judge_refuses(runner.judge_with(root, fx.repo, "main", head), "trusted_base_unrecorded")
    gitfix.git(fx.repo, "checkout", "-q", "main")
    fx.log.add("push", "guy", {"digest": trusted_judge.digest(fx.repo, "main"), "review": "0" * 64}, world().guy)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    commit(fx.repo, "Record the trusted base")
    assert runner.judge_with(root, fx.repo, "main", "main").get("ok") is True


def charter_judged(root, charter=None, amend=None):
    """Verdicts on main against itself and on a docs proposal, after Guy's trunk commit editing CHARTER.md, amending, or both."""
    w = world()
    fx = make_repo(w)
    gitfix.git(fx.repo, "checkout", "-q", "main")
    if charter is not None:
        gitfix.write(fx.repo, "CHARTER.md", charter)
    if amend is not None:
        fx.log.add("decision", "guy", {"kind": "transmute", "subject": "A2"}, w.guy)
        fx.log.add("amend", "guy", {"id": "A2", "charter": amend, "activate_at": 9}, w.guy)
        gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    commit(fx.repo, "Guy changes the charter")
    gitfix.git(fx.repo, "checkout", "-q", "pr")
    gitfix.git(fx.repo, "reset", "-q", "--hard", "main")
    gitfix.write(fx.repo, "README.md", "docs\n")
    propose(fx.repo, fx.log, w, "counsel", "docs")
    return [runner.judge_with(root, fx.repo, "main", head) for head in ("main", "pr")]


def t_charter_edit_unrecorded(root):
    """SPEC §10.2: an edit to trunk's CHARTER.md lands only with the amend recording its SHA-256."""
    edited = gitfix.CHARTER_TEXT + "A2. An amendment.\n"
    for r in charter_judged(root, charter=edited):
        judge_refuses(r, "charter_mismatch")
    for r in charter_judged(root, charter=edited, amend=hashlib.sha256(edited.encode()).hexdigest()):
        assert r.get("ok") is True, r


def t_amend_stale(root):
    """SPEC §10.2: the promulgated charter is the latest amend's, not genesis's, and must be trunk's CHARTER.md."""
    for r in charter_judged(root, amend="ff" * 32):
        judge_refuses(r, "charter_mismatch")
    for r in charter_judged(root, amend=gitfix.CHARTER_SHA256):
        assert r.get("ok") is True, r


def t_freeze_ignored(root):
    w = world()
    for height, reason in ((4, "push_during_amendment"), (3, None)):
        fx = make_repo(w)
        fx.log.add("decision", "guy", {"kind": "transmute", "subject": "A2"}, w.guy)
        fx.log.add("amend", "guy", {"id": "A2", "charter": gitfix.CHARTER_SHA256, "activate_at": height}, w.guy)
        fx.log.add("push", "guy", {"digest": json.loads(fx.log.lines[0])["body"]["checker"], "review": "0" * 64}, w.guy)
        gitfix.write(fx.repo, "log.jsonl", fx.log.text())
        propose(fx.repo, fx.log, w, msg="Amend then push")
        r = judged(root, fx)
        if reason:
            judge_refuses(r, reason)
        else:
            assert r.get("ok") is True, r


def t_one_act_amendment(root):
    w = world()
    for transmute in (False, True):
        fx = make_repo(w)
        if transmute:
            fx.log.add("decision", "guy", {"kind": "transmute", "subject": "A2"}, w.guy)
        fx.log.add("amend", "guy", {"id": "A2", "charter": gitfix.CHARTER_SHA256, "activate_at": 9}, w.guy)
        gitfix.write(fx.repo, "log.jsonl", fx.log.text())
        propose(fx.repo, fx.log, w, msg="Amend")
        r = judged(root, fx)
        if transmute:
            assert r.get("ok") is True, r
        else:
            judge_refuses(r, "amend_untransmuted")


def t_decision_forged(root):
    w = world()
    for sovereign in (False, True):
        fx = make_repo(w)
        fx.log.add("key", "guy", build.decl("stranger-1", "guy", w.stranger, ["decision"]), w.guy)
        fx.log.add("decision", "guy", {"kind": "fix", "subject": "x"}, w.guy if sovereign else w.stranger)
        gitfix.write(fx.repo, "log.jsonl", fx.log.text())
        propose(fx.repo, fx.log, w, msg="Decision")
        r = judged(root, fx)
        if sovereign:
            assert r.get("ok") is True, r
        else:
            judge_refuses(r, "decision_by_other")
        gitfix.git(fx.repo, "branch", "-f", "main", "pr")
        r = runner.judge_with(root, fx.repo, "main", "main")
        if sovereign:
            assert r.get("ok") is True, r
        else:
            judge_refuses(r, "decision_by_other")


# --- kernel pins ------------------------------------------------------------

def t_unsigned_change(root):
    w = world()
    lg = w.log(); lg.add("key", "ann", build.decl("x", "ann", w.stranger, ["proposal"]), w.ann)
    refused(runner.check_with(root, lg.lines), 1, "no_power")
    lg = w.log(); lg.add("key", "ann", build.decl("ann-1", "ann", w.ann, ["proposal", "key"]), w.ann)
    refused(runner.check_with(root, lg.lines), 1, "no_power")
    lg = w.log(); lg.add("key", "guy", build.decl("x", "stranger", w.stranger, ["proposal"]), w.guy)
    lg.add("proposal", "stranger", proposal(), w.stranger)
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


def t_weak_key(root):
    w = world()
    for name, pub32 in keys.weak_keys():
        lg = w.log(); lg.add("key", "guy", build.decl("eve-1", "eve", keys.fake_key(pub32), ["proposal"]), w.guy)
        refused(runner.check_with(root, lg.lines), 1, "bad_key")
    name, pub32 = keys.weak_keys()[0]
    lg = build.Log(); lg.add("genesis", "guy", build.genesis_body(w.decls + [build.decl("eve-1", "eve", keys.fake_key(pub32), [])]), w.guy)
    refused(runner.check_with(root, lg.lines), 0, "bad_key")
    lg = w.log(); lg.add("key", "guy", build.decl("stranger-1", "stranger", w.stranger, ["proposal"]), w.guy)
    admitted(runner.check_with(root, lg.lines), 2)


def t_reserved_bytes(root):
    w = world()
    lg = w.log()
    lg.add("proposal", "ann", proposal("a"), w.ann)
    admitted(runner.check_with(root, lg.lines), 2)
    e = log.parse_line(lg.lines[1])
    e["sig"] = keys.rewrap(e["sig"], reserved=b"\x00")
    refused(runner.check_with(root, [lg.lines[0], log.canonical(e)]), 1, "bad_signature")


def t_ts_instant(root):
    """A timestamp must be an existing UTC instant in ASCII digits."""
    w = world()
    for ts in ("\uff12\uff10\uff12\uff16-10-14T00:00:00Z", "2026-13-14T00:00:00Z", "2026-02-29T00:00:00Z", "2026-10-14T00:00:60Z"):
        lg = w.log(); lg.add("proposal", "ann", proposal("a"), w.ann, ts=ts)
        refused(runner.check_with(root, lg.lines), 1, "schema")
    lg = w.log(); lg.add("proposal", "ann", proposal("a"), w.ann, ts="2028-02-29T23:59:59Z")
    admitted(runner.check_with(root, lg.lines), 2)


def t_deep_nesting(root):
    """Nesting beyond 32 is malformed_json at any depth, never a crash."""
    for depth in (33, 100000):
        refused(runner.check_with(root, ['{"a":' * depth + "1" + "}" * depth]), 0, "malformed_json")
    refused(runner.check_with(root, ['{"a":' * 32 + "1" + "}" * 32]), 0, "schema")


def t_big_integer(root):
    """A very long integer is not_canonical, never unreadable."""
    refused(runner.check_with(root, ['{"a":' + "9" * 5000 + "}"]), 0, "not_canonical")


def t_pubkey_reused(root):
    """A public key belongs to one key_id for the life of the log, even after rotation."""
    w = world()
    lg = w.log(); lg.add("key", "guy", build.decl("ann-1", "ann", w.stranger, ["proposal"]), w.guy)
    base = list(lg.lines)
    lg.add("key", "guy", build.decl("eve-1", "eve", w.ann, ["proposal"]), w.guy)
    refused(runner.check_with(root, lg.lines), 2, "bad_key")
    lg = build.Log(base); lg.add("key", "guy", build.decl("ann-1", "ann", w.ann, ["proposal"]), w.guy)
    admitted(runner.check_with(root, lg.lines), 3)


def t_key_decl_members(root):
    """A key declaration has exactly four members."""
    w = world()
    lg = w.log(); lg.add("key", "guy", dict(build.decl("eve-1", "eve", w.stranger, ["proposal"]), note="x"), w.guy)
    refused(runner.check_with(root, lg.lines), 1, "schema")
    lg = w.log(); lg.add("key", "guy", build.decl("eve-1", "eve", w.stranger, ["proposal"]), w.guy)
    admitted(runner.check_with(root, lg.lines), 2)


def t_last_key_revocable(root):
    """The power to declare keys, once lost, can be regained by no entry: its last holder cannot drop it."""
    w = world()
    lg = w.log(); lg.add("key", "guy", build.decl("guy-master", "guy", w.guy, [t for t in build.ALL if t != "key"]), w.guy)
    refused(runner.check_with(root, lg.lines), 1, "bad_key")
    lg = w.log(); lg.add("key", "guy", build.decl("guy-master", "guy", w.guy, build.ALL), w.guy)
    admitted(runner.check_with(root, lg.lines), 2)


def t_kernel2_runnable(root):
    """The judge runs trunk's kernel2 with git's file modes, so its launcher may call its own scripts."""
    fx = make_repo(world())
    gitfix.git(fx.repo, "checkout", "-q", "main")
    gitfix.write(fx.repo, "kernel2/check", '#!/bin/sh\nexec "$(dirname "$0")/helper.sh" "$@"\n')
    gitfix.write(fx.repo, "kernel2/helper.sh", "#!/bin/sh\necho '{\"ok\":true,\"entries\":1}'\n")
    for name in ("check", "helper.sh"):
        os.chmod(os.path.join(fx.repo, "kernel2", name), 0o755)
    commit(fx.repo, "kernel2 whose launcher calls a helper")
    bind_genesis(fx.repo, fx.log, world())
    r = runner.judge_with(root, fx.repo, "main", "main")
    assert r.get("ok") is True and r.get("kernel2") == {"ok": True, "entries": 1}, r


def t_selfcheck_blind(root):
    """The CI self-check fails when the judge cannot run kernel2, and passes when it can."""
    def repo(helper_mode):
        fx = make_repo(world())
        gitfix.git(fx.repo, "checkout", "-q", "main")
        gitfix.write(fx.repo, "kernel2/check", '#!/bin/sh\nexec "$(dirname "$0")/helper.sh" "$@"\n')
        gitfix.write(fx.repo, "kernel2/helper.sh", "#!/bin/sh\necho '{\"ok\":true,\"entries\":1}'\n")
        os.chmod(os.path.join(fx.repo, "kernel2", "check"), 0o755)
        os.chmod(os.path.join(fx.repo, "kernel2", "helper.sh"), helper_mode)
        commit(fx.repo, "kernel2")
        bind_genesis(fx.repo, fx.log, world())
        return fx.repo
    def run(r):
        import subprocess
        return subprocess.run([sys.executable, os.path.join(root, "judge", "selfcheck.py"), "--repo", r],
                              capture_output=True, text=True).returncode
    assert run(repo(0o644)) == 1, "self-check passed a trunk whose kernel2 cannot run"
    assert run(repo(0o755)) == 0, "self-check failed a healthy trunk"


def t_checker_drift(root):
    """The C0 second checker agrees on C0 pin fixtures and vectors (C1 vectors live in c1/)."""
    w = world()
    def founding():
        declarations = [dict(d, powers=[p for p in d["powers"] if p in ("genesis", "key", "proposal", "merge")]) for d in w.decls]
        lg = build.Log()
        lg.add("genesis", "guy", build.genesis_body(declarations), w.guy)
        return lg
    logs = [founding().lines]
    lg = founding(); lg.add("key", "guy", build.decl("stranger-1", "stranger", w.stranger, ["proposal"]), w.guy)
    lg.add("proposal", "stranger", proposal(), w.stranger); logs.append(list(lg.lines))
    lg = founding(); lg.add("proposal", "guy", proposal(), w.stranger); logs.append(lg.lines)
    lg = founding(); lg.add("proposal", "guy", proposal(), w.guy)            # body altered after signing
    e = log.parse_line(lg.lines[1]); e["body"]["title"] += "x"; logs.append([lg.lines[0], log.canonical(e)])
    with tempfile.TemporaryDirectory() as tmp:
        paths = sorted(glob.glob(os.path.join(root, "spec", "vectors", "logs", "*.jsonl")))  # every reason code
        for i, lines in enumerate(logs):
            paths.append(os.path.join(tmp, f"{i}.jsonl"))
            with open(paths[-1], "w") as f:
                f.write("".join(l + "\n" for l in lines))
        bad = diff.compare([sys.executable, "-E", "-s", "-m", "kernel.check"], [os.path.join(root, "kernel2", "check")], paths)
    assert not bad, bad


# --- ledger pins (BRIEF-C1.md, C1a) -----------------------------------------------------------

@functools.lru_cache(None)
def ledger():
    return ledger_cases(world())


def ledger_pin(*names):
    """A pin over pins/fixtures.py's ledger logs: each gives exactly its (seq, reason), or is admitted whole."""
    def test(root):
        for name in names:
            lg, want = ledger()[name]
            v = runner.check_with(root, lg.lines)
            admitted(v, want) if isinstance(want, int) else refused(v, *want)
    return test


SCORE_TABLE = """| proposer | type | resolved | mean p | rate | loss | base-rate loss |
|---|---|---:|---:|---:|---:|---:|
| builder | pins_green | 1 | 0.8000 | 1.0000 | 0.2231 | 0.6931 |
| builder | world.delivery | 1 | 0.9000 | 0.0000 | 2.3026 | 0.6931 |
| counsel | pins_green | 1 | 0.5000 | 1.0000 | 0.6931 | 0.6931 |
| counsel | world.screen | 2 | 0.4500 | 0.5000 | 0.4338 | 0.8959 |
| reviewer | pins_green | 1 | 0.7000 | 0.0000 | 1.2040 | 1.0986 |"""  # BRIEF-C1.md, verbatim


def t_score_proper(root):
    """BRIEF-C1.md criterion 5: `jack score` on the reviewer's witness, spec/vectors/score.jsonl, prints the brief's table first,
    exactly; run in a copy of the tools holding only that log, so the tree's own log.jsonl is never touched."""
    with tempfile.TemporaryDirectory() as tmp:
        for d in ("tools", "kernel", "judge", "harness"):
            shutil.copytree(os.path.join(root, d), os.path.join(tmp, d), ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(os.path.join(root, "spec", "vectors", "score.jsonl"), os.path.join(tmp, "log.jsonl"))
        r = subprocess.run([sys.executable, os.path.join(tmp, "tools", "jack"), "score"], cwd=tmp, capture_output=True, text=True)
    assert (r.returncode, r.stdout.split("\n\n")[0]) == (0, SCORE_TABLE), r.stdout + r.stderr


# --- differential pins (SPEC §9a.7) ----------------------------------------------

def toy(body='echo "{\\"ok\\":true,\\"entries\\":$n}"', wrong_at=-1):
    """A shell checker that accepts every log of n lines, but claims 9 entries at length wrong_at."""
    return f'n=$(($(wc -l < "$1"))); [ $n -eq {wrong_at} ] && n=9; {body}\n'


def differential(root, b, a=toy(), timeout=60):
    """(exit status, report) of root's harness/diff.py over a three-line log; a checker given as None does not exist."""
    with tempfile.TemporaryDirectory() as tmp:
        path = lambda body: os.path.join(tmp, "missing" if body is None else "a" if body == a else "b")  # noqa: E731
        for name, body in [(path(c), "#!/bin/sh\n" + c) for c in {a, b} - {None}] + [(os.path.join(tmp, "log"), "x\ny\nz\n")]:
            with open(name, "w") as f:
                f.write(body)
            os.chmod(name, 0o755)
        r = subprocess.run([sys.executable, os.path.join(root, "harness", "diff.py"), "--a", path(a), "--b", path(b),
                            "--timeout", str(timeout), os.path.join(tmp, "log")], capture_output=True, text=True)
    return r.returncode, json.loads(r.stdout)


def lengths(rc, report):
    return rc, [d["length"] for d in report["disagreements"]]


def t_whole_log_only(root):
    """A second checker wrong only on a proper prefix is caught."""
    assert lengths(*differential(root, toy(wrong_at=1))) == (1, [1])
    assert lengths(*differential(root, toy())) == (0, [])


def t_loose_parse(root):
    """{"ok":1,...}, or a correct object with the wrong exit status, is no verdict; a respaced object is one."""
    for b in (toy('echo "{\\"ok\\":1,\\"entries\\":$n}"'), toy('echo "{\\"ok\\":true,\\"entries\\":$n}"; exit 1')):
        assert lengths(*differential(root, b)) == (1, [0, 1, 2, 3]), b
    assert lengths(*differential(root, toy('echo "{ \\"entries\\": $n, \\"ok\\": true }"'))) == (0, [])


def t_crash_as_agreement(root):
    """A crash, a missing checker or a timeout disagrees, even with the same failure from the other checker."""
    for bad in ("exit 3\n", "exec sleep 30\n", None):
        assert lengths(*differential(root, bad, bad, timeout=0.3)) == (1, [0, 1, 2, 3]), bad
    assert lengths(*differential(root, toy(), toy())) == (0, [])


def t_prefix_skipped(root):
    """Every proper prefix is compared, the empty log and the longest included."""
    for k in (0, 2):
        assert lengths(*differential(root, toy(wrong_at=k))) == (1, [k]), k
    rc, report = differential(root, toy())
    assert (rc, report["logs"], report["prefixes"]) == (0, 1, 3), report


GUARD = 'if digest(repo, head) != report["trusted_digest"] or show(repo, head, CHARTER) != show(repo, trunk, CHARTER):'

CHARTER_MISMATCH = '    if old and promulgated_charter(repo, trunk, trunk_log) != hashlib.sha256(show(repo, trunk, CHARTER) or b"").hexdigest():'

# each party pin's mutant removes that party's list from judge/scope.json and nothing else (SPEC §10)
BUILDER_LIST = '"builder": ["sim/", "harness/", "tests/", "tools/", "transcripts/", "log.jsonl"],\n             '
REVIEWER_LIST = '\n             "reviewer": ["pins/", "spec/vectors/", "transcripts/", "log.jsonl"],'
COUNSEL_LIST = (',\n             "counsel": ["REPORT.md", "BRIEF-C1.md", "LAW.md", "README.md", "RUNBOOK.md",'
                '\n                         "transcripts/", "sim/runs/", "log.jsonl"]')

PINS = [
    Pin("charter_edit_unrecorded", t_charter_edit_unrecorded, [
        Mutant("charter_unchecked", "judge/judge.py", CHARTER_MISMATCH, "    if False:")]),
    Pin("amend_stale", t_amend_stale, [
        Mutant("genesis_charter_compared", "judge/judge.py", CHARTER_MISMATCH,
               CHARTER_MISMATCH.replace("promulgated_charter(repo, trunk, trunk_log)", "genesis_charter(old[0])"))]),
    Pin("push_unrecorded", t_push_unrecorded, [
        Mutant("trusted_base_unchecked", "judge/judge.py", '    if old and trusted != report["trusted_digest"]:', '    if False:')]),
    Pin("freeze_ignored", t_freeze_ignored, [
        Mutant("amendment_freeze_unchecked", "judge/judge.py", '    if any(a["seq"] < e["seq"] < a["body"]["activate_at"]', '    if any(False and a["seq"] < e["seq"] < a["body"]["activate_at"]')]),
    Pin("one_act_amendment", t_one_act_amendment, [
        Mutant("transmutation_unchecked", "judge/judge.py", '        if e["type"] == "amend" and e["body"]["id"] not in transmuted:', '        if False:')]),
    Pin("decision_forged", t_decision_forged, [
        Mutant("sovereign_unchecked", "judge/judge.py", '        if e["type"] == "decision" and base64.b64encode(blob[14:14 + n]).decode() not in founders:', '        if False:')]),
    Pin("trusted_path_unguarded", t_trusted_path, [
        Mutant("guard_removed", "judge/judge.py", GUARD, "if False:"),
        Mutant("judge_dir_untrusted", "judge/judge.py",
               'TRUSTED = ("kernel/", "kernel2/", "judge/", ".github/workflows/", "SPEC.md")',
               'TRUSTED = ("kernel/", "kernel2/", ".github/workflows/", "SPEC.md")')]),
    Pin("trusted_rename_admitted", t_trusted_rename, [
        Mutant("path_guard_only", "judge/judge.py", GUARD,
               'if any(is_under(p, TRUSTED + (CHARTER,)) for p in report["touched"]):')]),
    Pin("judge_from_proposal", t_judge_from_proposal, [
        Mutant("digest_unchecked", "judge/judge.py",
               'if e["type"] == "merge" and e["body"]["checker"] != report["trusted_digest"]:',
               'if e["type"] == "merge" and False:')]),
    Pin("unattributed_proposal_admitted", t_unattributed_proposal, [
        Mutant("commit_unchecked", "judge/judge.py",
               ' and e["body"]["commit"] in commits]', ']'),
        Mutant("later_commits_unchecked", "judge/judge.py", '    if later - {LOG}:', '    if False:'),
        Mutant("law_at_end", "judge/judge.py",
               '[e["body"] for e in entries[1:i] if e["type"] == "key"]', '[e["body"] for e in entries[1:] if e["type"] == "key"]'),
        Mutant("first_entry_attributes", "judge/judge.py", '    seq, last = named[-1]', '    seq, last = named[0]'),
        Mutant("party_by_key_id", "judge/judge.py", 'next((d["principal"] for d in', 'next((d["key_id"] for d in')]),
    Pin("counsel_build_admitted", t_counsel_builds, [
        Mutant("counsel_unlisted", "judge/scope.json", COUNSEL_LIST, "")]),
    Pin("builder_pin_admitted", t_builder_pin, [
        Mutant("builder_unlisted", "judge/scope.json", BUILDER_LIST, "")]),
    Pin("reviewer_code_admitted", t_reviewer_code, [
        Mutant("reviewer_unlisted", "judge/scope.json", REVIEWER_LIST, "")]),
    Pin("scope_unguarded", t_scope, [
        Mutant("scope_unchecked", "judge/judge.py",
               '    if any(not is_under(p, scope["paths"]) for p in changed):', '    if False:'),
        Mutant("rename_hides_source", "judge/judge.py",
               'changed = touched(repo, trunk, head, "--no-renames")', 'changed = touched(repo, trunk, head)')]),
    Pin("cap_unguarded", t_code_cap, [
        Mutant("cap_unchecked", "judge/judge.py",
               '    if counted_lines(repo, head, scope["counted"]) > scope["cap"]:', '    if False:')]),
    Pin("shebang_uncounted", t_shebang_counted, [
        Mutant("py_suffix_only", "judge/judge.py",
               'return path.endswith(".py") or (first.startswith(b"#!") and b"python" in first)', 'return path.endswith(".py")')]),
    Pin("foreign_object_admitted", t_foreign_object, [
        Mutant("mode_unchecked", "judge/judge.py", "    if objects:\n", "    if False:\n"),
        Mutant("trusted_mode_unchecked", "judge/judge.py", "    if foreign_base:\n", "    if False:\n")]),
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
    Pin("unattributed_entry", t_unattributed, [
        Mutant("empty_proposer_admitted", "kernel/check.py",
               '    if e["proposer"] == "":\n        raise Refuse("no_proposer")', '    if False:\n        raise Refuse("no_proposer")'),
        Mutant("unknown_key_trusted", "kernel/check.py",
               '    key_id = next((k for k, d in keys.items() if d.blob == blob), None)',
               '    key_id = next((k for k, d in keys.items() if d.blob == blob), next(iter(keys), None))')]),
    Pin("forged_signature_admitted", t_forged_signature, [
        Mutant("s_bound_unchecked", "kernel/sig.py",
               '    if a is None or r is None or s >= L:', '    if a is None or r is None:')]),
    Pin("weak_key_admitted", t_weak_key, [
        Mutant("noncanonical_key_admitted", "kernel/sig.py",
               '    return a is None or _encode(_mul(8, _ext(a))) == IDENTITY',
               '    return a is not None and _encode(_mul(8, _ext(a))) == IDENTITY'),
        Mutant("small_order_key_admitted", "kernel/sig.py",
               '    return a is None or _encode(_mul(8, _ext(a))) == IDENTITY',
               '    return a is None')]),
    Pin("reserved_bytes_admitted", t_reserved_bytes, [
        Mutant("reserved_unchecked", "kernel/sig.py",
               'or hash_alg != b"sha512" or reserved != b"":', 'or hash_alg != b"sha512":')]),
    Pin("ts_not_an_instant", t_ts_instant, [
        Mutant("unicode_digits_admitted", "kernel/log.py",
               'TS = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")',
               'TS = re.compile(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z")'),
        Mutant("calendar_unchecked", "kernel/log.py",
               "        datetime.datetime(int(v[0:4]), int(v[5:7]), int(v[8:10]), int(v[11:13]), int(v[14:16]), int(v[17:19]))\n",
               "        pass\n")]),
    Pin("deep_nesting_crashes", t_deep_nesting, [
        Mutant("depth_unbounded", "kernel/log.py",
               "    if isinstance(value, (dict, list)) and depth > MAX_DEPTH:", "    if False:"),
        Mutant("recursion_uncaught", "kernel/log.py",
               "    except (ValueError, RecursionError):", "    except ValueError:")]),
    Pin("big_integer_unreadable", t_big_integer, [
        Mutant("int_digits_limited", "kernel/log.py",
               'obj = json.loads(line, parse_int=lambda s: int(s) if len(s) <= 20 else float("inf"))',
               "obj = json.loads(line)")]),
    Pin("pubkey_reused", t_pubkey_reused, [
        Mutant("ownership_forgotten", "kernel/check.py",
               '    if owners.get(blob, d["key_id"]) != d["key_id"]:', "    if False:")]),
    Pin("key_decl_extra_member", t_key_decl_members, [
        Mutant("extra_members_allowed", "kernel/log.py",
               "        if set(d) != KEY_FIELDS:", "        if False:")]),
    Pin("last_key_revocable", t_last_key_revocable, [
        Mutant("last_key_unguarded", "kernel/check.py",
               '        if not any("key" in k.powers for k in keys.values()):', "        if False:")]),
    Pin("kernel2_unrunnable", t_kernel2_runnable, [
        Mutant("modes_ignored", "judge/judge.py", "                os.chmod(dest, 0o755)", "                pass")]),
    Pin("selfcheck_blind", t_selfcheck_blind, [
        Mutant("judge_errors_ignored", "judge/selfcheck.py",
               "        return 1  # selfcheck: judge refused or failed", "        return 0")]),
    Pin("checker_drift", t_checker_drift, [
        Mutant("reason_code_flipped", "kernel2/check", "bad_signature", "bad_signatur3")]),
    Pin("whole_log_only", t_whole_log_only, [
        Mutant("prefixes_uncompared", "harness/diff.py", "for k in range(len(lines) + 1):", "for k in [len(lines)]:")]),
    Pin("loose_parse", t_loose_parse, [
        Mutant("ok_not_boolean", "harness/diff.py", 'type(v.get("ok")) is bool', '"ok" in v'),
        Mutant("exit_status_ignored", "harness/diff.py", ' and r.returncode == (not v["ok"])', "")]),
    Pin("crash_as_agreement", t_crash_as_agreement, [
        Mutant("like_failures_agree", "harness/diff.py", ' and "ok" in a else', " else")]),
    Pin("prefix_skipped", t_prefix_skipped, [
        Mutant("empty_prefix_skipped", "harness/diff.py", "for k in range(len(lines) + 1):", "for k in range(1, len(lines) + 1):"),
        Mutant("prefix_off_by_one", "harness/diff.py", "lines[:k])", "lines[:k + 1])")]),
    Pin("clock_runs_backward", ledger_pin("48_ts_decreased_bad", "ts_back_and_bad_seq", "ts_equal"), [
        Mutant("ts_unchecked", "kernel/check.py", '    if state.ts is not None and e["ts"] < state.ts:', "    if False:")]),
    Pin("self_resolution_admitted", ledger_pin("42_resolution_self_bad", "self_same_key", "other_party"), [
        Mutant("self_unchecked", "kernel/check.py",
               '    if e["type"] == "resolution" and state.forecasts[body["forecast"]] == e["proposer"]:', "    if False:")]),
    Pin("dangling_resolution_admitted", ledger_pin("43_resolution_dangling_bad", "dangling_2", "dangling_3", "dangling_9007199254740991",
                                                   "dangling_resolution_seq", "other_party"), [
        Mutant("target_unchecked", "kernel/check.py", '(body["forecast"] not in state.forecasts or body', "(body")]),
    Pin("double_resolution_admitted", ledger_pin("44_resolution_double_bad", "self_of_resolved", "second_open_forecast"), [
        Mutant("resolved_unchecked", "kernel/check.py", ' or body["forecast"] in state.resolved)', ")")]),
    Pin("past_forecast_admitted", ledger_pin("45_forecast_past_bad", "past_by_400_days", "resolves_by_equal_ts"), [
        Mutant("resolves_by_unchecked", "kernel/check.py", '    if e["type"] == "forecast" and body["resolves_by"] < e["ts"]:', "    if False:")]),
    Pin("permille_out_of_range_admitted", ledger_pin("46a_forecast_permille_0_bad", "46b_forecast_permille_1000_bad", "p_1", "p_999"), [
        Mutant("p_0_admitted", "kernel/log.py", "_is_int(v) and 1 <= v <= 999", "_is_int(v) and 0 <= v <= 999"),
        Mutant("p_1000_admitted", "kernel/log.py", "_is_int(v) and 1 <= v <= 999", "_is_int(v) and 1 <= v <= 1000")]),
    Pin("boolean_integer_admitted", ledger_pin("47_forecast_boolean_bad", "p_false", "outcome_true", "outcome_false", "forecast_true",
                                               "p_1", "outcome_0", "other_party"), [
        Mutant("p_boolean_admitted", "kernel/log.py", '"p": lambda v: _is_int(v) and', '"p": lambda v: isinstance(v, int) and'),
        Mutant("outcome_boolean_admitted", "kernel/log.py", '"outcome": lambda v: _is_int(v) and', '"outcome": lambda v: isinstance(v, int) and'),
        Mutant("booleans_are_integers", "kernel/log.py", "    return isinstance(v, int) and not isinstance(v, bool)", "    return isinstance(v, int)")]),
    Pin("self_judged_uncoded", ledger_pin("42_resolution_self_bad", "self_same_key", "49_self_resolution_bad_signature", "other_party"), [
        Mutant("self_judged_as_schema", "kernel/check.py", 'raise Refuse("self_judged",', 'raise Refuse("schema",'),
        Mutant("judged_before_signature", "kernel/check.py", "    signer(e, keys)\n    if e[\"type\"] == \"resolution\" and state.forecasts[body[\"forecast\"]] == e[\"proposer\"]:\n"
               "        raise Refuse(\"self_judged\", f\"{e['proposer']} made forecast {body['forecast']}\")  # by principal: maxim 1\n",
               "    if e[\"type\"] == \"resolution\" and state.forecasts[body[\"forecast\"]] == e[\"proposer\"]:\n"
               "        raise Refuse(\"self_judged\", f\"{e['proposer']} made forecast {body['forecast']}\")  # by principal: maxim 1\n    signer(e, keys)\n")]),
    Pin("score_not_proper", t_score_proper, [
        Mutant("linear_score", "tools/entry.py", "-math.log((p if o else 1000 - p) / 1000)", "1 - abs(o - p / 1000)"),
        Mutant("minimised_at_999", "tools/entry.py", "-math.log((p if o else 1000 - p) / 1000)", "(1000 - p) / 1000")]),
]


# --- clerk pins (BRIEF-C1b v7 §Pins; REVIEW-C1b-v7 §4) -------------------------

def fixture_tests(module, *methods):
    """Run the disposable tree's distinguishing fixtures, never this process's imports."""
    def test(root):
        names = [f"tests.{module}.test_{method}" for method in methods]
        r = subprocess.run([sys.executable, "-E", "-s", "-m", "unittest", "-q", *names],
                           cwd=root, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
    return test


clerk_tests = functools.partial(fixture_tests, "test_clerk.ClerkTest")
promotion_tests = functools.partial(fixture_tests, "test_promotion.Promotion")
status_tests = functools.partial(fixture_tests, "test_status.StatusTest")
W1_TEST = clerk_tests("w1_from_entry_strict_deadline_holders_and_discharge")
W1_OPEN = 'if e["type"] == "forecast" and e["seq"] > opening and e["seq"] not in resolved:'
TAINT = '            for _, repairs in opened.values():\n                repairs.append(seq)'
OLDEST_TAINT = Mutant("oldest_only_attribution", "tools/status.py", TAINT,
                      '            for _, repairs in list(opened.values())[:1]:\n                repairs.append(seq)')
BATCH = '            finalise(e, "batch", sorted(pending), not royal)'

# A genuine evidence-component mutant: join the new batch to all intersecting old
# components transitively, replacing their identities and recomputing the bets.
REGROUP = '''
        if kind == "batch":
            evidence = {r["body"]["forecast"]: r["body"]["evidence"] for r in es
                        if r["seq"] <= e["seq"] and r["type"] == "resolution"}
            component = items.pop()
            while True:
                labels = {evidence.get(f) for f in component["forecasts"]}
                joined = [i for i in items if labels & {evidence.get(f) for f in i["forecasts"]}]
                if not joined:
                    break
                for old in joined:
                    items.remove(old)
                    component["forecasts"] = tuple(sorted(set(component["forecasts"] + old["forecasts"])))
                    component["repairs"] = tuple(sorted(set(component["repairs"] + old["repairs"])))
                    component["Y"] &= old["Y"]
            items.append(component)
'''

C1B_PINS = [
    Pin("overdue_strictly_after", W1_TEST, [
        Mutant("equality_overdue", "tools/clerk.py", '"escalated": deadline < now', '"escalated": deadline <= now')]),
    Pin("w1_from_entry", W1_TEST, [
        Mutant("only_when_overdue", "tools/clerk.py", W1_OPEN,
               W1_OPEN[:-1] + ' and e["body"]["resolves_by"] < now:')]),
    Pin("self_holder", W1_TEST, [
        Mutant("self_filter_dropped", "tools/clerk.py", 'd["principal"] != e["proposer"]', 'True')]),
    Pin("w3_unwitnessed", promotion_tests("w3_only_earlier_green_exact_workflow_and_commit_discharge"), [
        Mutant("any_run_accepted", "tools/clerk.py",
               'r.get("path") == status.WORKFLOW and r.get("head_sha") == e["body"]["commit"] and\n'
               '                    r.get("conclusion") == "success" and status.completed_by(r, e["ts"])', 'True')]),
    Pin("w4_promote_unmet", promotion_tests("historical_bad_promote_stays_repair_after_later_success"), [
        Mutant("repair_never_raised", "tools/status.py", '        if failures:\n', '        if False:\n')]),
    Pin("promote_refused", promotion_tests("all_met_lawful_and_the_verb_signs", "veto_subject_is_exact",
                                         "short_tree_criterion_alone_prevents_signing", "stop_ratio_alone_prevents_signing",
                                         "map_printed_and_each_required_hand_row_refuses", "live_e_not_replaced_by_green_regression_run"), [
        Mutant("promotion_check_dropped", "tools/jack",
               '        lines == [f"promote {a.subject}: lawful"] or refuse("\\n".join(lines) or "status returned no promotion verdict")', '        pass'),
        Mutant("regression_run_for_live_E", "tools/status.py", 's["E"] >= 20 and s["promotion_E"] >= 20', 'verified')]),
    Pin("run_verified", promotion_tests("all_met_lawful_and_the_verb_signs", "run_verified_each_field_and_no_signing"), [
        Mutant("any_run_accepted", "tools/status.py",
               'return isinstance(run, dict) and all(run.get(k) == v for k, v in (',
               'return isinstance(run, dict) and all(True or run.get(k) == v for k, v in ('),
        Mutant("event_unchecked", "tools/status.py", '("event", "push"), ', '')]),
    Pin("escalated", W1_TEST, [
        Mutant("escalation_silent", "tools/clerk.py", 'f" ESCALATED to {w[\'sovereign\']}"', '""')]),
    Pin("wealth_arithmetic", clerk_tests("exact_prequential_wealth"), [
        Mutant("p0_reestimated", "tools/status.py", '    result, successes, capital = [], 0, Fraction(1)',
               '    items = list(items)\n    P0 = Fraction(sum(i["Y"] for i in items) + 1, len(items) + 2)\n'
               '    result, successes, capital = [], 0, Fraction(1)')]),
    Pin("item_before_open", clerk_tests("window_and_same_timestamp_opening"), [
        Mutant("preopening_counted", "tools/status.py", 'if typ == "forecast" and seq > after_seq:', 'if typ == "forecast":')]),
    Pin("item_is_batch", clerk_tests("batch_is_not_a_count_of_resolutions"), [
        Mutant("resolutions_counted_singly", "tools/status.py", BATCH,
               '            for member in sorted(pending):\n                finalise(e, "batch", [member], not royal)')]),
    Pin("regroup_scored_items", clerk_tests("evidence_reuse_cannot_regroup_scored_items"), [
        Mutant("evidence_component_regrouping", "tools/status.py", '"Y": int(success and not repairs)})',
               '"Y": int(success and not repairs)})\n' + REGROUP)]),
    Pin("expired_writ_zero", clerk_tests("expiry_precedes_own_resolution_and_expired_only_merge", "mixed_batch_keeps_only_fresh_writs",
                                        "expiry_ties_in_forecast_order", "batch_is_not_a_count_of_resolutions"), [
        Mutant("late_resolution_success", "tools/status.py", 'if forecast["body"]["resolves_by"] < e["ts"]:',
               'if forecast["body"]["resolves_by"] < e["ts"] and not (e["type"] == "resolution" and e["body"]["forecast"] == f):'),
        Mutant("empty_batch_success", "tools/status.py", 'if typ == "merge" and pending:', 'if typ == "merge":')]),
    Pin("repair_erased_from_success", clerk_tests("repair_subject_never_narrows_taint"), [
        Mutant("repair_predicate_dropped", "tools/status.py", '"Y": int(success and not repairs)', '"Y": int(success)')]),
    Pin("repair_taints_all_open", clerk_tests("repair_subject_never_narrows_taint"), [
        Mutant("named_subject_only", "tools/status.py", TAINT,
               '            named = [(f, rs) for f, rs in opened.values() if f["body"]["claim"] == body.get("subject")]\n'
               '            for _, repairs in named or opened.values():\n                repairs.append(seq)'),
        OLDEST_TAINT]),
    Pin("replay_merge_110", clerk_tests("real_prefix_and_semantic_twin"), [OLDEST_TAINT]),
    Pin("late_report_immutable", lambda root: (
        clerk_tests("late_report_never_changes_prior_items_stakes_or_wealth")(root),
        promotion_tests("all_met_lawful_and_the_verb_signs", "late_report_line_refuses_without_revising_any_bet")(root)), [
        Mutant("finalised_item_revised", "tools/status.py", '                late_reports.append(seq)',
               '                late_reports.append(seq)\n                for item in items:\n'
               '                    if body.get("subject") in map(str, item["forecasts"]):\n                        item["Y"] = 0'),
        Mutant("late_report_line_omitted", "tools/status.py", '        checks.append((n == 0, f"late-reported repairs: {n}"))', '        pass')]),
    Pin("sovereign_resolution_zero", clerk_tests("sovereign_resolution_and_merge_are_zero", "batch_is_not_a_count_of_resolutions"), [
        Mutant("sovereign_completion_as_herald", "tools/status.py", '        royal = signer_blob(e) in sovereign',
               '        royal = signer_blob(e) in sovereign and typ not in ("resolution", "merge")')]),
    Pin("window_from_the_promote", clerk_tests("window_and_same_timestamp_opening"), [
        Mutant("latest_decision_opens", "tools/status.py",
               'opening = next(e for e in es if e["type"] == "decision" and\n                   promotes(e, "C1a"))',
               'opening = next(e for e in reversed(es) if e["type"] == "decision")'),
        Mutant("latest_counsel_forecast_ends", "tools/status.py",
               'l0 = next(e for e in es if e["seq"] < opening["seq"] and e["type"] == "forecast" and\n'
               '              e["proposer"] == "counsel" and e["body"].get("args", {}).get("id") == "L0")',
               'l0 = next(e for e in reversed(es) if e["type"] == "forecast" and e["proposer"] == "counsel")')]),
    Pin("evidence_unhashed", status_tests("counts_ratio_and_evidence", "evidence_must_hash"), [
        Mutant("rehash_skipped", "tools/status.py", 'hashlib.sha256(tree_bytes(root, rev, path)).hexdigest() == ev[7:]',
               'tree_bytes(root, rev, path) is not None')]),
    Pin("ratio_misclassified", status_tests("counts_ratio_and_evidence", "resolution_ratio_follows_its_forecasts_type"), [
        Mutant("world_resolution_procedure", "tools/status.py",
               'or (e["type"] == "resolution" and e["body"]["forecast"] in world))', ')')]),
    Pin("flooding_bounded", clerk_tests("w1_from_entry_strict_deadline_holders_and_discharge", "flood_and_byte_identical_projection"), [
        Mutant("deduplicated_by_claim", "tools/clerk.py", W1_OPEN,
               W1_OPEN[:-1] + ' and not any(es[w["seq"]]["body"]["claim"] == e["body"]["claim"] for w in writs):')]),
    Pin("veto_c1b", promotion_tests("veto_subject_is_exact"), [
        Mutant("veto_subject_ignored", "tools/status.py", 'and e["body"].get("subject") == subject for e in prefix)', 'for e in prefix)')]),
    Pin("map_printed", promotion_tests("map_printed_and_each_required_hand_row_refuses"), [
        Mutant("hand_row_passes", "tools/status.py", 'mapping.get(k, {}).get("enforcer", "").startswith("code:")',
               'mapping.get(k, {}).get("enforcer", "").startswith(("code:", "hand:"))')]),
]
PINS += C1B_PINS
