"""Seeded simulator: a generator for every record attack in CHARTER §6 and for benign entries.

Each case carries the verdict the generator intends (its oracle). The oracle is
an independent account of the law at C0 — which keys hold which powers after
each entry — and never calls the kernel. The rule attacks of §6 (vacuous,
impossible) have no generator until the law language arrives in C1.
Not kernel.
"""
import random
from collections import namedtuple

from harness import build, keys
from harness.build import ALL, decl, proposal
from kernel import log, sig  # canonical form, hashes and SSHSIG parsing, to craft lines; the oracle is independent

Case = namedtuple("Case", "seed kind lines expected")
KINDS = ("benign", "retroactive", "forged", "rewriting", "forking", "unattributed", "unsigned_change", "revoked",
         "weak_key", "duplicate_key", "self_judging", "stalling", "flooding", "schema", "structure")
TITLES = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta")
CHECKER = "33" * 32  # the checker digest genesis records in simulated logs


class KeyPool:
    """Throwaway keys for one run: guy (all powers), ann (proposal), bob (granted later), stranger."""

    def __init__(self, tmpdir):
        self.guy, self.ann = keys.make_key(tmpdir, "guy"), keys.make_key(tmpdir, "ann")
        self.bob, self.stranger = keys.make_key(tmpdir, "bob"), keys.make_key(tmpdir, "stranger")
        self.decls = [decl("guy-master", "guy", self.guy, ALL), decl("ann-1", "ann", self.ann, ["proposal"])]


class Model:
    """The oracle's account of the law in force: key_id → (principal, powers); plus bookkeeping."""

    def __init__(self):
        self.keys = {"guy-master": ("guy", frozenset(ALL)), "ann-1": ("ann", frozenset({"proposal"}))}
        self.proposals, self.signers = [], []  # seqs of proposals; the key that signed each line

    def may(self, key_id, type_):
        return type_ in self.keys.get(key_id, ("", frozenset()))[1]


class Sim:
    def __init__(self, rng, pool):
        self.rng, self.pool, self.model, self.lg = rng, pool, Model(), build.Log()
        self.add("genesis", "guy", build.genesis_body(pool.decls, checker=CHECKER), pool.guy)

    def add(self, type_, proposer, body, key, **kw):
        self.model.signers.append(key)
        return self.lg.add(type_, proposer, body, key, ts=self.ts(), **kw)

    def ts(self):
        return f"2026-{self.rng.randint(1, 12):02}-{self.rng.randint(1, 28):02}T{self.rng.randint(0, 23):02}:00:00Z"

    @property
    def n(self):
        return len(self.lg.lines)

    def title(self):
        return self.rng.choice(TITLES)

    # --- benign steps -------------------------------------------------------
    def step_proposal(self, who="ann"):
        self.model.proposals.append(self.n)
        self.add("proposal", who, proposal(self.title()), self.pool.ann if who == "ann" else self.pool.bob)

    def step_key(self):
        """Grant bob the proposal power, or revoke it if he has it (the change rule at work)."""
        powers = [] if self.model.may("bob-1", "proposal") else ["proposal"]
        self.model.keys["bob-1"] = ("bob", frozenset(powers))
        self.add("key", "guy", decl("bob-1", "bob", self.pool.bob, powers), self.pool.guy)

    def grant_bob(self):
        if not self.model.may("bob-1", "proposal"):
            self.step_key()

    def revoke_bob(self):
        if self.model.may("bob-1", "proposal"):
            self.step_key()

    def step_merge(self, checker=CHECKER):
        self.add("merge", "guy", build.merge(self.rng.choice(self.model.proposals), checker), self.pool.guy)

    def step(self):
        menu = [self.step_proposal, self.step_key]
        if self.model.proposals:
            menu.append(self.step_merge)
        if self.model.may("bob-1", "proposal"):
            menu.append(lambda: self.step_proposal("bob"))
        self.rng.choice(menu)()

    def prefix(self, lo=0, hi=5):
        for _ in range(self.rng.randint(lo, hi)):
            self.step()

    # --- verdicts -----------------------------------------------------------
    def ok(self):
        return {"ok": True, "entries": self.n}

    def refused(self, reason, seq=None):
        return {"ok": False, "seq": self.n - 1 if seq is None else seq, "reason": reason}


