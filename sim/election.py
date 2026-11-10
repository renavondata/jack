"""Kernel-valid election attacks and their honest twins, using throwaway keys."""
import json

from harness import build
from tools import elect

OPEN = "2026-01-01T00:00:00Z"
W0 = "2026-01-01T01:00:00Z"
DRAW = "2026-01-01T00:15:00Z"


def entries(lg):
    return list(map(json.loads, lg.lines))


def setup(pool):
    lg = build.Log()
    decls = [build.decl("guy-master", "guy", pool.guy, build.ALL),
             build.decl("herald-2", "herald", pool.bob, ["forecast"]),
             build.decl("reviewer-2", "reviewer", pool.ann, ["forecast", "resolution"]),
             build.decl("builder-2", "builder", pool.stranger, ["forecast", "resolution"])]
    lg.add("genesis", "guy", build.genesis_body(decls), pool.guy, ts=OPEN)
    # X7 must be counsel's: re-declare an id prospectively, retaining its ownership.
    lg.add("key", "guy", build.decl("reviewer-2", "counsel", pool.ann, ["forecast", "resolution"]), pool.guy, ts=OPEN)
    lg.add("forecast", "counsel", dict(claim="X7", p=500, type="counsel.programme",
           args={"id": "X7"}, resolves_by=elect.later(OPEN, 336)), pool.ann, ts=OPEN)
    lg.add("key", "guy", decls[2], pool.guy, ts=OPEN)
    lg.add("decision", "guy", dict(kind="promote", subject="C2a"), pool.guy, ts=OPEN)
    lg.add("push", "guy", dict(digest="1" * 64, review="0" * 64), pool.guy, ts=OPEN)
    return lg


def body(lg, pool, W=W0, when=DRAW):
    es = entries(lg)
    rounds, errors = elect.audit(es, elect.verify_sigma)
    assert not errors, errors
    sigma = elect.sign_sigma(pool.bob.path, elect.round_string("freshness", W))
    return elect.invite_body(es, rounds, "freshness", W, when, sigma)


def add_invite(lg, pool, b=None, when=DRAW, who="herald"):
    key = pool.bob if who == "herald" else pool.ann
    lg.add("forecast", who, b or body(lg, pool, when=when), key, ts=when)
    return entries(lg)[-1]


def feedback(lg, pool, f, count=6, p=999, when="2026-01-01T02:10:00Z"):
    a = f["body"]["args"]
    fk = pool.ann if a["principal"] == "reviewer" else pool.stranger
    rk = pool.stranger if a["principal"] == "reviewer" else pool.ann
    fs = []
    for dataset in elect.DATASETS:
        fs.append(len(lg.lines))
        args = dict(stream="freshness", dataset=dataset, window_utc=a["window_utc"], model=a["model"], invite=f["seq"])
        lg.add("forecast", a["principal"], dict(claim=dataset, p=p, type="world.renavon", args=args,
               resolves_by=f["body"]["resolves_by"]), fk, ts=elect.later(a["window_utc"][0], -0.5))
    for target in fs[:count]:
        lg.add("resolution", elect.resolver(f), dict(forecast=target, outcome=1, evidence="saved public page"), rk, ts=when)


def attack(pool, kind, variant="gains", twin=False):
    lg = setup(pool)
    b = body(lg, pool)
    if kind == "self_invite":
        f = add_invite(lg, pool, b, who="herald" if twin else "reviewer")
    elif variant == "later_prefix":
        first = add_invite(lg, pool, b)
        feedback(lg, pool, first)
        b = body(lg, pool, elect.later(W0, 4), "2026-01-01T04:15:00Z")
        if not twin:
            lg.lines = lg.lines[:first["seq"] + 1]
        f = add_invite(lg, pool, b, when="2026-01-01T04:15:00Z" if twin else "2026-01-01T00:20:00Z")
        if not twin:
            feedback(lg, pool, first)
    else:
        if not twin and variant == "gains":
            b["args"]["gains"][0] = "1"
        if not twin and variant == "sigma":
            sigma = elect.sign_sigma(pool.stranger.path, elect.round_string("freshness", W0))
            b = elect.invite_body(entries(lg), [], "freshness", W0, DRAW, sigma)
        f = add_invite(lg, pool, b)
    return lg, f["seq"]
