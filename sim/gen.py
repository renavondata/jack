"""Seeded simulator: a generator for every attack in CHARTER §6 and for benign entries.

Each case carries the verdict the generator intends (its oracle). The oracle is
an independent account of the law for the restricted family of rules the
simulator writes (rules that forbid proposal titles); it never calls the kernel.
Not kernel.
"""
import random
from collections import namedtuple

from harness import build, keys
from harness.build import ALL, decl, proposal, rule_body, witness
from kernel import log, sig  # canonical form, hashes and SSHSIG parsing, to craft lines; the oracle is independent

Case = namedtuple("Case", "seed kind lines expected")
KINDS = ("benign", "retroactive", "vacuous", "impossible", "orphaning", "forged", "rewriting", "forking",
         "unattributed", "unsigned_change", "self_judging", "stalling", "flooding", "lapse", "breach",
         "unstratifiable", "malformed_rule", "duplicate_rule", "unknown_repeal", "schema", "structure")
TITLES = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta")
SAT = "ok"          # the satisfying title no benign rule ever forbids
SPARE = "spare"     # a proposal title no rule ever forbids, so a free title always exists
RETRO = "retro"     # the title the retroactive case proposes and then forbids
CHECKER = "33" * 32  # the checker digest genesis records in simulated logs


class KeyPool:
    """Throwaway keys for one run: guy (all powers), ann (proposal), bob (granted later), stranger."""

    def __init__(self, tmpdir):
        self.guy, self.ann = keys.make_key(tmpdir, "guy"), keys.make_key(tmpdir, "ann")
        self.bob, self.stranger = keys.make_key(tmpdir, "bob"), keys.make_key(tmpdir, "stranger")
        self.decls = [decl("guy-master", "guy", self.guy, ALL), decl("ann-1", "ann", self.ann, ["proposal"])]


class Model:
    """The oracle's account of the law in force (rules of the form 'forbid these titles')."""

    def __init__(self):
        self.rules, self.used, self.lapse, self.proposals, self.bob = {}, set(), [], [], None
        self.signers = []  # key that signed each line

    def forbidden(self, except_=None):
        return {t for rid, (_, f, _) in self.rules.items() if rid != except_ for t in f}

    def rule_for(self, title):
        return min((rid for rid, (_, f, _) in self.rules.items() if title in f), key=lambda r: self.rules[r][0])

    def change(self, n):
        remaining = dict(sorted(self.rules.items(), key=lambda kv: kv[1][0]))
        for rid, (_, _, viol) in list(remaining.items()):
            others = {r: v for r, v in remaining.items() if r != rid}
            if all(any(t in f for _, f, _ in others.values()) for t in viol):
                self.lapse.append([n, rid])
                remaining = others


def W(title, type_="proposal"):
    return witness(type_, "p", proposal(title))


def forbid(rid, titles, viol, sat=SAT, **kw):
    return rule_body(rid, build.forbid_title(rid, *titles), [W(t) for t in viol], [W(sat)], **kw)


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

    def new_rid(self):
        rid = f"r{len(self.model.used)}"
        self.model.used.add(rid)
        return rid

    def free_title(self):
        return self.rng.choice([t for t in TITLES + (SPARE,) if t not in self.model.forbidden()])

    # --- benign steps -------------------------------------------------------
    def step_proposal(self, who="ann"):
        key = self.pool.ann if who == "ann" else self.pool.bob
        self.model.proposals.append(self.n)
        self.add("proposal", who, proposal(self.free_title()), key)

    def step_rule(self, titles=None):
        titles = titles or self.rng.sample(TITLES, self.rng.randint(1, 2))
        rid = self.new_rid()
        viol = (self.rng.choice(titles),)
        self.model.rules[rid] = (self.n, frozenset(titles), viol)
        self.add("rule", "guy", forbid(rid, titles, viol), self.pool.guy)
        self.model.change(self.n - 1)

    def step_repeal(self):
        rid = self.rng.choice(sorted(self.model.rules))
        del self.model.rules[rid]
        self.add("repeal", "guy", {"rule_id": rid}, self.pool.guy)
        self.model.change(self.n - 1)

    def step_key(self):
        powers = [] if self.model.bob else ["proposal"]
        self.model.bob = set(powers)
        self.add("key", "guy", decl("bob-1", "bob", self.pool.bob, powers), self.pool.guy)

    def step_merge(self, checker=CHECKER):
        self.add("merge", "guy", build.merge(self.rng.choice(self.model.proposals), checker), self.pool.guy)

    def step(self):
        menu = [self.step_proposal, self.step_rule, self.step_key]
        if self.model.rules:
            menu.append(self.step_repeal)
        if self.model.proposals:
            menu.append(self.step_merge)
        if self.model.bob:
            menu.append(lambda: self.step_proposal("bob"))
        self.rng.choice(menu)()

    def prefix(self, lo=0, hi=5):
        for _ in range(self.rng.randint(lo, hi)):
            self.step()

    # --- verdicts -----------------------------------------------------------
    def ok(self):
        return {"ok": True, "entries": self.n, "lapse": list(self.model.lapse)}

    def refused(self, reason, seq=None, rule=None):
        return {"ok": False, "seq": self.n - 1 if seq is None else seq, "rule": rule, "reason": reason}

    def ensure_rule(self):
        if not self.model.rules:
            self.step_rule()