def generate_kind(kind, rng, pool):
    s = Sim(rng, pool)
    m, lg = s.model, s.lg
    s.prefix()
    if kind == "benign":
        s.step()
        return Case(None, kind, lg.lines, s.ok())
    if kind == "retroactive":  # a checker applying the final keys to earlier entries would refuse bob's proposal
        s.grant_bob()
        s.step_proposal("bob")
        s.revoke_bob()
        s.step_proposal()
        return Case(None, kind, lg.lines, s.ok())
    if kind == "forged":
        variant = rng.choice(("tamper", "stranger", "malleate", "reserved"))
        if variant == "stranger":
            s.add("proposal", "ann", proposal(s.title()), pool.stranger)
            return Case(None, kind, lg.lines, s.refused("unknown_key"))
        s.add("proposal", "ann", proposal(s.title()), pool.ann)
        e = log.parse_line(lg.lines[-1])
        if variant == "tamper":
            e["body"]["title"] = e["body"]["title"] + "!"
        elif variant == "reserved":
            e["sig"] = keys.rewrap(e["sig"], reserved=rng.choice((b"\x00", b"x", b"\x00" * 4)))
        else:
            _, sig64 = sig.parse_sshsig(e["sig"])
            e["sig"] = keys.rewrap(e["sig"], sig64=sig64[:32] + (int.from_bytes(sig64[32:], "little") + sig.L).to_bytes(32, "little"))
        lg.lines[-1] = log.canonical(e)
        return Case(None, kind, lg.lines, s.refused("bad_signature"))
    if kind == "rewriting":
        i = rng.randrange(s.n)
        e = log.parse_line(lg.lines[i])
        if e["type"] == "key":  # a key declaration has exactly four members (SPEC §5): tamper a valid field instead
            e["ts"] = "2025-06-15T12:34:56Z"  # never generated (Sim.ts: 2026, :00:00)
        else:
            e["body"]["charter" if e["type"] == "genesis" else "note"] = "ab" * 32 if e["type"] == "genesis" else "edited"
        if i < s.n - 1 and rng.random() < 0.5:
            del e["sig"]
            lg.lines[i] = build.make_entry(i, e["parent"], e["type"], e["proposer"], e["body"], m.signers[i], ts=e["ts"])
            return Case(None, kind, lg.lines, s.refused("parent_mismatch", seq=i + 1))
        lg.lines[i] = log.canonical(e)
        return Case(None, kind, lg.lines, s.refused("bad_signature", seq=i))
    if kind == "forking":
        parent = rng.choice([log.GENESIS_PARENT] + [log.line_hash(l) for l in lg.lines[:-1]])
        lg.lines.append(build.make_entry(s.n, parent, "proposal", "ann", proposal(s.title()), pool.ann))
        return Case(None, kind, lg.lines, s.refused("parent_mismatch"))
    if kind == "unattributed":
        if rng.random() < 0.5:
            s.add("proposal", "", proposal(s.title()), pool.ann)
            return Case(None, kind, lg.lines, s.refused("no_proposer"))
        s.add("proposal", "guy", proposal(s.title()), pool.ann)
        return Case(None, kind, lg.lines, s.refused("proposer_mismatch"))
    if kind == "unsigned_change":
        body = rng.choice((decl("x", "ann", pool.stranger, ["proposal"]), decl("ann-1", "ann", pool.ann, ["proposal", "key"])))
        s.add("key", "ann", body, pool.ann)
        return Case(None, kind, lg.lines, s.refused("no_power"))
    if kind == "revoked":
        s.grant_bob()
        s.revoke_bob()
        s.add("proposal", "bob", proposal(s.title()), pool.bob)
        return Case(None, kind, lg.lines, s.refused("no_power"))
    if kind == "weak_key":
        name, pub32 = rng.choice(keys.weak_keys())
        eve = decl("eve-1", "eve", keys.fake_key(pub32), rng.choice(([], ["proposal"])))
        if rng.random() < 0.3:
            lg = build.Log()
            lg.add("genesis", "guy", build.genesis_body(pool.decls + [eve], checker=CHECKER), pool.guy)
            return Case(None, kind, lg.lines, {"ok": False, "seq": 0, "reason": "bad_key"})
        s.add("key", "guy", eve, pool.guy)
        return Case(None, kind, lg.lines, s.refused("bad_key"))
    if kind == "duplicate_key":
        s.grant_bob()
        twin = rng.choice((decl("ann-2", "ann", pool.ann, ["proposal"]), decl("bob-2", "bob", pool.bob, []),
                           decl("guy-2", "guy", pool.guy, ["merge"])))
        s.add("key", "guy", twin, pool.guy)
        return Case(None, kind, lg.lines, s.refused("bad_key"))
    if kind == "self_judging":
        if not m.proposals:
            s.step_proposal()
        s.step_merge(checker="ab" * 32)
        return Case(None, kind, lg.lines, s.ok())
    if kind == "stalling":
        for _ in range(rng.randint(2, 4)):
            s.step_proposal()
        return Case(None, kind, lg.lines, s.ok())
    if kind == "flooding":
        for _ in range(rng.randint(20, 35)):
            s.step()
        return Case(None, kind, lg.lines, s.ok())
    if kind == "schema":
        variant = rng.choice(("proposal", "merge", "key", "type"))
        if variant == "proposal":
            s.add("proposal", "ann", {"title": "no commit"}, pool.ann)
        elif variant == "merge":
            s.add("merge", "guy", {"proposal": 1, "commit": build.HEX40, "checker": "nothex"}, pool.guy)
        elif variant == "key":
            s.add("key", "guy", decl("bob-1", "bob", pool.bob, ["rule"]), pool.guy)
        else:
            s.add(rng.choice(("rule", "repeal")), "guy", {"rule_id": "r1"}, pool.guy)
        return Case(None, kind, lg.lines, s.refused("schema"))
    if kind == "structure":
        variant = rng.choice(("bad_seq", "not_canonical", "malformed_json", "genesis_misplaced"))
        if variant == "genesis_misplaced":
            s.add("genesis", "guy", build.genesis_body(pool.decls, checker=CHECKER), pool.guy)
            return Case(None, kind, lg.lines, s.refused("genesis_misplaced"))
        line = build.make_entry(s.n + (variant == "bad_seq"), lg.head, "proposal", "ann", proposal(s.title()), pool.ann)
        if variant == "not_canonical":
            line = line.replace(',"ts"', ', "ts"', 1)
        if variant == "malformed_json":
            line = line[:-3]
        lg.lines.append(line)
        return Case(None, kind, lg.lines, s.refused(variant))
    raise ValueError(kind)


def generate(seed_hex, pool):
    rng = random.Random(int(seed_hex, 16))
    case = generate_kind(rng.choice(KINDS), rng, pool)
    return case._replace(seed=seed_hex)
