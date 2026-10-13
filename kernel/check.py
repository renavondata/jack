"""The validity predicate: check(log) → ok | (seq, rule, reason). CHARTER §3, §9.3.

Entry i is judged by the law admitted before i: the keys and rules declared by
entries 0..i-1 (genesis certifies itself). Pure: no I/O except in main().
"""
import json
import sys
from collections import namedtuple

from . import datalog, log, sig
from .log import Refuse, atom, untag

Key = namedtuple("Key", "principal blob powers")
Rule = namedtuple("Rule", "seq clauses violating satisfying")
State = namedtuple("State", "head keys rules used facts")
EMPTY = State(log.GENESIS_PARENT, {}, {}, frozenset(), {})
CHANGE = ("rule", "repeal")


def _union(*facts):
    out = {}
    for f in facts:
        for pred, rows in f.items():
            out.setdefault(pred, set()).update(rows)
    return out


def entry_facts(seq, type_, proposer, body, ts=None):
    """Base facts contributed by one entry (or one witness, as a virtual entry)."""
    f = {"entry": {(atom(seq), atom(type_), atom(proposer))},
         "field": {(atom(seq), atom(p), atom(v)) for p, v in log.flatten(body)}}
    return _union(f, {"ts": {(atom(seq), atom(ts))}}) if ts is not None else f


def law_facts(state, extra, candidate):
    """Everything a rule may see when entry `candidate` is judged."""
    keys = {(atom(k), atom(d.principal), atom(p)) for k, d in state.keys.items() for p in d.powers}
    return _union(state.facts, {"key": keys, "candidate": {(atom(candidate),)}}, extra)


def in_force(state):
    return sorted(state.rules.items(), key=lambda kv: kv[1].seq)


def violations(rules, facts):
    """{(seq, rule_id)} derived by `rules` (an iterable of (id, Rule)) over `facts`."""
    derived = datalog.evaluate([c for _, r in rules for c in r.clauses], facts)
    return {(untag(s), untag(r)) for s, r in derived.get("violation", ())}


def signer(e, keys):
    """Recognition (b): which declared key signed e, with power for its type."""
    try:
        blob, sig64 = sig.parse_sshsig(e["sig"])
    except ValueError as x:
        raise Refuse("bad_signature", f"sshsig: {x}") from None
    key_id = next((k for k, d in keys.items() if d.blob == blob), None)
    if key_id is None:
        raise Refuse("unknown_key")
    if keys[key_id].principal != e["proposer"]:
        raise Refuse("proposer_mismatch", f"key {key_id} belongs to {keys[key_id].principal}")
    if e["type"] not in keys[key_id].powers:
        raise Refuse("no_power", f"key {key_id} may not sign {e['type']}")
    message = log.canonical({k: v for k, v in e.items() if k != "sig"}).encode("utf-8")
    if not sig.verify(message, blob, sig64):
        raise Refuse("bad_signature")
    return key_id


def declare(keys, d):
    blob = log.pubkey_blob(d["pubkey"])
    for kid, k in keys.items():
        if k.blob == blob and kid != d["key_id"]:
            raise Refuse("schema", f"pubkey already declared as {kid}")
    return {**keys, d["key_id"]: Key(d["principal"], blob, frozenset(d["powers"]))}


def check_witness(w):
    ok = (isinstance(w, dict) and {"type", "proposer", "body"} <= set(w) <= {"type", "proposer", "body", "ts"}
          and w["type"] in log.TYPES and isinstance(w["proposer"], str) and w["proposer"]
          and isinstance(w["body"], dict) and ("ts" not in w or log.TS.fullmatch(str(w["ts"]))))
    if not ok:
        raise Refuse("rule_malformed", "witness shape")
    try:
        log.check_body(w["type"], w["body"])
    except Refuse as x:
        raise Refuse("rule_malformed", f"witness body: {x.detail}") from None
    return w


def witness_list(ws, what):
    if not (isinstance(ws, list) and ws):
        raise Refuse("rule_malformed", f"{what}: need a non-empty list of witnesses")
    return tuple(check_witness(w) for w in ws)


def passes(state, rules, m, w):
    """Does witness w, as the virtual entry m, draw no violation under `rules`?"""
    facts = law_facts(state, entry_facts(m, w["type"], w["proposer"], w["body"], w.get("ts")), m)
    return not any(s == m for s, _ in violations(rules, facts))


