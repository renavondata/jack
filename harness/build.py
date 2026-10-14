"""Build signed logs for tests, pins and the simulator. Not kernel."""
from harness import keys
from kernel import log

TS = "2026-10-13T00:00:00Z"
HEX64 = "11" * 32
HEX40 = "22" * 20
ALL = list(log.TYPES)


def make_entry(seq, parent, type_, proposer, body, key, ts=TS, sig=None):
    """A canonical, signed log line (sig=... overrides the signature)."""
    e = {"seq": seq, "parent": parent, "ts": ts, "type": type_, "proposer": proposer, "body": body}
    e["sig"] = sig if sig is not None else keys.sign(key, log.canonical(e).encode())
    return log.canonical(e)


def decl(key_id, principal, key, powers):
    return {"key_id": key_id, "principal": principal, "pubkey": key.pubkey, "powers": list(powers)}


def genesis_body(decls, charter=HEX64, checker=HEX64):
    return {"charter": charter, "checker": checker, "keys": list(decls)}


def proposal(title="t", **extra):
    return dict({"title": title, "commit": HEX40}, **extra)


def merge(proposal_seq, checker=HEX64):
    return {"proposal": proposal_seq, "commit": HEX40, "checker": checker}


class Log:
    """An append-only chain of signed lines."""

    def __init__(self, lines=()):
        self.lines = list(lines)

    @property
    def head(self):
        return log.line_hash(self.lines[-1]) if self.lines else log.GENESIS_PARENT

    def add(self, type_, proposer, body, key, **kw):
        line = make_entry(len(self.lines), self.head, type_, proposer, body, key, **kw)
        self.lines.append(line)
        return line

    def text(self):
        return "".join(l + "\n" for l in self.lines)


class World:
    """Throwaway keys: guy (all powers) and ann (proposal only), plus a genesis."""

    def __init__(self, tmpdir):
        self.guy = keys.make_key(tmpdir, "guy")
        self.ann = keys.make_key(tmpdir, "ann")
        self.stranger = keys.make_key(tmpdir, "stranger")
        self.decls = [decl("guy-master", "guy", self.guy, ALL), decl("ann-1", "ann", self.ann, ["proposal"])]

    def log(self, **genesis_kw):
        lg = Log()
        lg.add("genesis", "guy", genesis_body(self.decls, **genesis_kw), self.guy)
        return lg
