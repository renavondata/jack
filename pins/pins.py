"""The pins (CHARTER §9): attack fixture, named mutant(s), passing twin. Data, run by pins/run.py.

Each test takes the root of the tree under test and runs that tree's checker or
judge as a subprocess, so the same fixtures run unchanged against the second
checker. Expectations are exact (seq, reason) or exact acceptance, so a mutant
cannot survive by failing for a different reason. C0 is the record only: the
rule pins of §9 (final_law_for_all, vacuous_rule_admitted,
impossible_rule_admitted, redundancy_unreported) return with the law language
in C1; unsigned_change reads over `key` entries, the change entries of C0.
"""
import functools
import glob
import os
import sys
import tempfile
from collections import namedtuple

from harness import build, diff, gitfix, keys, runner
from harness.build import proposal
from kernel import log, sig

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


# --- judge pins -------------------------------------------------------------

def t_trusted_path(root):
    w = world()
    for path in ("kernel/check.py", "judge/judge.py", "kernel2/check"):
        fx = gitfix.make_repo(w)
        gitfix.write(fx.repo, path, 'print(\'{"ok": true, "entries": 0}\')\n')
        gitfix.commit_all(fx.repo, "edit trusted file")
        r = judged(root, fx)
        assert (r.get("ok"), r.get("reason")) == (False, "trusted_path"), (path, r)
    fx = gitfix.make_repo(w)
    gitfix.write(fx.repo, "README.md", "docs only\n")
    gitfix.commit_all(fx.repo, "docs")
    assert judged(root, fx).get("ok") is True


def t_trusted_rename(root):
    w = world()
    for old, new in (("SPEC.md", "docs/SPEC.md"), ("CHARTER.md", "CHARTER.old.md"), ("kernel/sig.py", "kernel/sig_.py")):
        fx = gitfix.make_repo(w)
        gitfix.move(fx.repo, old, new)
        gitfix.commit_all(fx.repo, "rename")
        r = judged(root, fx)
        assert old not in r.get("touched", [old]), f"fixture: git must report the rename under its new name only: {r}"
        assert (r.get("ok"), r.get("reason")) == (False, "trusted_path"), (old, new, r)
    fx = gitfix.make_repo(w)
    gitfix.move(fx.repo, "README.md", "docs/README.md")
    gitfix.commit_all(fx.repo, "rename docs")
    assert judged(root, fx).get("ok") is True


def t_judge_from_proposal(root):
    from judge import judge as trunk_judge  # pristine, only to compute the fixture trunk's digest
    w = world()
    fx = gitfix.make_repo(w)
    fx.log.add("proposal", "ann", proposal("a"), w.ann)
    fx.log.add("merge", "guy", build.merge(1, "ab" * 32), w.guy)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    gitfix.commit_all(fx.repo, "merge judged by a checker the proposal supplied")
    r = judged(root, fx)
    assert (r.get("ok"), r.get("reason")) == (False, "judge_from_proposal"), r
    fx.log.lines.pop()
    fx.log.add("merge", "guy", build.merge(1, trunk_judge.digest(fx.repo, fx.main)), w.guy)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    gitfix.commit_all(fx.repo, "merge judged by trunk")
    assert judged(root, fx).get("ok") is True
    fx = gitfix.make_repo(w)
    fx.log.add("proposal", "ann", proposal("b"), w.ann)
    gitfix.write(fx.repo, "log.jsonl", fx.log.text())
    gitfix.commit_all(fx.repo, "proposal")
    assert judged(root, fx).get("ok") is True


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