def admit_rule(state, n, body):
    """Rule admissibility (§9.3): witnesses, replacements, weak non-contradiction."""
    rid, m = body["rule_id"], n + 1
    if rid in state.used:
        raise Refuse("duplicate_rule")
    rule = Rule(n, datalog.compile_rule(rid, body["clauses"]),
                witness_list(body["witnesses"]["violating"], "violating"),
                witness_list(body["witnesses"]["satisfying"], "satisfying"))
    repl = {t: witness_list(ws, f"replacements.{t}") for t, ws in body.get("replacements", {}).items()}
    rules = {**state.rules, rid: rule}
    state = state._replace(rules=rules, used=state.used | {rid},
                           facts=_union(state.facts, {"rule": {(atom(rid), atom(n))}}))
    datalog.stratify([c for _, r in in_force(state) for c in r.clauses])
    law = in_force(state)
    for w in rule.violating:
        facts = law_facts(state, entry_facts(m, w["type"], w["proposer"], w["body"], w.get("ts")), m)
        if (m, rid) not in violations(law, facts):
            raise Refuse("vacuous_rule", "a violating witness is not violated by this rule")
    for w in rule.satisfying:
        if not passes(state, law, m, w):
            raise Refuse("impossible_rule", "a satisfying witness is violated")
    for target, ws in repl.items():
        if target not in rules:
            raise Refuse("rule_malformed", f"replacement for a rule not in force: {target}")
        if not all(passes(state, law, m, w) for w in ws):
            raise Refuse("impossible_rule", f"replacement witness for {target} is violated")
        rules[target] = rules[target]._replace(satisfying=rules[target].satisfying + ws)
    for qid, q in in_force(state):
        if not any(passes(state, law, m, w) for w in q.satisfying):
            raise Refuse("orphans_rule", f"no satisfying witness of {qid} passes the law with {rid}")
    return state


def lapse_candidates(state, n):
    """§3 Change, lapse: oldest first, one at a time, reported only."""
    remaining, out, m = in_force(state), [], n + 1
    for rid, r in list(remaining):
        others = [(q, rule) for q, rule in remaining if q != rid]
        if all(not passes(state, others, m, w) for w in r.violating):
            out.append([n, rid])
            remaining = others
    return out


def check_entry(state, i, line):
    """Recognition (a)(b)(c) then admissibility; returns (next state, lapse report)."""
    e = log.parse_line(line)
    log.check_shape(e)
    if e["seq"] != i:
        raise Refuse("bad_seq", f"expected {i}")
    if e["parent"] != state.head:
        raise Refuse("parent_mismatch")
    if (e["type"] == "genesis") != (i == 0):
        raise Refuse("genesis_misplaced")
    if e["proposer"] == "":
        raise Refuse("no_proposer")
    log.check_body(e["type"], e["body"])
    keys = state.keys
    if e["type"] == "genesis":
        for d in e["body"]["keys"]:
            keys = declare(keys, d)
    key_id = signer(e, keys)
    own = _union(entry_facts(i, e["type"], e["proposer"], e["body"], e["ts"]),
                 {"signed_by": {(atom(i), atom(key_id))}})
    hits = {r for s, r in violations(in_force(state), law_facts(state, own, i)) if s == i}
    if hits:
        raise Refuse("violation", rule=min(hits, key=lambda r: state.rules[r].seq))
    state = state._replace(head=log.line_hash(line), facts=_union(state.facts, own))
    if e["type"] == "key":
        keys = declare(keys, e["body"])
    if e["type"] == "repeal":
        rid = e["body"]["rule_id"]
        if rid not in state.rules:
            raise Refuse("unknown_rule", f"{rid} is not in force")
        rules = {k: v for k, v in state.rules.items() if k != rid}
        state = state._replace(rules=rules, facts=_union(state.facts, {"repealed": {(atom(rid), atom(i))}}))
    if e["type"] == "rule":
        state = admit_rule(state, i, e["body"])
    state = state._replace(keys=keys)
    return state, (lapse_candidates(state, i) if e["type"] in CHANGE else [])


def check(lines):
    """check(log) → {"ok": true, "entries", "lapse"} | {"ok": false, "seq", "rule", "reason", "detail"}."""
    state, lapse = EMPTY, []
    for i, line in enumerate(lines):
        try:
            state, new = check_entry(state, i, line)
        except Refuse as x:
            return {"ok": False, "seq": i, "rule": x.rule, "reason": x.reason, "detail": x.detail}
        lapse += new
    return {"ok": True, "entries": len(lines), "lapse": lapse}


def read_lines(data):
    """Split log bytes into lines; undecodable bytes become lone surrogates and fail parsing."""
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    return [l.decode("utf-8", "surrogateescape") for l in lines]


def main(argv):
    if len(argv) != 2:
        print("usage: python3 -m kernel.check <log.jsonl>", file=sys.stderr)
        return 2
    try:
        with open(argv[1], "rb") as f:
            data = f.read()
    except OSError as x:
        print(f"cannot read {argv[1]}: {x}", file=sys.stderr)
        return 2
    verdict = check(read_lines(data))
    print(json.dumps(verdict, sort_keys=True))
    return 0 if verdict["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
