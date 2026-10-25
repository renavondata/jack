"""Log format: canonical JSON, line hashes, entry shape, body schemas.

CHARTER §9.1. Pure functions; no I/O, no clock.
"""
import base64
import datetime
import hashlib
import json
import re

TYPES = ("genesis", "key", "proposal", "merge", "amend", "push", "decision", "spec_conflict", "forecast", "resolution")
TOP_KEYS = frozenset({"seq", "parent", "ts", "type", "proposer", "body", "sig"})
GENESIS_PARENT = "0" * 64
MAX_INT = 2**53 - 1
MAX_DEPTH = 32
KEY_FIELDS = frozenset({"key_id", "principal", "pubkey", "powers"})
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")
TS = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
IDENT = re.compile(r"[a-z0-9_-]{1,64}")
TYPE = re.compile("|".join(TYPES))
NONEMPTY = re.compile(r".+", re.S)
BASE64 = re.compile(r"[A-Za-z0-9+/]+={0,2}")


class Refuse(Exception):
    """A refusal: reason code (closed set, SPEC.md) plus free-text detail."""

    def __init__(self, reason, detail=""):
        super().__init__(reason, detail)
        self.reason, self.detail = reason, detail


def canonical(obj):
    """The one serialisation of a JSON value that the log accepts."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def line_hash(line):
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def _defects(value, found=None, depth=1):
    """Visit every scalar; collect defects: nesting beyond MAX_DEPTH and lone surrogates (malformed),
    bad numbers (not canonical)."""
    found = {} if found is None else found
    if isinstance(value, (dict, list)) and depth > MAX_DEPTH:
        found["depth"] = f"nested deeper than {MAX_DEPTH}"
    elif isinstance(value, dict):
        for k, v in value.items():
            _defects(k, found, depth + 1)
            _defects(v, found, depth + 1)
    elif isinstance(value, list):
        for v in value:
            _defects(v, found, depth + 1)
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


def parse_line(line):
    """Parse one log line; it must be a canonical JSON object."""
    try:
        obj = json.loads(line, parse_int=lambda s: int(s) if len(s) <= 20 else float("inf"))
    except (ValueError, RecursionError):
        raise Refuse("malformed_json") from None
    if not isinstance(obj, dict):
        raise Refuse("malformed_json", "not an object")
    found = _defects(obj)
    if "depth" in found or "surrogate" in found:
        raise Refuse("malformed_json", found.get("depth", found.get("surrogate")))
    if "number" in found or canonical(obj) != line:
        raise Refuse("not_canonical", found.get("number", ""))
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


def instant(v):
    """A UTC instant that exists: ASCII digits, a real Gregorian date, seconds 00-59 (SPEC.md §4)."""
    if not (isinstance(v, str) and TS.fullmatch(v)):
        return False
    try:
        datetime.datetime(int(v[0:4]), int(v[5:7]), int(v[8:10]), int(v[11:13]), int(v[14:16]), int(v[17:19]))
    except ValueError:
        return False
    return True


def check_shape(e):
    """Top-level shape of an entry (CHARTER §9.1)."""
    if set(e) != TOP_KEYS:
        raise Refuse("schema", "top-level keys")
    _match({"seq": int, "parent": HEX64, "ts": instant, "type": TYPE, "proposer": str,
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


KEY_DECL = {"key_id": IDENT, "principal": NONEMPTY, "powers": (TYPE,),
            "pubkey": lambda v: pubkey_blob(v) is not None}
BODY = {
    "genesis": {"charter": HEX64, "checker": HEX64, "keys": (KEY_DECL,)},
    "key": KEY_DECL,
    "proposal": {"title": str, "commit": HEX40},
    "merge": {"proposal": int, "commit": HEX40, "checker": HEX64},
    "amend": {"id": re.compile(r"[A-Z][0-9]{1,3}"), "charter": HEX64, "activate_at": _is_int},
    "push": {"digest": HEX64, "review": HEX64},
    "decision": {"kind": re.compile(r"veto|promote|budget|grant|transmute|fix"), "subject": NONEMPTY},
    "spec_conflict": {"section": NONEMPTY, "text": NONEMPTY},
    "forecast": {"claim": NONEMPTY, "p": lambda v: _is_int(v) and 1 <= v <= 999, "resolves_by": instant},  # p per mille
    "resolution": {"forecast": int, "outcome": lambda v: _is_int(v) and v in (0, 1), "evidence": NONEMPTY},
}


def check_body(type_, body):
    """Per-type required members; extra members are allowed."""
    _match(BODY[type_], body, type_)
    for d in body["keys"] if type_ == "genesis" else [body] if type_ == "key" else []:
        if set(d) != KEY_FIELDS:
            raise Refuse("schema", "a key declaration has exactly key_id, principal, pubkey, powers")
