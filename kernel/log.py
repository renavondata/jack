"""Log format: canonical JSON, line hashes, entry shape, body schemas, facts.

CHARTER §9.1. Pure functions; no I/O, no clock.
"""
import base64
import hashlib
import json
import re

TYPES = ("genesis", "key", "rule", "repeal", "proposal", "merge")
TOP_KEYS = frozenset({"seq", "parent", "ts", "type", "proposer", "body", "sig"})
GENESIS_PARENT = "0" * 64
MAX_INT = 2**53 - 1
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")
TS = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
RULE_ID = re.compile(r"[a-z0-9_-]{1,64}")
TYPE = re.compile("|".join(TYPES))
NONEMPTY = re.compile(r".+", re.S)
BASE64 = re.compile(r"[A-Za-z0-9+/]+={0,2}")


class Refuse(Exception):
    """A refusal: reason code (closed set, SPEC.md) plus free-text detail."""

    def __init__(self, reason, detail="", rule=None):
        super().__init__(reason, detail)
        self.reason, self.detail, self.rule = reason, detail, rule


def canonical(obj):
    """The one serialisation of a JSON value that the log accepts."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def line_hash(line):
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def _scan(value, on_key=None, found=None):
    """Visit every scalar; collect defects: lone surrogates (malformed) and bad numbers (not canonical)."""
    found = {} if found is None else found
    if isinstance(value, dict):
        for k, v in value.items():
            _scan(k, on_key, found)
            if on_key:
                on_key(k)
            _scan(v, on_key, found)
    elif isinstance(value, list):
        for v in value:
            _scan(v, on_key, found)
    elif isinstance(value, float):
        found["number"] = "non-integer number"
    elif isinstance(value, int) and not isinstance(value, bool) and abs(value) > MAX_INT:
        found["number"] = "integer beyond 2^53-1"
    elif isinstance(value, str):
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            found["surrogate"] = "lone surrogate"
    return found


def _walk(value, on_key=None):
    found = _scan(value, on_key)
    if "surrogate" in found:
        raise Refuse("malformed_json", found["surrogate"])
    if "number" in found:
        raise Refuse("not_canonical", found["number"])


def parse_line(line):
    """Parse one log line; it must be a canonical JSON object."""
    try:
        obj = json.loads(line)
    except ValueError:
        raise Refuse("malformed_json") from None
    if not isinstance(obj, dict):
        raise Refuse("malformed_json", "not an object")
    _walk(obj)
    if canonical(obj) != line:
        raise Refuse("not_canonical")
    return obj


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _match(spec, value, where):
    """Declarative schema: regex → full-match string; type → isinstance;
    dict → required keys with sub-specs (extra keys allowed); tuple → list of spec."""
    ok = True
    if isinstance(spec, re.Pattern):
        ok = isinstance(value, str) and spec.fullmatch(value) is not None
    elif spec is int:
        ok = _is_int(value) and value >= 0
    elif isinstance(spec, type):
        ok = isinstance(value, spec)
    elif isinstance(spec, dict):
        if not isinstance(value, dict):
            ok = False
        else:
            for k, sub in spec.items():
                if k not in value:
                    raise Refuse("schema", f"{where}: missing {k}")
                _match(sub, value[k], f"{where}.{k}")
    elif isinstance(spec, tuple):
        if not isinstance(value, list):
            ok = False
        else:
            for i, v in enumerate(value):
                _match(spec[0], v, f"{where}.{i}")
    elif callable(spec):
        ok = spec(value)
    if not ok:
        raise Refuse("schema", f"{where}: bad value")


def check_shape(e):
    """Top-level shape of an entry (CHARTER §9.1)."""
    if set(e) != TOP_KEYS:
        raise Refuse("schema", "top-level keys")
    _match({"seq": int, "parent": HEX64, "ts": TS, "type": TYPE, "proposer": str,
            "body": dict, "sig": BASE64}, e, "entry")


def pubkey_blob(text):
    """'ssh-ed25519 <base64>' → the SSH wire blob, or None if malformed."""
    parts = text.split(" ") if isinstance(text, str) else []
    try:
        blob = base64.b64decode(parts[1], validate=True) if len(parts) == 2 else b""
    except ValueError:
        return None
    body = b"\x00\x00\x00\x0bssh-ed25519\x00\x00\x00\x20"
    ok = parts[:1] == ["ssh-ed25519"] and blob[:19] == body and len(blob) == 51
    return blob if ok else None


KEY_DECL = {"key_id": RULE_ID, "principal": NONEMPTY, "powers": (TYPE,),
            "pubkey": lambda v: pubkey_blob(v) is not None}
BODY = {
    "genesis": {"charter": HEX64, "checker": HEX64, "keys": (KEY_DECL,)},
    "key": KEY_DECL,
    "rule": {"rule_id": RULE_ID, "clauses": list, "witnesses": {"violating": list, "satisfying": list}},
    "repeal": {"rule_id": RULE_ID},
    "proposal": {"title": str, "commit": HEX40},
    "merge": {"proposal": int, "commit": HEX40, "checker": HEX64},
}


def _no_dots(key):
    if "." in key:
        raise Refuse("schema", f"body key contains '.': {key}")


def check_body(type_, body):
    """Per-type required fields; extra fields allowed; no dotted keys."""
    _match(BODY[type_], body, type_)
    if type_ == "rule" and "replacements" in body:
        _match(dict, body["replacements"], "rule.replacements")
    _walk(body, _no_dots)


def _flat(path, v):
    if isinstance(v, dict):
        return [f for k, x in v.items() for f in _flat(f"{path}.{k}", x)]
    if isinstance(v, list):
        return [f for i, x in enumerate(v)
                for f in (_flat(f"{path}.{i}", x) if isinstance(x, (dict, list)) else [(path, x)])]
    return [(path, v)]


def flatten(body):
    """Body → [(path, scalar)]: dotted paths; list atoms at the list's own path."""
    return [f for k, v in body.items() for f in _flat(k, v)]


def atom(v):
    """Tag a JSON scalar so that 1, true and "1" are distinct Datalog constants."""
    tag = "b" if isinstance(v, bool) else "i" if isinstance(v, int) else "s" if isinstance(v, str) else "n"
    return (tag, v)


def untag(a):
    return a[1]
