"""Shared signed streams and disposable committed trees for clerk/status witnesses."""
import json
import tempfile
import unittest
from contextlib import contextmanager

from harness import build, gitfix, keys
from tools import status

NOW, DUE, LATE = "2026-10-31T12:00:00Z", "2026-11-03T00:00:00Z", "2026-11-03T00:00:01Z"


@contextmanager
def tree(files):
    with tempfile.TemporaryDirectory() as root:
        gitfix.git(root, "init", "-q")
        yield root, commit(root, files)


def commit(root, files):
    for path, data in files.items():
        gitfix.write(root, path, data)
    return gitfix.commit_all(root, "fixture")


class SignedFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.signers = {who: keys.make_key(cls.tmp.name, who) for who in ("guy", "counsel", "herald")}

    def setUp(self):
        self.s = Stream(self.signers)


class Stream:
    def __init__(self, signers):
        self.signers, self.log, self.es = signers, build.Log(), []
        self.add("genesis", "guy", **build.genesis_body([build.decl("guy", "guy", signers["guy"], build.ALL)]))
        for who in ("counsel", "herald"):
            self.add("key", "guy", **build.decl(who, who, signers[who], build.ALL))
        self.forecast(args={"id": "L0"})
        self.opening = self.add("decision", "guy", kind="promote", subject="C1a")

    def add(self, typ, who="herald", ts=NOW, **body):
        self.es.append(json.loads(self.log.add(typ, who, body, self.signers[who], ts=ts)))
        return self.es[-1]["seq"]

    def forecast(self, **body):
        return self.add("forecast", "counsel", **dict({"claim": "same claim", "p": 500, "resolves_by": DUE}, **body))

    def resolve(self, f, who="herald", ts=NOW, evidence="run"):
        return self.add("resolution", who, ts=ts, forecast=f, outcome=1, evidence=evidence)

    def merge(self, who="herald", ts=NOW):
        return self.add("merge", who, ts=ts, **build.merge(self.opening))

    def process(self):
        return status.item_process(self.es, self.opening)

    def complete(self, n, **body):
        for _ in range(n):
            self.resolve(self.forecast(**body))
            self.merge()