def t_kernel2_runnable(root):
    """The judge runs trunk's kernel2 with git's file modes, so its launcher may call its own scripts."""
    fx = gitfix.make_repo(world())
    gitfix.git(fx.repo, "checkout", "-q", "main")
    gitfix.write(fx.repo, "kernel2/check", '#!/bin/sh\nexec "$(dirname "$0")/helper.sh" "$@"\n')
    gitfix.write(fx.repo, "kernel2/helper.sh", "#!/bin/sh\necho '{\"ok\":true,\"entries\":1}'\n")
    for name in ("check", "helper.sh"):
        os.chmod(os.path.join(fx.repo, "kernel2", name), 0o755)
    gitfix.commit_all(fx.repo, "kernel2 whose launcher calls a helper")
    r = runner.judge_with(root, fx.repo, "main", "main")
    assert r.get("ok") is True and r.get("kernel2") == {"ok": True, "entries": 1}, r


def t_selfcheck_blind(root):
    """The CI self-check fails when the judge cannot run kernel2, and passes when it can."""
    def repo(helper_mode):
        fx = gitfix.make_repo(world())
        gitfix.git(fx.repo, "checkout", "-q", "main")
        gitfix.write(fx.repo, "kernel2/check", '#!/bin/sh\nexec "$(dirname "$0")/helper.sh" "$@"\n')
        gitfix.write(fx.repo, "kernel2/helper.sh", "#!/bin/sh\necho '{\"ok\":true,\"entries\":1}'\n")
        os.chmod(os.path.join(fx.repo, "kernel2", "check"), 0o755)
        os.chmod(os.path.join(fx.repo, "kernel2", "helper.sh"), helper_mode)
        gitfix.commit_all(fx.repo, "kernel2")
        return fx.repo
    def run(r):
        import subprocess
        return subprocess.run([sys.executable, os.path.join(root, "judge", "selfcheck.py"), "--repo", r],
                              capture_output=True, text=True).returncode
    assert run(repo(0o644)) == 1, "self-check passed a trunk whose kernel2 cannot run"
    assert run(repo(0o755)) == 0, "self-check failed a healthy trunk"


def t_checker_drift(root):
    """Both checkers agree, verdict by verdict, on the pin fixtures (runs once kernel2/check exists)."""
    w = world()
    logs = [w.log().lines]
    lg = w.log(); lg.add("key", "guy", build.decl("stranger-1", "stranger", w.stranger, ["proposal"]), w.guy)
    lg.add("proposal", "stranger", proposal(), w.stranger); logs.append(list(lg.lines))
    lg = w.log(); lg.add("proposal", "guy", proposal(), w.stranger); logs.append(lg.lines)
    lg = w.log(); lg.add("proposal", "guy", proposal(), w.guy)            # body altered after signing
    e = log.parse_line(lg.lines[1]); e["body"]["title"] += "x"; logs.append([lg.lines[0], log.canonical(e)])
    with tempfile.TemporaryDirectory() as tmp:
        paths = sorted(glob.glob(os.path.join(root, "spec", "vectors", "logs", "*.jsonl")))  # every reason code
        for i, lines in enumerate(logs):
            paths.append(os.path.join(tmp, f"{i}.jsonl"))
            with open(paths[-1], "w") as f:
                f.write("".join(l + "\n" for l in lines))
        bad = diff.compare([sys.executable, "-E", "-s", "-m", "kernel.check"], [os.path.join(root, "kernel2", "check")], paths)
    assert not bad, bad


GUARD = 'if digest(repo, head) != report["trusted_digest"] or show(repo, head, CHARTER) != show(repo, trunk, CHARTER):'

PINS = [
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
    Pin("kernel2_unrunnable", t_kernel2_runnable, [
        Mutant("modes_ignored", "judge/judge.py", "                os.chmod(dest, 0o755)", "                pass")]),
    Pin("selfcheck_blind", t_selfcheck_blind, [
        Mutant("judge_errors_ignored", "judge/selfcheck.py",
               "        return 1  # selfcheck: judge refused or failed", "        return 0")]),
    Pin("checker_drift", t_checker_drift, [
        Mutant("reason_code_flipped", "kernel2/check", "bad_signature", "bad_signatur3")]),
]