def generate_kind(kind, rng, pool):
    s = Sim(rng, pool)
    m, lg = s.model, s.lg
    s.prefix()
    if kind == "benign":
        s.step()
        return Case(None, kind, lg.lines, s.ok())
    if kind == "retroactive":
        s.add("proposal", "ann", proposal(RETRO), pool.ann)
        m.proposals.append(s.n - 1)
        s.step_rule([RETRO])
        s.step_proposal()
        return Case(None, kind, lg.lines, s.ok())
    if kind == "vacuous":
        a, b = rng.sample(TITLES, 2)
        s.add("rule", "guy", forbid("rx", [a], [b]), pool.guy)
        return Case(None, kind, lg.lines, s.refused("vacuous_rule"))
    if kind == "impossible":
        a = rng.choice(TITLES)
        sat = a if not m.forbidden() or rng.random() < 0.5 else rng.choice(sorted(m.forbidden()))
        s.add("rule", "guy", forbid("rx", [a], [a], sat=sat), pool.guy)
        return Case(None, kind, lg.lines, s.refused("impossible_rule"))
    if kind == "orphaning":
        s.ensure_rule()
        s.add("rule", "guy", forbid("rx", [SAT], [SAT], sat="ok2"), pool.guy)
        return Case(None, kind, lg.lines, s.refused("orphans_rule"))
    if kind == "forged":
        variant = rng.choice(("tamper", "stranger", "malleate"))
        if variant == "stranger":
            s.add("proposal", "ann", proposal(s.free_title()), pool.stranger)
            return Case(None, kind, lg.lines, s.refused("unknown_key"))
        s.add("proposal", "ann", proposal(s.free_title()), pool.ann)
        e = log.parse_line(lg.lines[-1])
        if variant == "tamper":
            e["body"]["title"] = e["body"]["title"] + "!"
        else:
            _, sig64 = sig.parse_sshsig(e["sig"])
            e["sig"] = keys.rewrap(e["sig"], sig64=sig64[:32] + (int.from_bytes(sig64[32:], "little") + sig.L).to_bytes(32, "little"))
        lg.lines[-1] = log.canonical(e)
        return Case(None, kind, lg.lines, s.refused("bad_signature"))
    if kind == "rewriting":
        i = rng.randrange(s.n)
        e = log.parse_line(lg.lines[i])
        e["body"]["charter" if e["type"] == "genesis" else "note"] = "ab" * 32 if e["type"] == "genesis" else "edited"
        if i < s.n - 1 and rng.random() < 0.5:
            del e["sig"]
            lg.lines[i] = build.make_entry(i, e["parent"], e["type"], e["proposer"], e["body"], m.signers[i], ts=e["ts"])
            return Case(None, kind, lg.lines, s.refused("parent_mismatch", seq=i + 1))
        lg.lines[i] = log.canonical(e)
        return Case(None, kind, lg.lines, s.refused("bad_signature", seq=i))
    if kind == "forking":
        parent = rng.choice([log.GENESIS_PARENT] + [log.line_hash(l) for l in lg.lines[:-1]])
        lg.lines.append(build.make_entry(s.n, parent, "proposal", "ann", proposal(s.free_title()), pool.ann))
        return Case(None, kind, lg.lines, s.refused("parent_mismatch"))
    if kind == "unattributed":
        if rng.random() < 0.5:
            s.add("proposal", "", proposal(s.free_title()), pool.ann)
            return Case(None, kind, lg.lines, s.refused("no_proposer"))
        s.add("proposal", "guy", proposal(s.free_title()), pool.ann)
        return Case(None, kind, lg.lines, s.refused("proposer_mismatch"))
    if kind == "unsigned_change":
        variant = rng.choice(("rule", "repeal", "key"))
        body = {"rule": forbid("rx", ["alpha"], ["alpha"]), "repeal": {"rule_id": "r0"},
                "key": decl("x", "ann", pool.stranger, ["proposal"])}[variant]
        s.add(variant, "ann", body, pool.ann)
        return Case(None, kind, lg.lines, s.refused("no_power"))
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
    if kind == "lapse":
        a, b = rng.sample(TITLES, 2)
        s.step_rule([a])
        s.step_rule([a, b])
        return Case(None, kind, lg.lines, s.ok())
    if kind == "breach":
        s.ensure_rule()
        t = rng.choice(sorted(m.forbidden()))
        s.add("proposal", "ann", proposal(t), pool.ann)
        return Case(None, kind, lg.lines, s.refused("violation", rule=m.rule_for(t)))
    if kind == "unstratifiable":
        clauses = [{"head": ["rx.a", "?S"], "body": [["candidate", "?S"], ["not", ["rx.b", "?S"]]]},
                   {"head": ["rx.b", "?S"], "body": [["candidate", "?S"], ["not", ["rx.a", "?S"]]]},
                   {"head": ["violation", "?S", "rx"], "body": [["rx.a", "?S"]]}]
        s.add("rule", "guy", rule_body("rx", clauses, [W("alpha")], [W(SAT)]), pool.guy)
        return Case(None, kind, lg.lines, s.refused("unstratifiable"))
    if kind == "malformed_rule":
        bad = rng.choice((rule_body("rx", build.forbid_title("ry", "alpha"), [W("alpha")], [W(SAT)]),
                          rule_body("rx", build.forbid_title("rx", "alpha"), [], [W(SAT)]),
                          rule_body("rx", build.forbid_title("rx", "alpha"), [witness("proposal", "p", {"title": "alpha"})], [W(SAT)]),
                          rule_body("rx", [{"head": ["violation", "?S", "rx"], "body": [["entry", "?S", "proposal"]]}], [W("alpha")], [W(SAT)])))
        s.add("rule", "guy", bad, pool.guy)
        return Case(None, kind, lg.lines, s.refused("rule_malformed"))
    if kind == "duplicate_rule":
        s.ensure_rule()
        rid = rng.choice(sorted(m.used))
        s.add("rule", "guy", forbid(rid, ["alpha"], ["alpha"]), pool.guy)
        return Case(None, kind, lg.lines, s.refused("duplicate_rule"))
    if kind == "unknown_repeal":
        s.add("repeal", "guy", {"rule_id": "never"}, pool.guy)
        return Case(None, kind, lg.lines, s.refused("unknown_rule"))
    if kind == "schema":
        if rng.random() < 0.5:
            s.add("proposal", "ann", {"title": "no commit"}, pool.ann)
        else:
            s.add("merge", "guy", {"proposal": 1, "commit": build.HEX40, "checker": "nothex"}, pool.guy)
        return Case(None, kind, lg.lines, s.refused("schema"))
    if kind == "structure":
        variant = rng.choice(("bad_seq", "not_canonical", "malformed_json", "genesis_misplaced"))
        if variant == "genesis_misplaced":
            s.add("genesis", "guy", build.genesis_body(pool.decls, checker=CHECKER), pool.guy)
            return Case(None, kind, lg.lines, s.refused("genesis_misplaced"))
        line = build.make_entry(s.n + (variant == "bad_seq"), lg.head, "proposal", "ann", proposal(s.free_title()), pool.ann)
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
