"""Stratified Datalog over tagged atoms: rules are data (CHARTER §3 Change, §9.2).

A rule is a list of clauses {"head": literal, "body": [literal]}; a literal is
["pred", arg...] or ["not", literal]; "?Name" is a variable, "?_..." an
anonymous one (each occurrence distinct). Semantics: least model, stratum by
stratum, negation as failure on completed lower strata (Ceri, Gottlob & Tanca
1989). No built-ins at C0.
"""
import itertools
import re

from .log import Refuse, atom

BASE = {"entry": 3, "ts": 2, "field": 3, "key": 3, "signed_by": 2, "rule": 2, "repealed": 2, "candidate": 1}
VAR = re.compile(r"\?[A-Za-z_][A-Za-z0-9_]*")
HELPER = re.compile(r"[a-z0-9_-]{1,64}\.[a-z0-9_]+")


def _arg(a, fresh):
    if isinstance(a, str) and a.startswith("?"):
        if not VAR.fullmatch(a):
            raise Refuse("rule_malformed", f"bad variable {a}")
        return ("v", f"_{next(fresh)}") if a.startswith("?_") else ("v", a[1:])
    if isinstance(a, (list, dict)):
        raise Refuse("rule_malformed", "nested argument")
    return atom(a)


def _literal(lit, fresh, neg=False):
    """JSON literal → (negated, predicate, args) with arity and name checks."""
    if not (isinstance(lit, list) and lit and isinstance(lit[0], str)):
        raise Refuse("rule_malformed", "literal shape")
    if lit[0] == "not":
        if neg or len(lit) != 2:
            raise Refuse("rule_malformed", "negation")
        return _literal(lit[1], fresh, True)
    pred, args = lit[0], tuple(_arg(a, fresh) for a in lit[1:])
    arity = BASE.get(pred, 2 if pred == "violation" else None)
    if (arity is None and not HELPER.fullmatch(pred)) or (arity is not None and len(args) != arity):
        raise Refuse("rule_malformed", f"predicate {pred}/{len(args)}")
    return neg, pred, args


def compile_rule(rule_id, clauses):
    """Validate a rule body's clauses; returns ((head_pred, head_args), body) tuples."""
    if not (isinstance(clauses, list) and clauses):
        raise Refuse("rule_malformed", "clauses must be a non-empty list")
    fresh, out = itertools.count(), []
    for c in clauses:
        if not (isinstance(c, dict) and set(c) == {"head", "body"} and isinstance(c["body"], list)):
            raise Refuse("rule_malformed", "clause shape")
        neg, pred, args = _literal(c["head"], fresh)
        own = args[1] == atom(rule_id) if pred == "violation" else pred.startswith(rule_id + ".")
        if neg or not own:
            raise Refuse("rule_malformed", f"head {pred} is not this rule's")
        body = tuple(_literal(lit, fresh) for lit in c["body"])
        bound = {a for n, _, bargs in body if not n for a in bargs if a[0] == "v"}
        needed = ({a for a in args if a[0] == "v"}
                  | {a for n, _, bargs in body if n for a in bargs if a[0] == "v" and not a[1].startswith("_")})
        if not needed <= bound:
            raise Refuse("rule_malformed", "unsafe variable")
        out.append(((pred, args), body))
    return tuple(out)


def stratify(clauses):
    """Group clauses by stratum of their head; Refuse if negation is cyclic."""
    stratum = {head[0]: 0 for head, _ in clauses}
    for _ in range(len(stratum) + 1):
        changed = False
        for (pred, _), body in clauses:
            for neg, q, _ in body:
                need = stratum.get(q, 0) + (1 if neg and q in stratum else 0)
                if need > stratum[pred]:
                    stratum[pred], changed = need, True
        if not changed:
            return [[c for c in clauses if stratum[c[0][0]] == s]
                    for s in range(max(stratum.values(), default=-1) + 1)]
    raise Refuse("unstratifiable")


def _unify(args, row, subst):
    s = dict(subst)
    for a, v in zip(args, row):
        if a[0] == "v" and a[1] not in s:
            s[a[1]] = v
        elif (s[a[1]] if a[0] == "v" else a) != v:
            return None
    return s


def _matches(pred, args, subst, facts):
    return [s for row in facts.get(pred, ()) if len(row) == len(args)
            and (s := _unify(args, row, subst)) is not None]


def _join(body, facts):
    substs = [{}]
    for neg, pred, args in body:
        if neg:
            substs = [s for s in substs if not _matches(pred, args, s, facts)]
        else:
            substs = [s2 for s in substs for s2 in _matches(pred, args, s, facts)]
    return substs


def evaluate(clauses, facts):
    """Least model of clauses over base facts; returns {pred: {row}} including the base."""
    facts = {p: set(rows) for p, rows in facts.items()}
    for stratum in stratify(clauses):
        changed = True
        while changed:
            changed = False
            for (pred, args), body in stratum:
                rel = facts.setdefault(pred, set())
                new = {tuple(s[a[1]] if a[0] == "v" else a for a in args) for s in _join(body, facts)} - rel
                if new:
                    rel |= new
                    changed = True
    return facts
